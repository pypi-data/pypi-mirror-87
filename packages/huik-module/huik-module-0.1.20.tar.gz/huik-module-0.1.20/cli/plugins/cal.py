import click
import math
import re
from cli.utils import TableDisplay
# init()

@click.command()
@click.argument("inputs",nargs=-1)
@click.option('--precision','-p','precision',default='9g',help="Precision,9g/9e/9f",show_default=True)
def cli(inputs,precision):
    """
    A big calculator.
    """
    # precision handing:
    precision = precision.strip('. ')

    formula = "".join(inputs)
    # replace log and ln
    formula = re.sub( "log\s*(?P<num>\d+)" , "math.log10(\g<num>)" , formula)
    formula = re.sub( "log\s*\((?P<num>.*)\)" , "math.log10(\g<num>)" , formula)
    formula = re.sub( "ln\s*(?P<num>\d+)" , "math.log(\g<num>)" , formula)
    formula = re.sub( "ln\s*\((?P<num>.*)\)" , "math.log(\g<num>)" , formula)

    # replace constant e and pi
    formula = re.sub( "eu" , "math.e" , formula)
    formula = re.sub( "pi" , "math.pi" , formula)

    # replace ^ by **
    formula = re.sub( "\^" , "**" , formula)
    formula = re.sub( "sqrt" , "math.sqrt" , formula)
    formula = re.sub( "sin" , "math.sin" , formula)
    formula = re.sub( "cos" , "math.cos" , formula)
    formula = re.sub( "tan" , "math.tan" , formula)
    formula = re.sub( "asin" , "math.asin" , formula)
    formula = re.sub( "acos" , "math.acos" , formula)
    formula = re.sub( "atan" , "math.atan" , formula)
    formula = re.sub( "abs" , "math.fabs" , formula)

    # replace factorial inside parenthesis
    formula = re.sub("\((?P<num>.*)\)!","math.factorial(\g<num>)",formula,)
    # replace factorial of numbers
    formula = re.sub("(?P<num>\s*\d+\s*)!","math.factorial(\g<num>)",formula)
    try:
        result = eval(formula)
        result = [(f'  [结果] = {{:.{precision}}}').format(result)]

    except Exception as e:
        result = [f"Formula : {formula}" , '<alert>Error {} </alert>'.format(e)]
    line1 = f'  [计算] <f>{"".join(inputs)}</f>'
    tf = TableDisplay({"[]":"fGsB",("<f>","</f>"):"fMsB","{}":"bB",("<alert>","</alert>"):"bR"})
    data = tf(title='{>>>计算器<<<}',text=[[line1],result])
    click.echo('')
    click.echo(data)
    click.echo('')
