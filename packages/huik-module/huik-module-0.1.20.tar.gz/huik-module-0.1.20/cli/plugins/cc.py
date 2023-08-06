import click
import re
from cli.utils import TableDisplay
from mymodule import mkdirs
import os
from datetime import datetime
from pathlib import PurePath
import shutil

@click.command()
@click.option('--folder','-f',default=None,type=click.Path(exists=False, file_okay=False,resolve_path=True),help="Provide folder to clean.")
@click.option('--pattern','-p',default=None, help = "Use custom regex pattern to delete.")
@click.option('--reverse','-r',is_flag=True,default=False,help='Reverse the deletion, move files and folders back.')
def cli(folder,pattern,reverse):
    """
    Clean files from a folder using regex pattern search.\n
    Default using icloud sync duplicate pattern / [2-9]$/ .
    """
    td=TableDisplay()
    op = 'reverse' if reverse else 'clean'
    folder = folder or click.prompt(td(text=f"Enter [path/to/folder] you want to {op}:")+'\n', default=os.getcwd())
    if reverse:
        try:
            click.echo(td(text=f'Reverse cleaning on folder [{folder}] ...'))
            reverse_deletion(folder)
            click.echo(td(title=">>> <g>SUCCESS</g> <<<",
                          text=f'Reversed cleaning on folder [{folder}]'))
        except Exception as e:
            click.echo(td(title=">>> <r>ERROR</r> <<<",text=f"Error: <r>{e}</r>"))
        return 
    pattern = pattern or click.prompt(td(text="Enter regex pattern:")+'\n', default=" [2-9]$") 
    try:
        pattern = re.compile(pattern)
    except re.error as e:
        click.echo(td(title=">>> <r>ERROR</r> <<<",text=f"Regex compile error: <r>{e}</r>"))
        return 
    if os.path.isdir(folder):       
        click.echo(td(text=f'Cleaning folder [{folder}] ...'))
        save , fileCount, folderCount= delete_by_pattern(folder,pattern) 
        click.echo(td(title=">>> <g>Result</g> <<<",
            text=f'Cleaning Done.\n{{{fileCount}}} files\n{{{folderCount}}} folders\nMoved to [{save}].'))
    else:
        click.echo(td(text=f"Path <r>{folder}</r> is invalid."))

def reverse_deletion(path):
    path = PurePath(path)
    tempfolder = path / '!DELETE SCRIPT TEMP FOLDER'
    filepath = tempfolder / 'Deleted files'
    folderpath = tempfolder / 'Deleted folders'
    f = open(tempfolder/'!Deletion Log.txt', 'r')
    def move(f,t,tag):
        if os.path.exists(f):
            shutil.move(f,t) 
            return
        click.echo(f'Miss [{tag}] <{filepath/p}>')

    for line in f.readlines():
        p = line.strip()[15:-1]
        if line.startswith("Move [ FILE ]"):
            move(filepath/p, path/p,' FILE ')
        elif line.startswith("Move [FOLDER]"):
            move(folderpath/p, path/p,'FOLDER')
    f.close()
   

def delete_by_pattern(path,pattern):
    regex = pattern.pattern
    movedFiles = 0
    movedFolders = 0
    tempfolder = PurePath(path) / '!DELETE SCRIPT TEMP FOLDER'
    filepath = tempfolder / 'Deleted files'
    folderpath = tempfolder / 'Deleted folders'
    mkdirs(tempfolder,filepath,folderpath)
    f = open(tempfolder/'!Deletion Log.txt', 'a')
    f.write(f'Start cleaning {path} on {datetime.now().strftime("%Y/%m/%d %H:%M")}\n')
    f.write(f"Cleaning pattern: >{regex}<\n")
    f.write('='*50+'\n')
    for root, dirs, files in os.walk(path):
        if str(tempfolder) in root:  # avoid looking into temp path.
            continue
        relative = PurePath(root).relative_to(path)
        if pattern.search(root):  # if the root folder is matched.
            click.echo(f'Move [FOLDER] <{relative}>')
            f.write(f'Move [FOLDER] <{relative}>\n')
            shutil.move(root, folderpath / relative)
            movedFolders += 1
            continue
        for file in files:
            if pattern.search(file):
                click.echo(f'Move [ FILE ] <{file}>')
                f.write(f'Move [ FILE ] <{os.path.join(relative, file)}>\n')
                os.makedirs(filepath / relative, exist_ok=True)
                shutil.move(os.path.join(root, file), filepath/relative/file)
                movedFiles += 1 #.append(oas.path.join(root, file))

    f.write('='*50+'\n')
    f.write(
        f'Cleaned {movedFiles} files, {movedFolders} folders, finished on {datetime.now().strftime("%Y/%m/%d %H:%M")}\n\n')
    f.close()
    return tempfolder, movedFiles, movedFolders
