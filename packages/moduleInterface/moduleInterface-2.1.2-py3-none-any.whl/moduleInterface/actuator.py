from . import defines
from . import interface

import os,sys
import signal
import argparse
import importlib
from multiprocessing import Process

# Author : Gibartes

class Actuator(object):
    def __init__(self):
        self.id = defines.ModuleID.ACTUATOR
        self.init()

    def __del__(self):
        self.clear()

    def __str__(self):
        return (defines.ModuleID.ACTUATOR,
                "Module Component {0}".format(self.__class__.__name__))

    @property
    def author(self):
        return "Gibartes"

    # <--------------------------------
    # @ Module Executor
    def open(self,key,id,value):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            self.errno = defines.FLAG.NO_SUCH_OBJECT
            return False
        self.errno = defines.FLAG.SUCCESS
        return obj.module_open(id,value)

    def getObject(self,key):
        return self.__objectTbl.get(key)

    def close(self,key,id,value):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            self.errno = defines.FLAG.NO_SUCH_OBJECT
            return False
        self.errno = defines.FLAG.SUCCESS
        return obj.module_close(id)

    # Get (a) module parameter(s)
    def get(self,key,attr):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            self.errno = defines.FLAG.NO_SUCH_OBJECT
            return False
        self.errno = defines.FLAG.SUCCESS
        return obj.get_attrib(attr)

    # Set (a) module parameter(s)
    def set(self,key,attr,value):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            self.errno = defines.FLAG.NO_SUCH_OBJECT
            return False
        self.errno = defines.FLAG.SUCCESS
        obj.set_attrib(attr,value)
        return True

    # Start Activity
    def call(self,key,cmd,option,mode=defines.FLAG.SAFELY_HANDLED):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            self.errno = defines.FLAG.NO_SUCH_OBJECT
            return None
        if(mode==defines.FLAG.UNSAFELY_HANDLED):
            return obj.execute(cmd,option)
        elif(mode==defines.FLAG.SAFELY_HANDLED):
            try:
                result = obj.execute(cmd,option)
                self.errno = defines.FLAG.SUCCESS
                return result
            except:
                self.errno = defines.FLAG.FAIL
                return None

    def fork(self,key,cmd,option,mode=defines.FLAG.SAFELY_HANDLED):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            self.errno = defines.FLAG.NO_SUCH_OBJECT
            return None
        if(mode==defines.FLAG.UNSAFELY_HANDLED):
            proc = Process(target=obj.execute,args=(cmd,option))
            proc.start()
            return True
        elif(mode==defines.FLAG.SAFELY_HANDLED):
            try:
                proc = Process(target=obj.execute,args=(cmd,option))
                proc.start()
                self.errno = defines.FLAG.SUCCESS
                return True
            except:
                self.errno = defines.FLAG.FAIL
                return None

    # Wrapper functions
    def module_open(self,key,id,value):
        return self.open(key,id,value)
    def module_close(self,key,id,value):
        return self.close(key,id,value)
    def set_attrib(self,key,value):
        return self.get(key,value)
    def get_attrib(self,key,value=None):
        return self.set(key,key,value)
    def execute(self,key,cmd,option):
        return self.call(key,cmd,option)

    # -------------------------------->

    # <--------------------------------
    # @ Module Loader
    def init(self):
        self.__objectTbl = {}
        self.__importTbl = {}
        self.errno       = 0

    def clear(self):
        keylist = self.__objectTbl.copy().keys()
        for k in keylist:
            self.__unloadObject(k)

        keylist = self.__importTbl.copy().keys()
        for k in keylist:
            self.unloadModule(k)
        
    # Load/Unload a python package
    def loadModule(self,module):
        try:
            tmp = importlib.import_module(module)
            if(self.__importTbl.get(module,None)==None):
                self.__importTbl.update({module:tmp})
                self.errno = defines.FLAG.SUCCESS
                return tmp
            self.errno = defines.FLAG.ALREADY_LOADED
            return None
        except:
            self.errno = defines.FLAG.IS_NOT_REGULAR
            return None

    def loadModuleAs(self,module,alias):
        try:
            tmp = importlib.import_module(module)
            if(self.__importTbl.get(alias,None)==None):
                self.__importTbl.update({alias:tmp})
                self.errno = defines.FLAG.SUCCESS
                return tmp
            self.errno = defines.FLAG.ALREADY_LOADED
            return None
        except:
            self.errno = defines.FLAG.IS_NOT_REGULAR
            return None    

    def unloadModule(self,module):
        tmp = self.__importTbl.pop(module,None)
        if(tmp!=None):
            try:
                importlib.reload(tmp)
                del tmp
            except:
                self.errno = defines.FLAG.NO_SUCH_OBJECT
            return
        self.errno = defines.FLAG.SUCCESS

    def getModuleHandle(self,module):
        return self.__importTbl.get(module,None)

    # Load/unload a class
    def __loadObject(self,name,obj,force=False):
        if(force==True):
            self.__unloadObject(name)
            self.__objectTbl.update({name:obj})
            self.errno = defines.FLAG.SUCCESS
            return True
        if(self.__objectTbl.get(name,None)==None):
            self.__objectTbl.update({name:obj})
            self.errno = defines.FLAG.SUCCESS
            return True
        try:del obj
        except:pass
        self.errno = defines.FLAG.ALREADY_LOADED
        return False

    def __unloadObject(self,name):
        tmp = self.__objectTbl.pop(name,None)
        if(tmp!=None):
            try:del tmp
            except:pass
            self.errno = defines.FLAG.SUCCESS
            return
        self.errno = defines.FLAG.NO_SUCH_OBJECT
        return tmp

    # Check
    def checkModuleLoaded(self,module):
        return (True if module in self.__importTbl.keys() else False)

    def getLoadedModuleList(self):
        return self.__importTbl.copy().keys()

    def checkObjectLoaded(self,name):
        return (True if name in self.__objectTbl.keys() else False)

    def getLoadedObjectList(self):
        return self.__objectTbl.copy().keys()

    # load("module_name","class_name")
    def load(self,module,cls):
        if(self.checkModuleLoaded(module)==False):
            if(self.loadModule(module)==None):
                self.errno = defines.FLAG.IS_NOT_REGULAR
                return None
        try:
            ClassObject = getattr(self.getModuleHandle(module),cls)
            Object      = ClassObject()
            if(isinstance(Object,interface.ModuleComponentInterface)):
                return self.__loadObject(module,Object)
            self.errno = defines.FLAG.IS_NOT_INSTANCE
            return False
        except:
            self.errno = defines.FLAG.IS_NOT_REGULAR
            return False

    # loadClass("module_name","class_name","class_name_alias")
    def loadClass(self,module,cls,alias=None,force=False):
        if(self.checkModuleLoaded(module)==False):
            self.errno = defines.FLAG.NO_SUCH_MODULE
            return False
        try:
            ClassObject = getattr(self.getModuleHandle(module),cls)
            Object      = ClassObject()
            if(isinstance(Object,interface.ModuleComponentInterface)):
                if(alias==None):
                    return self.__loadObject(module,Object,force)
                else:
                    return self.__loadObject(alias,Object,force)
            self.errno = defines.FLAG.IS_NOT_INSTANCE
            return False
        except:
            self.errno = defines.FLAG.IS_NOT_REGULAR
            return False

    # unloadClass("class_name_alias")
    def unloadClass(self,name):
        return self.__unloadObject(name)

    # loadLibrary("module_name")
    def loadLibrary(self,module):
        if(self.checkModuleLoaded(module)==False):
            if(self.loadModule(module)==None):
                return None
            return True
        return False

    # loadLibraryAs("module_name","namespace")
    def loadLibraryAs(self,module,alias):
        if(self.checkModuleLoaded(alias)==True):
            return False
        if(self.checkModuleLoaded(module)==False):
            if(self.loadModuleAs(module,alias)==None):
                return None
            return True
        return False

    # unloadLibrary("module_name")
    def unloadLibrary(self,module):
        if(self.checkModuleLoaded(module)==False):
            return False
        return self.unloadModule(module)

    # loadModuleClassAs("module_name","class_name","namespace","class_alias")
    def loadModuleClassAs(self,module,cls,mod_alias=None,cls_alias=None,force=False):
        if(mod_alias!=None):
            self.loadLibraryAs(module,mod_alias)
            return self.loadClass(mod_alias,cls,cls_alias,force)
        else:
            self.loadLibrary(module)
            return self.loadClass(module,cls,cls_alias,force)

    # -------------------------------->


if __name__ == '__main__':

    def signal_handler(signal,frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # python .\actuator.py -t module_bmp -f '.\sample\img.bmp' -i module_bmp -c ModuleBMP
    mod    = Actuator()
    parser = argparse.ArgumentParser(description="select run mode")
    parser.add_argument("-t",action="store",dest="target",type=str,default='n',     required=True)
    parser.add_argument("-f",action="store",dest="file",type=str,default='n',       required=True)
    parser.add_argument("-e",action="store",dest="encode",type=str,default='euc-kr',required=False)
    parser.add_argument("-b",action="store",dest="block",type=int,default=1024,     required=False)
    parser.add_argument("-from",action="store",dest="start",type=int,default=0,     required=False)
    parser.add_argument("-to",action="store",dest="end",type=int,default=0,         required=False)
    parser.add_argument("-cmd",action="store",dest="cmd",type=str,default=None,     required=False)
    parser.add_argument("-opt",action="store",dest="option",type=bool,default=True, required=False)
    parser.add_argument("-i",action="store",dest="lib",type=str,default=None,       required=False)
    parser.add_argument("-c",action="store",dest="cls",type=str,default=None,       required=False)

    args = parser.parse_args()

    _request  = args.target
    _file     = args.file
    _encode   = args.encode
    _base     = args.start
    _last     = args.end
    _block    = args.block
    _cmd      = args.cmd
    _opt      = args.option
    _lib      = args.lib
    _cls      = args.cls

    if(_block<=0):
        print("[!] Error")
        sys.exit(0)
    
    if(_lib!=None and _cls!=None):
        mod.load(_lib,_cls)

    if(_request not in mod.getLoadedObjectList()):
        print("[!] Unsupport type")
        sys.exit(0)

    print("[*] Start to verify type of the file.")

    mod.set(_request,defines.ModuleConstant.FILE_ATTRIBUTE,_file)          # File to carve
    mod.set(_request,defines.ModuleConstant.IMAGE_BASE,_base)              # Set start offset of the file base
    mod.set(_request,defines.ModuleConstant.IMAGE_LAST,_last)              # Set last offset of the file base
    mod.set(_request,defines.ModuleConstant.ENCODE,_encode)                # Set encode type
    mod.set(_request,defines.ModuleConstant.CLUSTER_SIZE,_block)           # Set cluster size

    cret = mod.call(_request,_cmd,_opt)

    print("[*] Result :\n(Start offset, Valid size, Record Type)")
    print(cret)

    sys.exit(0)
