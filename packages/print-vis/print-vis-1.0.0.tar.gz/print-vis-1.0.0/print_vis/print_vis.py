import threading
import time

def clear():
    print("\033c", end="")
    
def clear_line():
    print ("\033[A                             \033[A")

class progress_bar:
    def __init__(self,size,update=True,**kwargs):
        self.filled_char = "█" if not 'filled_char' in kwargs else kwargs['filled_char']
        self.off_char = "-" if not 'off_char' in kwargs else kwargs['off_char']
        self.show_percent = True if not 'show_percent' in kwargs else kwargs['show_percent']
        self.string_template = f'[{"%"*size}]'
        self.string = self.string_template.replace('%',self.off_char)
        self.update_line = update
        self.size = size
        print(self.string,'0%' if self.show_percent else '')
    def update(self,value):
        num_of_on = round(value/100 * self.size)
        self.string = self.string_template.replace('%',self.filled_char,num_of_on).replace('%',self.off_char)
        if(self.update_line):
            clear_line()
        percent = str(value)+'%'
        print(self.string,percent if self.show_percent else '')

class loading_wheel:
    def __init__(self,persistent = True,chars = ['|','/','-','\\'],**kwargs):
        self.chars = iter(chars)
        self._chars = chars
        self.speed = 0.5 if not 'speed' in kwargs else kwargs['speed']
        self.Exit = False
        if(persistent):
            threading.Thread(target=self._start).start()
    def _start(self):
        ''' in thread '''
        while True:
            try:
                print(next(self.chars))
            except:
                self.chars = iter(self._chars)
                print(next(self.chars))
            time.sleep(self.speed)
            clear_line()
            if(self.Exit): break
    def next(self):
        try:
            print(next(self.chars))
        except:
            self.chars = iter(self._chars)
            print(next(self.chars))
    def exit(self):
        self.Exit = True
