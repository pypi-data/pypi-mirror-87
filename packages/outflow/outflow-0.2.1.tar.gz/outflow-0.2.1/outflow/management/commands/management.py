# -*- coding: utf-8 -*-
from outflow.core.command import RootCommand


@RootCommand.subcommand(invokable=False)
def Management():
    pass


@Management.subcommand(with_task_context=True)
def DisplayConfig(self):
    print(self.context.config)


@Management.subcommand(with_task_context=True)
def Shell(self):
    # Opens a shell inside the outflow context
    import code

    try:
        import readline  # allow Up/Down/History  # noqa: F401
    except ImportError:
        #  readline is not available for Windows
        pass

    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()
