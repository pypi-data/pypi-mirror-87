#-*- encoding: utf-8 -*-
#encoding: utf-8
from __future__ import print_function
VERSION = "X.X"
import os
import sys
import inspect
import random
import socket
import cmdw
import datetime
from make_colors import make_colors
import configparser
import re
import traceback
import ctypes
if not sys.platform == 'win32':
    import ctypes
PID = os.getpid()
HANDLE = None
MAX_WIDTH = cmdw.getWidth()

DEBUG = False
if DEBUG == 1 or DEBUG == '1':
    DEBUG = True
elif DEBUG == 0 or DEBUG == '0':
    DEBUG = False

if os.getenv('DEBUG') == 1 or os.getenv('DEBUG') == '1':
    DEBUG = True
if os.getenv('DEBUG') == 0 or os.getenv('DEBUG') == '0':
    DEBUG = False

if isinstance(DEBUG, str):
    DEBUG = bool(DEBUG.title())

DEBUG_SERVER = os.getenv('DEBUG_SERVER')
if DEBUG_SERVER == 1 or DEBUG_SERVER == '1':
    DEBUG_SERVER = True
if DEBUG_SERVER == 0 or DEBUG_SERVER == '0':
    DEBUG_SERVER = False
if DEBUG_SERVER == "True" or DEBUG_SERVER == True:
    DEBUG_SERVER = True

DEBUGGER_SERVER = ['127.0.0.1:50001']
CONFIG_NAME = os.path.join(os.path.dirname(__file__), 'debug.ini')
PATH = ''
if PATH:
    CONFIG_NAME = os.path.join(PATH, os.path.basename(CONFIG_NAME))

try:
    cfg = configparser.RawConfigParser(allow_no_value=True)
    cfg.optionxform = str
    cfg.read(CONFIG_NAME)
    try:
        cfg = cfg.get('DEBUGGER', 'HOST')
    except:
        try:
            cfg.set('DEBUGGER', 'HOST', '0.0.0.0')
        except configparser.NoSectionError:
            cfg.add_section('DEBUGGER')
            cfg.set('DEBUGGER', 'HOST', '0.0.0.0')
        cfg_data = open(CONFIG_NAME, 'w')
        cfg.write(cfg_data)
        cfg_data.close()
        cfg = cfg.get('DEBUGGER', 'HOST')
    if ";" in cfg:
        DEBUGGER_SERVER = re.split(";", cfg)
    else:
        DEBUGGER_SERVER = [cfg]
except:
    traceback.format_exc()

if os.getenv('DEBUGGER_SERVER'):
    if ";" in os.getenv('DEBUGGER_SERVER'):
        DEBUGGER_SERVER = os.getenv('DEBUGGER_SERVER').strip().split(";")
    else:
        DEBUGGER_SERVER = [os.getenv('DEBUGGER_SERVER')]
# print("DEBUGGER_SERVER =", DEBUGGER_SERVER)
FILENAME = ''
if os.getenv('DEBUG_FILENAME'):
    FILENAME = os.getenv('DEBUG_FILENAME')

class configset(object):
    cfg = configparser.RawConfigParser(allow_no_value=True)
    cfg.optionxform = str
    THIS_PATH = os.path.dirname(__file__)

    def __init__(self):
        super(configset, self)
        global CONFIG_NAME
        global PATH
        self.cfg = configparser.RawConfigParser(allow_no_value=True)
        self.cfg.optionxform = str        
        self.configname = CONFIG_NAME
        if self.configname:
            configname = self.configname

        self.path = None
        if not self.path:
            self.path = os.path.dirname(inspect.stack()[0][1])
        if PATH:
            self.path = PATH
        # debug(self_path = self.path)

        configname = os.path.join(self.path, os.path.basename(configname))
        # debug(configname=configname)

    def get_config_file(self, filename='', verbosity=None):
        if not filename:
            filename = self.configname
        configname = filename
        self.configname = configname
        #debug(configname = filename)
        self.configname = configname
        #debug(configset_configname = self.configname)
        self.path = None
        if self.path:
            if os.getenv('DEBUG'):
                print ("001")
            if configname:
                self.configname = os.path.join(os.path.abspath(self.path), os.path.basename(self.configname))

        if os.path.isfile(os.path.join(os.getcwd(), filename)):
            if os.getenv('DEBUG'):
                print ("002")
            #debug(checking_001 = "os.path.isfile(os.path.join(os.getcwd(), filename))")
            self.configname = os.path.join(os.getcwd(), filename)
            #debug(configname = os.path.join(os.getcwd(), filename))
            return os.path.join(os.getcwd(), filename)
        elif os.path.isfile(filename):
            if os.getenv('DEBUG'):
                print ("003")
            #debug(checking_002 = "os.path.isfile(filename)")
            self.configname =filename
            #debug(configname = os.path.abspath(filename))
            return filename
        elif os.path.isfile(os.path.join(os.path.dirname(__file__), filename)):
            if os.getenv('DEBUG'):
                print ("004")
            #debug(checking_003 = "os.path.isfile(os.path.join(os.path.dirname(__file__), filename))")
            self.configname =os.path.join(os.path.dirname(__file__), filename)
            #debug(configname = os.path.join(os.path.dirname(__file__), filename))
            return os.path.join(os.path.dirname(__file__), filename)
        elif os.path.isfile(self.configname):
            if os.getenv('DEBUG'):
                print ("005")
            #debug(checking_004 = "os.path.isfile(configname)")
            #debug(configname = os.path.abspath(configname))
            return configname
        else:
            if os.getenv('DEBUG'):
                print ("006")
            #debug(checking_006 = "ELSE")
            fcfg = self.configname
            f = open(fcfg, 'w')
            f.close()
            filecfg = fcfg
            #debug(CREATE = os.path.abspath(filecfg))
            return filecfg

    def write_config(self, section, option, filename='', value=None, cfg = None, verbosity=None):
        #print ("SECTION:", section)
        #print ("OPTION :", option)
        if not os.path.isfile(self.configname):
            filename = self.get_config_file(filename, verbosity)
        else:
            filename = self.configname
        if not cfg:
            cfg = configset.cfg
        if cfg:
            cfg.read(filename)
        else:
            cfg = configparser.RawConfigParser(allow_no_value=True)
            cfg.optionxform = str
            cfg.read(filename)
        try:
            cfg.set(section, option, value)
        except configparser.NoSectionError:
            cfg.add_section(section)
            cfg.set(section, option, value)
        except configparser.NoOptionError:
            cfg.set(section, option, value)

        if os.path.isfile(filename):
            cfg_data = open(filename,'w+')
        else:
            cfg_data = open(filename,'wb')

        cfg.write(cfg_data) 
        cfg_data.close()  

        return self.read_config(section, option, filename)

    def read_config(self, section, option, filename='', value=None, verbosity=None):
        """
            option: section, option, filename='', value=None
        """
        if not os.path.isfile(self.configname):
            filename = self.get_config_file(filename, verbosity)
        else:
            filename = self.configname

        self.cfg.read(filename)
        try:
            data = self.cfg.get(section, option)
        except:
            #if os.getenv('DEBUG') or os.getenv('DEBUG_SERVER'):
            #    traceback.format_exc()
            #else:
                #traceback.format_exc(print_msg= False)
            pass
            self.write_config(section, option, filename, value)
            data = configset.cfg.get(section, option)
        return data

class debugger(object):

    global VERSION
    global CONFIG_NAME

    VERSION = "x.x"

    def __init__(self, defname = None, debug = None, filename = None, **kwargs):
        super(debugger, self)
        self.DEBUG = debug
        self.FILENAME = filename
        self.platform = sys.platform
        if DEBUG:
            self.DEBUG = DEBUG
        if FILENAME:
            self.FILENAME = FILENAME
        #print "self.FILENAME =", self.FILENAME
        if os.getenv('DEBUG') and os.getenv('DEBUG') == 1 or os.getenv('DEBUG') and os.getenv('DEBUG') == '1' or os.getenv('DEBUG') and os.getenv('DEBUG') == True or os.getenv('DEBUG') and os.getenv('DEBUG') == "True":
            self.DEBUG = True
        #import configset
        self.CONFIG = configset()
        self.CONFIG.configname = CONFIG_NAME
        #print ("CONFIG_NAME =", CONFIG_NAME)
        #self.CONFIG = configparser.RawConfigParser(allow_no_value=True)
        #self.CONFIG.opionxform = str
        #self.CONFIG.read(CONFIG_NAME)
        self.read_config = self.CONFIG.read_config
        self.get_config_file = self.CONFIG.get_config_file

    def version(cls):
        print("version:", VERSION)

    version = classmethod(version)

    def debug_server_client(self, msg, server_host = '127.0.0.1', port = 50001):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if DEBUGGER_SERVER:
            for i in DEBUGGER_SERVER:
                if ":" in i:
                    host, port = str(i).strip().split(":")
                    port = int(port.strip())
                    host = host.strip()
                    if not host:
                        host = '127.0.0.1'
                else:
                    if str(i).isdigit():
                        host = '127.0.0.1'
                        port = int(i)
                    else:
                        host = i.strip()
                if host == '0.0.0.0':
                    host = '127.0.0.1'
                # print ("host =", host)
                # print ("port =", port)
                # print("message =", str(msg))
                try:
                    s.sendto(bytes(msg.encode('utf-8')), (host, port))
                except UnicodeDecodeError:
                    pass
                except OSError:
                    pass
                except:
                    #if os.getenv('DEBUG') == '1':
                    traceback.format_exc()
                s.close()
        else:
            print("self.read_config('DEBUGGER', 'HOST') =", self.read_config('DEBUGGER', 'HOST'))
            if self.read_config('DEBUGGER', 'HOST'):
                if ":" in self.read_config('DEBUGGER', 'HOST'):
                    host, port = str(self.read_config('DEBUGGER', 'HOST')).strip().split(":")
                    port = int(port.strip())
                    host = host.strip()
                else:
                    host = self.read_config('DEBUGGER', 'HOST').strip()
                s.sendto(msg, (host, port))
                s.close()                

    def setDebug(self, debug):
        self.DEBUG = debug

    def get_len(self, objects):
        if isinstance(objects, list) or isinstance(objects, tuple) or isinstance(objects, dict):
            return len(objects)
        else:
            if sys.platform == 'win32':
                if sys.version_info.major == 2:
                    return len(unicode(objects))
                else:
                    return len(str(objects))
            else:
                return len(str(objects))

        return 0

    def track(self, check = False):
        if not check:
            if self.read_config('DEBUG', 'debug') == 1 or os.getenv('DEBUG') or os.getenv('DEBUG_SERVER'):
                traceback.format_exc()
        else:
            if self.read_config('DEBUG', 'debug') == 1: #or os.getenv('DEBUG') or os.getenv('DEBUG_SERVER'):
                return True
        return False

    def colored(self, strings, fore, back = None, with_colorama = False, attrs = []):
        if self.read_config('COLORS', 'colorama') == 1 or os.getenv('colorama') == 1 or with_colorama:
            if back:
                return fore + strings + back
            else:
                return fore + strings
        else:
            return make_colors(strings, fore, back, attrs)


    def printlist(self, defname = None, debug = None, filename = '', linenumbers = '', print_function_parameters = False, **kwargs):
        
        cls = False
        formatlist = ''
        if DEBUG_SERVER:
            debug_server = True

        if not filename:
            filename = self.FILENAME

        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)

        if not debug:
            debug = self.DEBUG
        
        color_random_1 = ['lightgreen', 'lightyellow', 'lightwhite', 'lightcyan', 'lightmagenta']
        
        arrow = make_colors(' -> ', 'lg')
            
        if print_function_parameters:
            for i in args:
                if i == 'self':
                    pass
                else:
                    try:
                        if sys.platform == 'win32':
                            formatlist = make_colors((str(i) + ": "), 'lw', 'bl') + make_colors(str(values[i]), color_random_1[int(args.index(i))]) + arrow
                        else:
                            formatlist = termcolor.colored((str(i) + ": "), 'lw', 'bl') + color_random_1[int(args.index(i))] + str(values[i]) + arrow
                    except:
                        formatlist = str(i) + ": " + str(values[i]) + arrow
                    if not defname:
                        defname = str(inspect.stack()[1][3])
                    if filename == None:
                        filename = sys.argv[0]
                    linenumbers = str(inspect.stack()[1][2])
                    try:
                        if sys.platform == 'win32':
                            formatlist = make_colors(datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f'), 'white') + " " + make_colors(defname + arrow, 'lw', 'lr') + formatlist + " " + "[" + str(filename) + "]" + " " + " [" + make_colors(str(linenumbers), 'lw', 'lc') + "] "
                        else:
                            formatlist = termcolor.colored(datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f'), 'white') + " " + termcolor.colored(defname + arrow, 'lw', 'lr') + formatlist + " " + "[" + str(filename) + "]" + " "  + " [" + termcolor.colored(str(linenumbers), 'lw', 'lc') + "] "
                    except:
                        formatlist = datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f') + " " + defname + arrow + formatlist + " " + "[" + str(filename) + "]" + " " + " [" + str(linenumbers) + "] "
                    if debug:
                        print(formatlist)
                    if DEBUG_SERVER:
                        self.debug_server_client(formatlist)            
            return formatlist
        if not kwargs == {}:
            for i in kwargs:
                if sys.version_info.major == 2:
                    i = i.encode('utf-8')
                if str(i) == "cls" or str(i) == "clear":
                    cls = True                
                try:
                    if kwargs.get(i) == '' or kwargs.get(i) == None:
                        formatlist += make_colors((str(i)), 'lw', 'bl') + arrow
                    else:
                        if sys.version_info.major == 2:
                            formatlist += make_colors(str(i) + ": ", 'b', 'ly') + make_colors(unicode(kwargs.get(i)), 'lc') + arrow + make_colors("TYPE:", 'b', 'ly') + make_colors(str(type(kwargs.get(i))), 'b', 'lc') + arrow + make_colors("LEN:", 'lw', 'lm') + make_colors(str(self.get_len(kwargs.get(i))), 'lightmagenta') + arrow 
                        else:
                            formatlist += make_colors((str(i) + ": "), 'b', 'ly') + make_colors(str(kwargs.get(i)), 'lc') + arrow + make_colors("TYPE:", 'b', 'ly') + make_colors(str(type(kwargs.get(i))), 'b', 'lc') + arrow + make_colors("LEN:", 'lw', 'lm') + make_colors(str(self.get_len(kwargs.get(i))), 'lightmagenta') + arrow
                except:
                    if os.getenv('DEBUG'):
                        traceback.format_exc()
                    if os.getenv('DEBUG_ERROR'):
                        try:
                            self.debug_server_client(traceback.format_exc(print_msg=False))
                        except:
                            print("Send traceback ERROR [290]")

                    try:
                        if kwargs.get(i) == '' or kwargs.get(i) == None:
                            formatlist += str(i).encode('utf-8') + arrow
                        else:
                            formatlist += str(i) + ": " + str(kwargs.get(i)) + arrow
                    except:
                        if os.getenv('DEBUG_ERROR'):
                            try:
                                self.debug_server_client(traceback.format_exc(print_msg=False))
                            except:
                                print("Send traceback ERROR [290]")
        else:
            try:
                formatlist += " " + make_colors("start ... ", random.choice(color_random_1)) + arrow
            except:
                try:
                    formatlist += " start... " + arrow
                except:
                    formatlist += " start... " + ' -> '

        formatlist = formatlist[:-4]
        defname_parent = ''
        defname_parent1 = ''
        the_class = ''
        
        if defname and isinstance(defname, str):
            if filename == None:
                #frame = inspect.stack()[1]
                #module = inspect.getmodule(frame[0])
                #filename = module.__file__
                #filename = inspect.stack()[2][3]
                filename = sys.argv[0]
            #defname = defname + " [" + str(inspect.stack()[0][2]) + "] "

            filename = make_colors(filename, 'lightgreen')

            try:
                formatlist = make_colors(datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f'), 'lw') + " " + make_colors(defname + arrow, 'lw', 'lr') + formatlist + " " + "[" + str(filename) + "]" + " "  + make_colors("[", "cyan") + make_colors(str(linenumbers)[2:-2], 'lw', 'lc') + make_colors("]", "lc") + " " + make_colors("PID:", 'red', 'lg') + make_colors(str(PID), 'lw')
            except:
                formatlist = datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f') + " " + defname + arrow + formatlist + " " + "[" + str(filename) + "]" + " "  + "[" + str(linenumbers)[2:-2] + "]"
        else:
            defname = str(inspect.stack()[2][3])
            if defname == "<module>":
                defname = sys.argv[0]
            try:
                the_class = re.split("'|>|<|\.", str(inspect.stack()[1][0].f_locals.get('self').__class__))[-3]
            except:
                pass
            if len(inspect.stack()) > 2:
                for h in inspect.stack()[3:]:
                    if isinstance(h[2], int):
                        if not h[3] == '<module>':
                            defname_parent1 += "[%s]" % (h[3]) + arrow
                            defname_parent += "%s" % (make_colors(h[3], 'lc')) + "[%s]" % (make_colors(str(h[2]), 'lightwhite', 'lightred')) + arrow
                #defname_parent = inspect.stack()[1][3]
            if the_class and not the_class == "NoneType":

                defname_parent += "(%s)" % (make_colors(the_class, 'lightwhite', 'blue')) + arrow
                
                defname_parent1 += "(%s)" % (the_class) + arrow
            
            if not linenumbers:
                try:
                    #line_number =  " [" + make_colors(str(inspect.stack()[1][2]), 'white', 'on_cyan') + "] " + " " + make_colors("PID:", 'red', 'lightgreen') + make_colors(str(PID), 'lightwhite')
                    line_number = make_colors("PID:", 'red', 'lightgreen') + make_colors(str(PID), 'lightwhite')
                except:
                    self.track()
                    line_number =  " [" + str(inspect.stack()[1][2]) + "] "
            else:
                linenumbers = str(linenumbers).strip()
                line_number = linenumbers + make_colors("PID:", 'r', 'lg') + make_colors(str(PID), 'lw')
                linenumbers = " [" + make_colors(str(linenumbers)[1:], 'r', 'lw') + make_colors("PID:", 'r', 'lg') + make_colors(str(PID), 'lw')
            if filename == None:
                filename = sys.argv[0]
            try:
                formatlist = make_colors(datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f'), 'b', 'lc') + " " + make_colors(defname, 'lw', 'lr') + make_colors(arrow, 'lr') + defname_parent + formatlist + "[" + make_colors(defname + ":", 'lw', 'lr') + make_colors(str(filename) + "]", 'lg') + " " + line_number
            except:
                self.track()
                formatlist = datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f') + " " + defname + arrow + defname_parent1 + formatlist + "[" + str(filename) + "] [" + str(inspect.stack()[1][2]) + "] "  + line_number

        if self.track(True):
            try:
                print(formatlist)
            except:
                pass
        else:
            if os.getenv("DEBUG") == '1' or debug or DEBUG == '1' or DEBUG == True:
                try:
                    if not formatlist == 'cls':
                        if sys.version_info.major == 2:
                            print(formatlist.encode('utf-8'))
                        else:
                            print(formatlist)
                except:
                    print("TRACEBACK =", traceback.format_exc())

        if DEBUG_SERVER or debug:
            # self.debug_server_client(formatlist + " [%s] [%s]" % (make_colors(ATTR_NAME, 'white', 'on_blue'), PID))
            if cls:
                formatlist = 'cls'
            
            self.debug_server_client(formatlist)
        cls = False
        #if debug_server:
            #self.debug_server_client(formatlist)
        
        return formatlist

def debug_server_client(msg, server_host = '127.0.0.1', port = 50001):
    global CONFIG_NAME
    try:
        if read_config('RECEIVER', 'HOST', CONFIG_NAME):
            RECEIVER_HOST = read_config('RECEIVER', 'HOST', CONFIG_NAME)
    except:
        pass
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if RECEIVER_HOST:
        for i in RECEIVER_HOST:
            if ":" in i:
                host, port = str(i).strip().split(":")
                port = int(port.strip())
                host = host.strip()
            else:
                host = i.strip()
            if host == "0.0.0.0":
                host = '127.0.0.1'
            
            s.sendto(msg, (host, port))
            s.close()

def debug_self(**kwargs):
    return debug(**kwargs)

def get_config(section, option, configname = 'debug.ini', value = ''):
    global CONFIG_NAME
    cfg = configparser.RawConfigParser(allow_no_value=True)
    cfg.optionxform = str

    if configname:
        configname = os.path.join(os.path.dirname(__file__), os.path.basename(configname))
    else:
        configname = CONFIG_NAME

    debug_self(configname = configname)    
    cfg.read(configname)

    try:
        data = cfg.get(section, option)
    except:
        try:
            try:
                cfg.set(section, option, value)
            #except configparser.NoSectionError:
            except:
                cfg.add_section(section)
                cfg.set(section, option, value)
            #except configparser.NoOptionError:
                #pass
            cfg_data = open(configname,'wb')
            cfg.write(cfg_data) 
            cfg_data.close()  
        except configparser.NoOptionError:
            pass
        except:
            traceback.format_exc()
        data = cfg.get(section, option)
    return data    

def serve(host = '0.0.0.0', port = 50001, on_top=False, center = False):
    if on_top:
        set_detach(center = center, on_top = on_top)
    global DEBUGGER_SERVER
    import socket
    host1 = ''
    port1 = ''
    if DEBUGGER_SERVER:
        if isinstance(DEBUGGER_SERVER, list):
            for i in DEBUGGER_SERVER:
                if ":" in i:
                    host1, port1 = str(i).split(":")
                    port1 = int(port1)
                    if not host1:
                        host1 = '127.0.0.1'
                else:
                    if str(i).isdigit():
                        port1 = int(i)
                    else:
                        host1 = i
        else:
            if ":" in DEBUGGER_SERVER:
                host1, port1 = str(DEBUGGER_SERVER).split(":")
                port1 = int(port1)
                if not host1:
                    host1 = '127.0.0.1'
            else:
                if str(DEBUGGER_SERVER).isdigit():
                    port1 = int(i)
                else:
                    host1 = DEBUGGER_SERVER
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if not host:
        if get_config('DEBUGGER', 'HOST', value= '0.0.0.0'):
            host = get_config('DEBUGGER', 'HOST')
        else:
            host = host1
    if not port:
        if get_config('DEBUGGER', 'PORT', value= '50001'):
            port = get_config('DEBUGGER', 'PORT')
            port = int(port)
        else:
            port = port1
    #print ("DEBUGGER_SERVER =", DEBUGGER_SERVER)
    if not host:
        host = '127.0.0.1'
    if not port:
        port = 50001
    while 1:
        try:
            s.bind((host, int(port)))
            break
        except socket.error:
            port = port + 1

    print(make_colors("BIND: ", 'white', 'green') + make_colors(host, 'white', 'red', attrs= ['bold']) + ":" + make_colors(str(port), 'black', 'yellow', attrs= ['bold']))
    while 1:
        msg = s.recv(6556500)
        if msg:
            if msg == 'cls' or msg == 'clear':
                if sys.platform == 'win32':
                    os.system('cls')
                else:
                    os.system('clear')
            else:
                showme()
                print(str(msg))
            if sys.platform == 'win32':
                print("=" * (MAX_WIDTH - 3))
            else:
                print("=" * ((MAX_WIDTH * 2) - 3))

def debug(defname = None, debug = None, debug_server = False, line_number = '', print_function_parameters = False, **kwargs):
    
    #if not defname:
        #print "inspect.stack =", inspect.stack()[1][2]
    #    defname = inspect.stack()[1][3]
    #print("inspect.stack() =", inspect.stack())
    #print("inspect.stack()[1][2] =", inspect.stack()[1][2])
    #print("inspect.stack()[1][2] =", type(inspect.stack()[1][2]))
    line_number =  " [" + make_colors(str(inspect.stack()[1][2]), 'red', 'lightwhite') + "] "
    #print("line_number =", line_number)
    #defname = str(inspect.stack()[1][3]) + " [" + str(inspect.stack()[1][2]) + "] "
    c = debugger(defname, debug)
    
    msg = c.printlist(defname, debug, linenumbers = line_number, print_function_parameters= print_function_parameters, **kwargs)
    
    return msg

def set_detach(width = 700, height = 400, x = 10, y = 50, center = False, buffer_column = 9000, buffer_row = 77, on_top = True):
    if not sys.platform == 'win32':
        return False
    from dcmd import dcmd
    setting = dcmd.dcmd()
    setting.setBuffer(buffer_row, buffer_column)
    screensize = setting.getScreenSize()
    setting.setSize(width, height, screensize[0] - width, y, center)
    if on_top:
        setting.setAlwaysOnTop(width, height, screensize[0] - width, y, center)

def showme():
    if not sys.platform == 'win32':
        return False
    global HANDLE
    # import ctypes
    # import win32gui, win32con
    # import ctypes
    # kernel32 = ctypes.WinDLL('kernel32')
    # handle = kernel32.GetStdHandle(-11)
    # handle1 = win32gui.GetForegroundWindow()
    # handle2 = ctypes.windll.user32.GetForegroundWindow()
    # print("HANDLE 0:", handle)
    # print("HANDLE 1:", handle1)
    # print("HANDLE 2:", handle2)
    #win32gui.MessageBox(None, str(HANDLE), str(HANDLE), 0)
    # handle = HANDLE
    # if not handle:
    #     handle = win32gui.GetForegroundWindow()
    # handle = win32gui.GetForegroundWindow()
    #handle1 = handle = win32gui.GetForegroundWindow()
    # print("HANDLE:", HANDLE)
    if HANDLE:
        # win32gui.ShowWindow(HANDLE, win32con.SW_RESTORE)
        # win32gui.SetForegroundWindow(HANDLE)
        # win32gui.BringWindowToTop(HANDLE)
        ctypes.windll.user32.SetForegroundWindow(HANDLE)
    
    #win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, 0)
    
    #win32gui.SetForegroundWindow(handle)

    #win32gui.ShowWindow(handle1,9)
    #win32gui.SetForegroundWindow(handle1)
    #win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, None, None, None, None, 0)

def cleanup(filename):
    import shutil
    from datetime import datetime
    
    file_dir = os.path.dirname(filename)
    file_name = os.path.basename(filename)
    file_ext = os.path.splitext(file_name)
    ext = ''
    if len(file_ext) == 2:
        ext = file_ext[1]

    shutil.copyfile(filename, os.path.join(file_dir, file_ext[0] + "_" + datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S%f') + ext))

    data = ''
    fileout = ''
    fileout1 = ''
    if sys.version_info.major == 2:
        with open(filename, 'rb') as f:
            data = f.readlines()
    else:
        with open(filename, 'r') as f:
            data = f.readlines()
    datax = ""
    for i in data:
        if not re.findall('debug\(.*?\).*?\n', i):
            datax += i
    
    if len(file_ext) == 2:
        file_ext = file_ext[1]
    else:
        file_ext = ""
    if not "_debug" in file_name:
        fileout = os.path.join(file_dir, os.path.splitext(file_name)[0] + "_release" + ext)
        fileout1 = filename.replace("_debug", "")
    else:
        fileout = filename.replace("_debug", "")
    print("FILENAME:", filename)
    print("FILEOUT :", fileout)

    if sys.version_info.major == 2:
        with open(fileout, 'wb') as f:
            data = f.write(datax)
        if fileout1:
            with open(fileout1, 'wb') as f:
                data = f.write(datax)
    else:
        with open(fileout, 'w') as f:
            data = f.write(datax)
        if fileout1:
            with open(fileout, 'w') as f:
                data = f.write(datax)
    if not "_debug" in file_name:
        shutil.copyfile(filename, os.path.join(file_dir, os.path.splitext(file_name)[0] + "_debug" + ext))

def usage():
    if not __name__ == '__main__':
        global HANDLE
        # import win32gui, win32con
        if sys.platform == 'win32':
            kernel32 = ctypes.WinDLL('kernel32')
            # handle = kernel32.GetStdHandle(-11)
            # handle1 = win32gui.GetForegroundWindow()
            handle2 = ctypes.windll.user32.GetForegroundWindow()
            HANDLE = handle2
    # print("HANDLE 3:", handle)
    # print("HANDLE 4:", handle1)
    # print("HANDLE 5:", handle2)
    import argparse
    parser = argparse.ArgumentParser(description= 'run debugger as server receive debug text default port is 50001', formatter_class= argparse.RawTextHelpFormatter)
    parser.add_argument('-b', '--host', action = 'store', help = 'Bind / listen ip address, default all network device: 0.0.0.0', default = '0.0.0.0', type = str)
    parser.add_argument('-p', '--port', action = 'store', help = 'Bind / listen port number, default is 50001', default = 50001, type = int)
    parser.add_argument('-a', '--on-top', action = 'store_true', help = 'Always On Top')
    parser.add_argument('-C', '--center', action = 'store_true', help = 'Centering window')
    parser.add_argument('-c', '--cleanup', action = 'store', help = 'CleanUp File')
    if len(sys.argv) == 1:
        print("\n")
        parser.print_help()
        try:
            args = parser.parse_args()
            serve(args.host, args.port, args.on_top, args.center)
        except KeyboardInterrupt:
            sys.exit()
    else:
        args = parser.parse_args()
        if args.cleanup:
            cleanup(args.cleanup)
        else:
            try:
                serve(args.host, args.port, args.on_top, args.center)
            except KeyboardInterrupt:
                sys.exit()

if __name__ == '__main__':
    if sys.platform == 'win32':
        kernel32 = ctypes.WinDLL('kernel32')
        handle2 = ctypes.windll.user32.GetForegroundWindow()
        HANDLE = handle2
    print("PID:", PID)
    if sys.platform == 'win32':
        print("HANDLE:", HANDLE)
    usage()
