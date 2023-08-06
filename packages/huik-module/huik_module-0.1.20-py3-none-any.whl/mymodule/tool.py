from inspect import signature
import timeit
import psutil
import multiprocessing
from itertools import product
import subprocess 


class LazyProperty():
    """
    lazy property descriptor class.
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

class FT_Decorator():
    def __init__(self,freq=1,callback=None,show=True):
        self.freq = freq
        self.callback = callback
        self.avgtime = 0
        self.count = 0
        self.show  = show

    def __call__(self,func):
        """
        decorator for printing execution time of a function.
        """
        sig = signature(func)
        def wrapped(*args, **kwargs):
            t1 = timeit.default_timer()
            result = func(*args, **kwargs)
            t2 = timeit.default_timer()


            self.avgtime = (self.count * self.avgtime + t2 - t1 ) / (self.count + 1)
            self.count += 1

            if self.callback:
                self.callback(t2-t1)

            if self.show and (self.count % self.freq == 0):
                print('Run {} {} times: avg: {:.5f}s; latest: {:.5f}s'.format(
                    func.__name__, self.count, self.avgtime, t2-t1))
            return result
        wrapped.__signature__ = sig
        wrapped.__name__ = func.__name__
        return wrapped

def ft_decorator(freq=1):
    def _ft_decorator(func):
        """
        decorator for printing execution time of a function.
        """
        sig = signature(func)
        avgtime = 0
        runcount = 0
        def wrapped(*args, **kwargs):
            nonlocal avgtime, runcount
            t1 = timeit.default_timer()
            result = func(*args, **kwargs)
            t2 = timeit.default_timer()
            avgtime = (runcount * avgtime + t2 - t1 ) / (runcount + 1)
            runcount += 1
            if runcount % freq == 0:
                print('Run {} {} times: avg: {:.5f}s; para:{}{}'.format(
                    func.__name__, runcount, avgtime, args, kwargs))
            return result
        wrapped.__signature__ = sig
        wrapped.__name__ = func.__name__
        return wrapped
    return _ft_decorator

def ft(func,args,kwargs={}, number=100):
    """
    use timeit to time [number] execution of function.
    """
    def wrapper():
        return func(*args,**kwargs)
    t = timeit.timeit(wrapper, number=number)
    print('Run {} {} times: total {:.6f}s; average {:.6f}s.'.format(func.__name__, number, t,t/number))
    return t

def poolMap(task,workload,initializer=None,initargs=None,chunks=None,
            total=None,progress_callback=None,progress_gap=(0,100),**kwargs):
    """
    speed up task in a list by multiprocessing.
    task is the function to apply on workload.
    workload is a iterable containing the task inputs.
    initializerr and initargs can be used to setup the function.
    """
    workerheads=psutil.cpu_count(logical=False)
    worker=multiprocessing.Pool(workerheads,initializer,initargs)
    total = total or len(workload)
    chunksize= int(total//chunks)+1 if chunks else int(total/workerheads/10+1)
    result = []
    count=0
    progress = progress_gap[0]
    for _ in worker.imap(task, workload, chunksize):
      count+=1
      result.append(_)
      if progress_callback :
          current_pro = count/total*(progress_gap[1]-progress_gap[0])+progress_gap[0]
          if current_pro > progress + 1:
              progress = current_pro
              progress_callback(current_pro)
    worker.close()
    worker.join()
    worker.terminate()
    return result


def cartesian(*arrays):
    """
    Give a list of arrays, return iterator of product of elements from arrays.
    similar to python product, but also yield indexes.
    """
    lenths = [len(i) for i in arrays]
    l = product(*lenths)
    p = product(*arrays)
    for i,j in zip(l,p):
        yield i,j



class MyPrint:
    """
    use mprint the same way as print().
    Set printToScreen = False to disable print. 
    Set mprint.callback to provide a callabck(msg) function when printToScreen is disabled.
    by default, call back is void().
    """
    printToScreen = True
  

    def callback(self,msg):
        return 
        
    def __call__(self,msg):
        if self.printToScreen:
            print(msg)
        else:
            self.callback(msg)
   
mprint = MyPrint()


class ProgressBar:
    """
    Class to display a progress bar, or pure count at a given frequency. 
        start: the start progress in percentage. default = 0 
        limits: the upper and lower bound of the iteration count. Set this limits so that in later calls, can use the number of iteration to display progress percentage automatically.
        prefix, suffix: text to display before and after the progress bar.
        length: length of the bar, default to be 70% of the terminal window width.
        percent_frequency: update frequency in percentage. default 0.1(%)
        number_frequency: update frequency of number if the percentage of progress cannot be determined. default = 1.
    """

    def __init__(self, start=0, limits=None, prefix='Progress', suffix="", decimals=2, length=None, percent_frequency=0.1, number_frequency=1):
        WINDOWSIZE = [int(i) for i in subprocess.run(
        'stty size', shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.split()]
        if WINDOWSIZE and length == None:
            TermRow, TermCol = WINDOWSIZE
            length = int(TermCol*0.6)
        else:
            length = length or 100
        self.prefix = prefix 
        self.length = length 
        self.suffix = suffix 
        self.template = "\r{} |{}| {:." + str(decimals) + "%} {}"
        self.progress = start
        self.frequency = percent_frequency / 100
        self.interval = number_frequency
        self.limits = limits
        self.default = None
        self.iteration = 0 # start iteration
       

    def __call__(self,value=None):
        "automatically determine what to use and use that for later. "
        if value == None:
            self.iteration += 1
            value = self.iteration
        if value<1:
            return self.display_percent(value)
        else:
            return self.display_iteration(value)

    def draw_bar(self):
        "draw the bar with length equal to self.length."
        filllength = int(self.length * max(min(self.progress, 1),0)) 
        bar = '█'*filllength + '-'*(self.length - filllength)
        print(self.template.format(self.prefix, bar, self.progress, self.suffix),end='\r')

    def draw_number(self):
        "draw a number equal to self.length."
        num = "{:.0f} ".format(self.progress) 
        bar = " "*(self.length - len(num)-1) + num 
        print(f"\r{self.prefix} |{bar}| {self.suffix}",end='\r')

    def display_percent(self,percent):
        "give a percentage, display if its above the frequency."
        if percent - self.progress >= self.frequency:
            self.progress = percent 
            self.draw_bar()

    def display_iteration(self,iteration):
        "give a iteration number, display the percentage of this number relative to the given iteration interval"
        if not self.limits: 
            return self.display_number(iteration)
        p = (iteration - self.limits[0]) / (self.limits[1] - self.limits[0])
        return self.display_percent(p) 
    
    def display_number(self,number):
        "display a blunt number, incase the upper limit of this progress is unknown, thus unable to show progress percentage."
        if number - self.progress >= self.interval:
            self.progress = number
            self.draw_number()
            
    def end_bar(self):
        "end the bar display. This should be called when you want to keep the bar displayed in terminal after it's done."
        print()
