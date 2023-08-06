import click
import os
from mymodule import mkdirs

plugin_folder = os.path.join(os.path.dirname(__file__), 'plugins')
mkdirs(plugin_folder)

def list_plugins(rv=[]):
    for filename in os.listdir(plugin_folder):
        if filename.endswith('.py'):
            temp = filename[:-3]
            if temp not in rv:
                rv.append(temp)
    return rv

class MyCLI(click.MultiCommand):
    """
    lazy load of sub commands from commands folder. 
    """
    commandList = {}
    def list_commands(self, ctx):
        rv = list(self.commandList.keys())
        rv = list_plugins(rv)
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        if name in self.commandList:
            return self.commandList[name]
        fn = os.path.join(plugin_folder, name + '.py')
        ns = {'__file__':fn}
        if os.path.isfile(fn):
            with open(fn) as f:
                # code = compile(f.read(), fn, 'exec')
                exec(f.read(), ns, ns)
            return ns['cli']
        else:
            return None

    def add_command(self,f):
        self.commandList[f.__name__] = f

    def add_command(self, cmd, name=None):
        """Registers another :class:`Command` with this group.  If the name
        is not provided, the name of the command is used.
        """
        name = name or cmd.name
        if name is None:
            raise TypeError("Command has no name.")
        if name in self.list_commands(1):
            raise RuntimeError(f'Command {name} already exist.')
        self.commandList[name] = cmd

    def command(self, *args, **kwargs):
        """A shortcut decorator for declaring and attaching a command to
        the group.  This takes the same arguments as :func:`command` but
        immediately registers the created command with this instance by
        calling into :meth:`add_command`.
        """
        command = click.command

        def decorator(f):
            cmd = command(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd
        return decorator


@click.group(cls=MyCLI)
def _plugins():
    pass 


@_plugins.command()
@click.option('--show-folder',"-sf",default=False, is_flag=True,help="Open plugins folder.")
@click.option('--install',"-i","file",default=None,type=click.Path(exists=True,dir_okay=False), help="Install to plugins folder.") #
@click.pass_context
def plugins(ctx,show_folder,file):
    """
    Manage plugins. Show folder or install plugin.
    Call directly will show a list of all currently available plugins.
    """
    if show_folder:
        import subprocess
        click.echo(f"Plugins stored in: {plugin_folder}")
        subprocess.run(f"cd {plugin_folder}\nopen .\n",shell=True)
        return 
    if file:
        from shutil import copyfile
        from cli.ok import menu
        cmds = menu.list_commands(ctx)
        click.echo(f"Current commands: {cmds}")
        name=click.prompt("Enter a different name for your plugin")
        if name in cmds:
            click.echo(f'!Failed. <{name}> is alread in use.')
            ctx.exit()
        copyfile(file,os.path.join(plugin_folder,f"{name}.py"))
        click.echo(f"Command <{name}> installed to plugins folder.")
        return

    # display installed plugin list 
    rv = list_plugins()
    click.echo(f'Currently installed plugins: {rv}')