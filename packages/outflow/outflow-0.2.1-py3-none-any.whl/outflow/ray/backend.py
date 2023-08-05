# -*- coding: utf-8 -*-
import multiprocessing
import os
import platform
import subprocess
import sys
import time

from outflow.core.backend import Backend as DefaultBackend
from outflow.core.generic.string import as_byte
from outflow.core.logging import logger
from outflow.ray.actors import MainActor

import ray


class Backend(DefaultBackend):
    def __init__(
        self, context=None, num_cpus=1, resources={"head_node": 1}, *args, **kwargs
    ):
        super().__init__(context=context)
        self._job_ids_queue = None
        self.setup_cluster()
        self.ray_actor = MainActor.options(
            resources=resources, num_cpus=num_cpus
        ).remote(context=self.pipeline_context, python_path=sys.path)

    def update_pipeline_context_args(self, pipeline_args, extra_args):
        self.ray_actor.update_pipeline_context_args.remote(pipeline_args, extra_args)

    @property
    def job_ids_queue(self):
        if self._job_ids_queue is None:
            self._job_ids_queue = multiprocessing.Queue()

        return self._job_ids_queue

    @staticmethod
    def launch_nodes(
        ray_params: dict,
        num_nodes: int,
        job_ids_q: multiprocessing.Queue,
        stop_event: multiprocessing.Event,
    ):
        class StreamToLogger(object):
            def __init__(self, logger):
                self.logger = logger
                self.linebuf = ""

            def write(self, buf):
                import logging

                for line in buf.rstrip().splitlines():
                    self.logger.log(logging.DEBUG, line.rstrip())

            def flush(self):
                pass

        from outflow.core.logging import logger

        sys.stdout = StreamToLogger(logger)

        from simple_slurm import Slurm

        ray_node = Slurm(
            cpus_per_task=ray_params["num_cpus"],
            job_name="ray_node",
        )

        for index in range(num_nodes):
            if index > 0:
                time.sleep(5)

            if stop_event.is_set():
                return

            python_path = sys.executable

            sbatch = (
                "srun {python_path} -m ray.scripts.scripts start --block --address='{redis_address}' "
                "--num-cpus={num_cpus} "
                "--redis-password='{_redis_password}' ".format(
                    python_path=python_path,
                    **ray_params
                    # memory=node_config["memory"],
                )
            )

            job_ids_q.put(ray_node.sbatch(sbatch))

    def setup_cluster(self):
        """
        Starts the ray head server, the main worker and sbatch the nodes
        """
        import ray

        # shutdown ray to avoid re-init issues
        ray.shutdown()

        # launch ray head server and main worker
        ray_params = dict()

        cluster_config = self.pipeline_context.config.get("cluster", {})

        if "mem_per_node" in cluster_config:
            # --- Binary ---
            # 1 MiB = 1024 * 1024
            # 1 MiB = 2^20 bytes = 1 048 576 bytes = 1024 kibibytes
            # 1024 MiB = 1 gibibyte (GiB)

            # --- Decimal ---
            # 1 MB = 1^3 kB = 1 000 000 bytes

            ray_params.update({"_memory": as_byte(cluster_config["mem_per_node"])})
        if "cpu_per_node" in cluster_config:
            ray_params.update({"num_cpus": cluster_config["cpu_per_node"]})

        ray_params.update(
            {"_redis_password": cluster_config.get("redis_password", "outflow")}
        )

        # FIXME: fix ray to support parallel job on windows
        if platform.system() == "Windows" or self.pipeline_context.config["local_mode"]:
            ray_params.update({"local_mode": True})

        # needed when plugins are not installed but only in python path
        os.environ["PYTHONPATH"] = ":".join(sys.path)

        ray_info = ray.init(**ray_params, resources={"head_node": 1e5})

        ray_params.update({"redis_address": ray_info["redis_address"]})

        num_nodes = cluster_config.get("num_nodes", 0)

        self.stop_event = multiprocessing.Event()

        if num_nodes > 0:
            logger.info(f"Launching {num_nodes} ray nodes")

            self.sbatch_proc = multiprocessing.Process(
                target=self.launch_nodes,
                args=(ray_params, num_nodes, self.job_ids_queue, self.stop_event),
            )
            self.sbatch_proc.start()

        else:
            logger.info(
                "No cluster config found in configuration file, "
                "running in a local cluster"
            )

    def run(self, *, task_list=[]):
        main_actor_result = self.ray_actor.run.remote(task_list=task_list)
        result = -1

        try:
            result = ray.get(main_actor_result)
        # except TypeError as te:  # FIXME maybe
        #     if "missing 1 required positional argument: 'task_context'" in te.args[0]:
        #         print('Task expected a context but "with_context" is False')
        #     raise
        finally:
            if hasattr(self, "sbatch_proc"):
                self.stop_event.set()
                self.sbatch_proc.join()
            while not self.job_ids_queue.empty():
                slurm_id = self.job_ids_queue.get()
                logger.debug("cancelling slurm id {id}".format(id=slurm_id))
                subprocess.run(["scancel", str(slurm_id)])

        return result
