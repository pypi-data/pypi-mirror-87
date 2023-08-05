# -*- coding: utf-8 -*-
# class RemoteTask(BaseTask):
# def __call__(self, *args, **kwargs):
#     super().__call__()
# from simple_slurm import Slurm
# ray_worker = Slurm(
#     cpus_per_task=self.num_cpus,
#     job_name="ray_worker",
# )
# redis_address = "171.20.135.102:6379"
# redis_password = "aa"
#
# venv_dir = "/home/gduvauchelle/.virtualenvs/kiss_raster_outflow/bin/"
# sbatch_string = f"{Path(venv_dir) / 'ray'} start --block --address='{redis_address}' --num-cpus={self.num_cpus} " \
# f"--memory={int(49e9)} --redis-password='{redis_password}' --resources='{{\"{self.worker_id}\":1}}' " \
# # f"--min-worker-port=12{int(index * 100 +1):03d} --max-worker-port=13{int(index * 100 + 100):03d}"
# print(sbatch_string)
#
# ray_worker.sbatch(sbatch_string)
