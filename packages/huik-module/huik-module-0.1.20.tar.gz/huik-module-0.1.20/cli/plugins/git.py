import os,json
import click
import subprocess as sub
from datetime import datetime as date
import socket
from cli.utils import TableDisplay
import re

@click.group(invoke_without_command=True)
@click.option('-v', is_flag=True,help='Use this flag to auto increment __version__ in __version__.* file.')
@click.pass_context
def cli(ctx,v):
    """
    git pull add commit push 4 step in one.
    """
    if ctx._depth == 2:
        if v: 
            versionfile=[]
            packagejson=[]
            for root,folder,files in os.walk(os.getcwd()):
                for file in files:
                    fullpath = os.path.join(root,file)
                    if file.split('.')[0]=='_version_':
                        versionfile.append(fullpath)
                    elif file.strip() == 'package.json':
                        if not ('node_modules' in root):
                            packagejson.append(fullpath)

            trueVersion = []
            for f in versionfile:
                try:
                    data = open(f,'rt').read()
                    if '__version__' in data:
                        trueVersion.append((f,data))
                except:
                    pass

            count = len(trueVersion) + len(packagejson)
            if count>1 or count==0:
                if count>1:
                    click.echo(f"Found these __version__ files:")
                    for f,d in trueVersion:
                        click.echo(f)
                    for f in packagejson:
                        click.echo(f)
                if not click.confirm(f'{"More" if count>1 else "Less"} than one _version_.* file was found, ignore version and continue?',default=True,):
                    return 
            else:
                foundVersion=False
                if trueVersion:
                    file,data = trueVersion[0]
                    data = data.split('\n')
                    for k,line in enumerate(data):
                        p = re.compile('\d+\.\d+\.\d+')
                        if '__version__' in line:
                            m=p.search(line)
                            if m:
                                foundVersion=True
                                ver = m.group()
                                verl = ver.split('.')
                                verl[-1] = str(int(verl[-1])+1)
                                newver = '.'.join(verl)
                                data[k] = line.replace(ver,newver)
                                
                else:
                    file = packagejson[0]
                    with open(file,'rt') as f:
                        data = json.load(f)
                    ver = data['version']
                    ov = ver.split('.')
                    ov[-1] = str(int(ov[-1])+1)
                    newver = '.'.join(ov)
                    data['version'] = newver

                    foundVersion=True

                if foundVersion:
                    if not click.confirm(f"Update __version__ in {file} from <{ver}> to <{newver}> ?", default=True):
                        return
                    with open(file,'wt') as f:
                        if trueVersion:
                            f.write('\n'.join(data))
                        else:
                            json.dump(data,f,indent=2)
                else:
                    click.echo(f'No __version__ can be found in <{file}>.')

        click.echo('\nGit pull')
        sub.run('git pull',shell=True,)
        click.echo('\nCommit to Git')
        msg = click.prompt("Enter a comment",show_default=True,
            default=f"ON: {date.now().strftime('%c')}, FROM: {socket.gethostname()}")
        sub.run(f'git add . \n git commit -m "{msg}" \n git push',shell=True)
        result = sub.run('git config --get remote.origin.url',stdout=sub.PIPE,encoding='utf-8',shell=True).stdout
        td = TableDisplay()
        click.echo(td(title='>>> <g>! Success</g> <<<',text=f"Commited to [{result.strip()}]"))

README="# This Repo is created by [OK git][huik]\n[![python version](https://img.shields.\
io\/badge/python-3.5%20%7C%203.6%20%7C%203.7%20-blue)][pythonwebsite]\n[![Alt text]\
(https://img.shields.io/pypi/v/huik-module 'Hover to see this text.')][huik]\n### \
Emphasis\n*Italic* ; **Bold** ; ***Bold and Italic*** ; ~~Scratch~~\n### List items\n1. \
First ordered list item\n* Unordered list can use asterisks\n\n[huik]:https://pypi.org\
/project/huik-module\n[pythonwebsite]: https://www.python.org/downloads/release/python-375\n"

IGNORE={
"py": '*.py[cod]\n__pycache__\n*.so\n.env\n*.json\ntest*.*\ntest*\n*.bak\n*.dat\n*.dir\
\n*.egg\n*.egg-info\ndump.rdb\ndist\nbuild\neggs\nparts\nbin\nvar\nsdist\ndevelop-eggs\n\
.installed.cfg\nlib\nlib64\n.DS_Store\npip-log.txt\n.coverage\n.tox\nnosetests.xml\n*.vscode\
\n*.code-workspace\n*.mo\n.mr.developer.cfg\n.project\n.pydevproject\n.env\nvenv\nlogs\n',
"js":'/node_modules\n/.pnp\n.pnp.js\n/coverage\n/build\n.DS_Store\n.env.local\n\
.env.development.local\n.env.test.local\n.env.production.local\nnpm-debug.log*\
\nyarn-debug.log*\nyarn-error.log*\n'
}

@cli.command()
@click.option('--javascript','-js','project',flag_value='js',help='Setup javascript .gitignore')
@click.option('--python','-py','project',flag_value='py',help='Setup python .gitignore')
def init(project):
    "Init a new git package with .gitignore and README.md"
    if not project:
        project =  click.prompt("Type of project to init",
        show_default=True,type=click.Choice(["py","js"],case_sensitive=False),
        default="py")
    with open('README.md','wt') as f:
        f.write(README)
    with open('.gitignore','wt') as f:
        f.write(IGNORE[project])
    url = click.prompt("Enter github repo url")
    sub.run(f'git init\ngit add .\ngit commit -m "First Commit"\ngit remote add origin {url}\ngit push --set-upstream origin master',shell=True)
   
    
    