"""
The default attribute of module :
    "name"   :"default",            # Module 이름
    "author" :"Gibartes",           # Module 제작자
    "ver"    :"0.0",                # Module 버젼
    "param"  :None,                 # Module 파라미터
    "encode" :"utf-8",              # Module 인코딩
    "base"   :0                     # File image base to carve

"""
import os, copy

# 정적 설정
# 동적인 설정은 ModuleConfiguration을 이용하여 config.txt에 기록!
# --> module_config.py

class ModuleConstant(object):
    # System Environment
    LIB_DEFAULT_PATH = "/usr/local/lib/"
    DEFINE_PATH      = os.path.abspath(os.path.dirname(__file__))+os.sep

    # Module Attribute
    NAME             = "name"
    AUTHOR           = "author"
    VERSION          = "ver"
    ID               = "id"
    PARAMETER        = "param"
    ENCODE           = "encode"
    FILE_ATTRIBUTE   = "file"
    IMAGE_BASE       = "base"
    IMAGE_LAST       = "last"
    EXCLUSIVE        = "excl"
    CLUSTER_SIZE     = "cluster"
    SECTOR_SIZE      = "sector"
    RETURN_SET       = "save_result"
    LAST_RETURN      = "result"
    FLAGS            = "flag"
    ARGUMENT         = "argument"
    CLASS_NAME       = "@class"
    CALL_SIGN        = "@callsign"
    CUSTOM_ATTRIBUTE = "@custom"
    FIRST_INPUT      = "@input"

    INDEX            = "index"
    FEATURE          = "features"
    LABEL            = "label"

    # Management Control
    LOAD_MODULE      = "load_module"
    UNLOAD_MODULE    = "unload_module"
    CONNECT_DB       = "connect_db"
    CREATE_DB        = "create_db"
    DISCONNECT_DB    = "disconnect_db"
    EXEC             = "exec"

    # Confiugration Operations
    COLLABORATE      = 6
    CONFIG_FILE      = "config.txt"
    INIT             = 0b00000000
    READ             = 0b00000001
    WRITE            = 0b00000010
    CREATE           = 0b00000100
    DELETE           = 0b00001000
    SAVE             = 0b00010000
    GETALL           = 0b00100000
    DESCRIPTION      = 0b01000000

    # Error
    class Return(object):
        SUCCESS          = 0    # 성공
        EINVAL_ATTRIBUTE = -1   # Invalid attribute
        EINVAL_FILE      = -2   # Invalid file input
        EINVAL_TYPE      = -3   # Invalid data type
        EINVAL_NONE      = -4   # Nothing to getw

    # Dependency List (Static)
    class Dependency(object):
        pecarve          = "pecarve"

class FLAG(object):
    SAFELY_HANDLED      = False
    UNSAFELY_HANDLED    = True
    SUCCESS             = 0
    FAIL                = -1
    IS_NOT_INSTANCE     = -2
    ALREADY_LOADED      = -3
    NO_SUCH_OBJECT      = -4
    IS_NOT_REGULAR      = -5
    NO_SUCH_MODULE      = -6

class ModuleID(object):
    UNALLOC          = 0x0000
    ACTUATOR         = 0x0001
    INIT             = 0X0002
    RESERVED         = 0xFFFF

class Offset_Info(object):
    NONE      = 0b00000000
    VALID     = 0b00000001
    MERGEABLE = 0b00000010
    ERROR     = 0b00000100
    UNKNWON   = 0b00001000
    UNIT      = 0b00010000
    GROUPABLE = 0b00100000
    EXTRACTED = 0b10000000

    def __init__(self):
        self.name        =  ""   # signature alias
        self.signature   = ""   # signatures in C_defy.SIGNATURE
        self.attribute   = None # static attribute which is not cleared.
        self.__contents  = list()
        self.__hcontents = dict()
        self.size        = 0
        self.flag        = None

    def append(self,start,end,flag):
        self.__contents.append([start,end,flag])
        self.size   += abs(end-start)
    
    def insert(self,*v):
        self.__contents.append(list(v))

    def update(self,key,value):
        self.__hcontents.update({key:value})

    def clear(self):
        self.__contents  = list()
        self.__hcontents = dict()
        self.size        = 0
        self.flag        = None

    def header(self):
        if(len(self.__contents)>0):
            return tuple(self.__contents[0])
        return (-1,-1,-1)

    @property
    def contents(self):
        return self.__contents

    @contents.setter
    def contents(self,contents):
        self.__contents = contents
