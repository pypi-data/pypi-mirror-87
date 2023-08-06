import re,json,os
from colorama import init, Fore,Back,Style
from textwrap import TextWrapper
from terminaltables import SingleTable

from mymodule import mkdirs

# WINDOWSIZE=[int(i) for i in subprocess.run('stty size', shell=True, stdout=subprocess.PIPE,encoding='utf-8').stdout.split()] 
TermCol , TermRow =  os.get_terminal_size()

class ColorText():
    """
    Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Style: DIM, NORMAL, BRIGHT, RESET_ALL
    """
    _color ={"K":"BLACK","R":"RED","Y":"YELLOW","G":"GREEN","B":'BLUE',"M":"MAGENTA","C":"CYAN","W":"WHITE",}
    _style={"D":"DIM","N":"NORMAL","B":"BRIGHT"}
    _mapping = {"f":_color,"s":_style,"b":_color}
    _type={'f':Fore,'b':Back,"s":Style}
    def __init__(self,mapping={"[]":"fC","{}":"bKfY",('<i>','</i>'):"fKbW", ("<g>","</g>") : "fG", ("<b>","</b>") : "fB", 
                ("<r>","</r>") : "fR",("<m>","</m>") : "fM",("<y>","</y>") : "fY", ("<a>","</a>"):"bR",}):
        """
        mapping: { pattern : color }
        pattern: "[]"/"{}"/(<p>,</p>)
        color:"fBbWsD"
        """
        self.color = {}
        ptns = []
        for k,i in mapping.items():
            color = ""
            for (s,c) in zip(i[::2],i[1::2]):
                color+=getattr(self._type[s],self._mapping[s][c])
            ptns.append((f"{re.escape(k[0])}(?P<{i}>.*?){re.escape(k[1])}"))
            self.color[i]=color
        self.pattern = re.compile("|".join(ptns),flags=re.DOTALL)

    def format(self,text):
        return self(text)

    def __call__(self,text,):
        def repl(x):
            mk = [k for k,i in x.groupdict().items() if i!=None][0]
            ct = x.groupdict()[mk]
            return self.color[mk]+ct+Style.RESET_ALL
        return self.pattern.sub(repl,text)


class TableDisplay():
    def __init__(self,color=ColorText()):
        self.col = (TermCol)
        if isinstance(color,dict):
            self.color = ColorText(color)
        else:
            self.color=color

    def format(self,title="",text=[]):
        """
        text = [ [ row 1 [ line1, line2 ] ], [row 2 [ lines]] ]
        if text is a string, then convert to single row, but respect the \n
        """
        if isinstance(text,str):
            text = [[i for i in text.split('\n')]]
        tw = TextWrapper(fix_sentence_endings=True,width=self.col-4)
        table_data = [ [self.color("\n".join(tw.fill(j,) for j in i))] for i in text]
        table = SingleTable(table_data,self.color(title))
        table.inner_row_border = True
        return table.table

    def __call__(self,title="",text=[]):
        return self.format(title,text)



class Config():
    """
    Class to store and read saved configure data.
    """
    folder = os.path.join(os.path.dirname(__file__), 'conf')
    def __init__(self,name):
        self.name = name 
        self.create()

    def create(self):
        mkdirs(self.folder)
        if not os.path.isfile(self.path):
            _=open(self.path,'wt')
            _.write("{}")
            _.close()
        
    @property
    def path(self):
        return os.path.join(self.folder,self.name+'.json')

    def readData(self):
        with open(self.path,'rt') as f:
            return json.load(f)

    def saveData(self,data,):
        with open(self.path,'wt') as f:
            json.dump(data,f,indent=2,)

    @staticmethod
    def list_config():
        fd = Config.folder
        mkdirs(fd)
        res = []
        for fn in os.listdir(fd):
            if fn.endswith('.json'):
                res.append(fn[:-5])
        return res