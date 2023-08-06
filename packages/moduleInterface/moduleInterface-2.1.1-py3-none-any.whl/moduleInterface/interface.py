# -*- coding: utf-8 -*-

#!/usr/bin/python3

from abc import *
import pandas as pd
import json
from collections import OrderedDict

class ModuleComponentInterface(metaclass=ABCMeta):
    def __init__(self):
        self.__status   = 0
        self.fHandle    = 0
        self.attrib     = OrderedDict({
            "name"       :"default",
            "author"     :"you",
            "ver"        :"0.0",
            "id"         :0,
            "param"      :"None",
            "encode"     :"utf-8",
            "base"       :0,
            "last"       :0,
            "excl"       :False,
            "save_result":False,
            "result"     :None,
            "flag"       :0
        })

    def __del__(self):
        pass

    @property
    def errno(self):
        return self.__status

    @property
    def id(self):
        return self.get_attrib("id",0)

    def status(self,status):
        if(type(status)==int):
            self.__status = status

    def update_attrib(self,key,value):      # 모듈 속성 업데이트
        self.attrib.update({key:value})

    def cat_attrib(self):                   # 모듈 속성 보기
        return json.dumps(self.attrib)

    @abstractmethod
    def module_open(self,id=2):             # Reserved method for multiprocessing
        self.__status = 0
        self.attrib.update({"id":int(id)})
    @abstractmethod
    def module_close(self):                 # Reserved method for multiprocessing
        pass
    @abstractmethod
    def set_attrib(self,key,value):         # 모듈 호출자가 모듈 속성 변경/추가하는 method interface
        self.update_attrib(key,value)
    @abstractmethod
    def get_attrib(self,key,value=None):    # 모듈 호출자가 모듈 속성 획득하는 method interface
        return self.attrib.get(key)
    @abstractmethod
    def execute(self,cmd=None,option=None): # 모듈 호출자가 모듈을 실행하는 method
        pass


class MemFrameTool(object):
    @staticmethod
    def read_csv(csv,encoding='utf-8',error=False):
        return pd.read_csv(csv,encoding=encoding,error_bad_lines=error).drop_duplicates()

    @staticmethod
    def read_xlsx(xlsx,sheet):
        return pd.read_excel(xlsx,sheet).drop_duplicates()

    @staticmethod
    def select_columms(df,columns):
        try:return pd.DataFrame(df,columns=columns)
        except:return None

    @staticmethod
    def filter(df,condition):
        return df.loc[condition]

    @staticmethod
    def contains(df,column,contained,boolean):
        return df[df[str(column)].astype(str).str.contains(str(contained))==bool(boolean)]

    @staticmethod
    def drops(df,*args):
        columns = list()
        for i in args:columns.append(i)
        df.dropna(subset=columns)
    
    @staticmethod
    def drop(df,column,v,op="equal"):
        if(op.lower()=="equal"):
            df = MemFrameTool.filter(df,(df[column]==v))
        elif(op.lower()=="unequal"):
            df = MemFrameTool.filter(df,(df[column]!=v))
        elif(op.lower()=="less"):
            df = MemFrameTool.filter(df,(df[column]<v))
        elif(op.lower()=="more"):
            df = MemFrameTool.filter(df,(df[column]>v))
        return df