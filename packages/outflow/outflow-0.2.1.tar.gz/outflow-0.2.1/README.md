<div align="center">
   <img src="https://gitlab.lam.fr/CONCERTO/outflow/-/raw/develop/docs/sections/images/logo.svg" width="500" style="max-width: 500px;">
</div>

<div align="center">

<a href="https://pypi.org/project/outflow/">
  <img src="https://img.shields.io/pypi/pyversions/outflow.svg" alt="python">
</a>

<a href="https://pypi.org/project/outflow/">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/outflow">
</a>

<a href="https://gitlab.lam.fr/CONCERTO/outflow/-/commits/develop">
  <img alt="pipeline status" src="https://gitlab.lam.fr/CONCERTO/outflow/badges/develop/pipeline.svg" />
</a>

<a href="https://gitlab.lam.fr/CONCERTO/outflow/-/commits/develop">
  <img alt="coverage report" src="https://gitlab.lam.fr/CONCERTO/outflow/badges/develop/coverage.svg" />
</a>

<a href=https://github.com/ambv/black>
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>

<a href='https://docs.outflow.dev'>
  <img src='https://readthedocs.org/projects/outflow/badge/?version=latest' alt='Documentation Status' />
</a>

<a href="https://pypi.python.org/pypi/outflow">
  <img src="https://img.shields.io/pypi/l/outflow.svg" alt="license" />
</a>

<a href="https://discord.outflow.dev/">
  <img src="https://img.shields.io/badge/discord-support-7389D8?logo=discord&style=flat&logoColor=fff" alt="chat-discord-support" />
</a>



</div>

Outflow is a framework that helps you build and run task workflows.

The api is as simple as possible while still giving the user full control over the definition and execution of the
workflows.

**Feature highlight :**
 - Simple but powerful API
 - Support for **parallelized and distributed execution**
 - Centralized **command line interface** for your pipeline commands
 - Integrated **database** access, sqlalchemy models and alembic migrations
 - Executions and exceptions logging for **tracability**
 - Strict type and input/output checking for a **robust** pipeline

Check out our [documentation][outflow readthedocs] for more information.

[outflow readthedocs]: https://docs.outflow.dev

# Installing

Install and update using [pip](https://pip.pypa.io/en/stable/):

```
pip install -U outflow
```

# Quick start

## One file starter

Create a `pipeline.py` script:

```python
# -- pipeline.py
from outflow.core.command import Command, RootCommand
from outflow.core.pipeline import Pipeline
from outflow.core.target import Target
from outflow.core.tasks.task import Task


# with the as_task decorator, the function will be automatically converted into a Task subclass
# the signature of the function, including the return type, is used to determine task inputs and outputs
@Task.as_task
def GetValues() -> {'a': str, 'b': str}:
    return {'a': 'hello', 'b': 'world'}

# default values can also be used as inputs
@Task.as_task
def PrintValues(a: str, b: str, c: str = '?' ):
    print(f"{a} {b}{c}")

@RootCommand.subcommand()
class HelloWorld(Command):

    def setup_tasks(self):
        # instantiate tasks
        get_values = GetValues()

        # you can specify inputs value during instantiation
        print_values = PrintValues(c="!")

        # build the workflow
        get_values >> print_values

        # return the terminating task(s) of the workflow
        # they will be used as entrypoints to navigate through the execution tree
        return [print_values]

if __name__ == "__main__":
    from outflow.core.pipeline import settings

    # use the default settings
    settings.configure()

    # instantiate and run the pipeline
    pipeline = Pipeline(settings_module=None)
    result = pipeline.run()


```

and run your first Outflow pipeline:

```
$ python pipeline.py hello_world
```

## A robust, configurable and well-organized pipeline

You had a brief overview of Outflow's features and you want to go further. Outflow offers command line tools to help you to start your pipeline project.

First, we will need to auto-generate the pipeline structure -- a collection of files including the pipeline settings, the database and the cluster configuration, etc.

```
$ python -m outflow management create pipeline my_pipeline
```

Then, we have to create a plugin -- a dedicated folder regrouping the commands, the tasks as well as the description of the database (the models)
```
$ python -m outflow management create plugin my_namespace.my_plugin --plugin_dir my_pipeline/plugins/my_plugin
```

In the my_pipeline/settings.py file, add your new plugin to the plugin list:

```python
PLUGINS = [
    'outflow.management',
    'my_namespace.my_plugin',
]
```

and run the following command:

```
$ python ./my_pipeline/manage.py my_plugin
```

You'll see the following output on the command line:

```
 * outflow.core.pipeline.pipeline - pipeline.py:325 - INFO - No cluster config found in configuration file, running in a local cluster
 * my_namespace.my_plugin.commands - commands.py:49 - INFO - Hello from my_plugin
```

Your pipeline is up and running. You can now start adding new tasks and commands.

# Contributing

For guidance on setting up a development environment and how to make a contribution to Outflow, see the [contributing guidelines](https://gitlab.lam.fr/CONCERTO/outflow/-/blob/master/CONTRIBUTING.md).
