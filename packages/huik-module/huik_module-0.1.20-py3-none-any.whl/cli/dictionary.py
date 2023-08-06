import click
import requests
from cli.utils import ColorText,TableDisplay,Config
import json

APIs = Config('api')
_data = APIs.readData()
COL_API_KEY=_data.get("COL_API_KEY",None)
MED_API_KEY=_data.get("MED_API_KEY",None)
URBAN_API_KEY=_data.get("URBAN_API_KEY",None)

def lookupMW(word,limit):
    url1=f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={COL_API_KEY}"
    url2=f"https://www.dictionaryapi.com/api/v3/references/medical/json/{word}?key={MED_API_KEY}"
    try:
        if COL_API_KEY is None or (MED_API_KEY is None):
            raise ValueError ("Missing API key for M-W dictionary. Run def --config to setup.")
        r1 = requests.request("GET", url1, ).json()
        r2 = requests.request("GET", url2, ).json()
        def process(r):
            result = []
            for k,d in enumerate(r[0:limit]):
                if not isinstance(d,dict):
                    continue
                _def = [("<gDef {}.g> [{}]".format(k+1,d.get('fl','None')))]
                for i,l in enumerate(d.get('shortdef',[])):
                    _def.append(f"  [{i+1}]. {l}")
                result.append(_def)
            return result
        res1 = process(r1)
        res2 = process(r2)
        result = [["{From M-W Collegiate Dictionary}"]]+res1+[["{From M-W Medical Dictionary}"]]+res2

        return result
    except Exception as e:
        return e


def lookupUrban(word,limit):
    """
    look up word on urban dictionary, export a upper limit
    """
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    querystring = {"term":word}
    headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': URBAN_API_KEY
        }
    try:
        if URBAN_API_KEY is None:
            raise ValueError ("No API key for urban dictionary. Run def --config to setup.")
        response = requests.request("GET", url, headers=headers, params=querystring)
        r=response.json()
        result = []
        for k,d in enumerate(r['list'][0:limit]):
            _def = [("<gDef {}.g> {}".format(k+1,d.get('definition',"None")))]
            txt    =[f'<gExample:g>']
            exp = list((d.get('example',"None")).split('\n'))
            result.append(_def+txt+exp)
        return result
    except Exception as e:
        return e

def run_config():
    ck = click.prompt("Enter Key for M-W collegiate dictionary",default=COL_API_KEY)
    mk = click.prompt("Enter Key for M-W medical dictionary",default=MED_API_KEY)
    uk = click.prompt("Enter Key for Urban dictionary",default=URBAN_API_KEY)
    data = APIs.readData()
    newdata = dict(COL_API_KEY=ck,MED_API_KEY=mk,URBAN_API_KEY=uk)
    data.update(newdata)
    click.echo('You have entered these keys:')
    click.echo(json.dumps(newdata,indent=4),)
    if click.confirm('Do you want to save?',abort=True,default=True):
        APIs.saveData(data)
    click.echo('API keys are saved.')

@click.group()
def dictionary():
    pass

@dictionary.command('def')
@click.argument("word",nargs=-1)
@click.option('-u','--urban','-urban','dictionary',flag_value="urban",default=False,help="Use Urban Dictionary")
@click.option('-mw','--mw','-m','-mw','dictionary',flag_value="mw",default=True,help="Use M-W Dictionary")
@click.option("--dictionary",'-d',type=click.Choice(['mw',"urban"],case_sensitive=False),default='mw',help="Select M-W or Urban Dictionary")
@click.option("--limit",'-l',default=5,help="Limit explanation entries")
@click.option("--config",is_flag=True,help="Configure Dictionary API keys")
@click.pass_context
def _def(ctx,word,limit,dictionary,config):
    """
    Dictionary. Support Urban Dict / M-W Dict.
    """
    if config:
        run_config()
        ctx.exit()
    if not word:
        click.echo(ctx.get_help())
        word = click.prompt('Please enter a word', type=str)
    else:
        word = " ".join(word)
    bkcolor = ColorText(mapping={"[]":"fC",("<g","g>") : "fG",("<alert>","</alert>"):"bR","{}":"bB"})
    if dictionary == "urban":
        result = lookupUrban(word,limit)
    else:
        result = lookupMW(word,limit)
    if isinstance(result,list) and result:
        td=TableDisplay(bkcolor)
        click.echo("")
        title = " DEFINITION : <g"+f">>> {word.capitalize()} <<<g>"
        click.echo(td.format(title=title,text=result))
        click.echo("")
    else:
        click.echo("")
        click.echo(bkcolor(f'<alert>!Unable to find online definition. \n <{result}> </alert>'))
        click.echo("")
