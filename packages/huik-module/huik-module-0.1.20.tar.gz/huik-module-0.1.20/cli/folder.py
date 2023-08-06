import click
import subprocess as sub
from cli.utils import TableDisplay, Config
import os 

config = Config('folders')


td = TableDisplay()

def displayMenu(data):
    data = data.get('favorites',{})
    dis = []
    for k in sorted(data.keys()):
        dis.append(f" >><g> [ {k} ] </g><< {data[k]}  ")
    click.echo(td(title= "[>> Favorite Folders <<]", text=[dis]))


def mark_fav(ctx,param,value):
    if not value or ctx.resilient_parsing:
        return
    cwd = os.getcwd()
    key = click.prompt(td(text=f'Enter name for favorite folder\n@ [{cwd}]')+'\n')
   
    data = config.readData()
    if data.get('favorites',None) is None:
        data['favorites'] = {}

    todis = []
    for k in key.split():
        data['favorites'][k]=cwd
        todis.append(f" >><g> [ {k} ] </g><< {cwd} ")

    config.saveData(data)
    click.echo(td(title=">>> <g>Favorite folder Saved</g> <<<",
                text=[todis]))
    ctx.exit()

def drop_fav(ctx,param,value):
    if not value or ctx.resilient_parsing:
        return
    data = config.readData()

    fav = data.get('favorites',{})
    displayMenu(data)
    key = click.prompt('Choose folder(s) to Delete',default="",show_default=False)
    dis = []
    if not key: ctx.abort()
    for k in key.split():
        if k in fav:
            dis.append(f"Deleted >><g> [ {k} ] </g><< {fav.pop(k)}")
        else:
            dis.append(f">> <a>{k}</a> << is not in favorites.")
    click.echo(td(text=[dis]))
    config.saveData(data)
    ctx.exit()

def config_shell(ctx,p,value):
    if not value or ctx.resilient_parsing:
        return
    data = config.readData()
    
    cs = data.get('shell','zsh')

    data['shell']  = click.prompt('Choose which shell to use', 
        type=click.Choice(['zsh', 'bash'],case_sensitive=False), 
        default='zsh',show_default=True )

    config.saveData(data)
    click.echo(f'Changed shell to {data["shell"]}.')
    ctx.exit()


@click.command() 
@click.option('--mark','-m',callback=mark_fav,is_flag=True,is_eager=True,
            expose_value=False,help="Mark current dir to favorite.")
@click.option('--drop','-d',callback=drop_fav,is_flag=True,is_eager=True,
            expose_value=False,help="Remove favorite folder.")
@click.option('--config','-c',callback=config_shell,is_flag=True,is_eager=True,
            expose_value=False,help="Configure default shell. Default zsh")
@click.argument('path',nargs=1,default=None,required=False)
@click.pass_context
def folder(ctx,path):
    """
    cd to favorite folders by $ fd \n
    Default shell is zsh, if need to use bash, use fd -c to config.
    """
    data = config.readData()
    fav=data.get('favorites',{})

    if path is None:
        displayMenu(data)
        path = click.prompt('Choose folder',default="",show_default=False)
        if not path: ctx.abort()
    
    if path not in fav:
        click.echo(td(text=f"'<r>{path}</r>' isn't in your favorites."))
        ctx.exit()

    if os.path.isdir(fav[path]):
        sub.run(f"cd '{fav[path]}'; exec {data.get('shell','zsh')} ",shell=True,)
    else:
        click.echo(td(text=f"Folder '<y>{fav[path]}</y>' doesn't exist."))


