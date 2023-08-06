import click
import subprocess
from cli.utils import  TableDisplay, Config
from cli._version_ import __version__
from cli.ok import print_version

TL_CONFIG = Config('tools')

td = TableDisplay()

def displayMenu(data):
    dis = []
    for k in sorted(data.keys()):
        dis.append(f" >><g> [ {k} ] </g><< {data[k]['name']}  ")
    click.echo(td(title= "[>>Tools Menu<<]", text=[dis]))

def displayCommand(data,items):
    if not items: items = sorted(data.keys())
    dis = []
    for k in items:
        if k in data:
            dis.extend([f" >><g> [ {k} ] </g><< {data[k]['name']}", f" {data[k]['command']}"])
        else:
            dis.append(f" >><r> [ {k} ] </r><< is not in your tool list.")
    click.echo(td(title= "[>>Tools Menu<<]", text=[dis]))



def run_tool(key,data):
    """
    key is the key to command dictionary sotred in data dict.
    data dict: key:{name: ... , command: ...}
    """
    if not key:
        click.echo(td(text="<y>No option selected.</y>"))
        return
    if key in data:
        name = data[key]['name']
        command = data[key]['command']
        click.echo(td(text=f"Run [{name}]\n$ <i>{command}</i>"))
        subprocess.run(command,shell=True)
    else:
        click.echo(td(text=f" <r>'{key}'</r> <y>not in menu.</y>"))
        return

@click.command()
@click.option('--version','-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,help='Show version.')
@click.option('-a','--add','ops',flag_value='add', help="Add new command.")
@click.option('-d','--delete','ops',flag_value='delete',help="Delete a command.")
@click.option('-e','--edit','ops',flag_value='edit',help="Edit a command.")
@click.option('-o','--open','ops',flag_value='open',help="Open command configure in editor.")
@click.option('-ls','ls',is_flag=True,help='List current commands.')
@click.argument('arg',nargs=-1,default=None)
@click.pass_context
def toollist(ctx,arg,ops,ls):
    """
    Open Tools menu  by $ tl\n
    Directly invoke tool list command by $ tl [command key].\n
    Configure tools list by $ tl -a/-e/-d/-o.
    """
    
    if ops:
        config(ops)
        ctx.exit()

    data = TL_CONFIG.readData()

    if ls: 
        displayCommand(data,arg)
        ctx.exit() 


    if not arg:
        displayMenu(data)
        key = click.prompt('Enter Key',default="",show_default=False)
        return run_tool(key,data)

    for key in arg:
        run_tool(key,data)
        ctx.exit() 


def config(ops):
    """
    To configure the tool list menu.
    """
    if ops == "open":
        subprocess.run(f"open {TL_CONFIG.path}",shell=True)
        return

    data = TL_CONFIG.readData()
    if ops == "add":
        click.echo("Add a New Command")
        name = click.prompt('Enter Command Name', type=str)
        click.echo(f"You Entered: {name}\n")
        command = click.prompt('Enter Command Script',type=str)
        click.echo(f"You Entered: {command}\n")
        key = click.prompt('Enter Associated Key',type=str)
        click.echo(f"You Entered: {key}\n")
        if click.confirm('Do you want to save?',abort=True,default=True):
            temp = key
            while temp in data:
                temp+="d"
            if temp != key:
                data[temp]=data.pop(key)
            data[key]={'name':name,'command':command}

    elif ops == "delete":
        displayMenu(data)
        keys = click.prompt('Enter the command you wan to delete',type=str)
        for key in keys.split():
            if key in data:
                name = data.pop(key)['name']
            else:
                click.echo(td(title="",text=[[f"<a> '{key}' not in menu.</a>"]]))
    elif ops == 'edit':
        displayMenu(data)
        key = click.prompt('Enter the command you wan to edit',type=str)
        if key not in data:
            click.echo(td(title="",text=[[f"<a> '{key}' not in menu.</a>"]]))
            return
        edit = data[key]
        name = click.prompt('Enter New Command Name', default=edit['name'])
        click.echo(f"You Entered: {name}\n")
        command = click.prompt('Enter New Command Script',default=edit['command'])
        click.echo(f"You Entered: {command}\n")
        newkey = click.prompt('Enter New Associated Key',default=key)
        click.echo(f"You Entered: {newkey}\n")
        if click.confirm('Do you want to save?',abort=True,default=True):
            data.pop(key)
            temp = newkey
            while temp in data:
                temp+="d"
            if temp != newkey:
                data[temp]=data.pop(newkey)
            data[newkey]={'name':name,'command':command}

    TL_CONFIG.saveData(data)

    click.echo(td(title="",text=f"<g> {ops.capitalize()} to '{name}' was saved.</g>"))




if __name__ == "__main__":
    toollist()
