import pymysql
import numpy as np
import pandas as pd
import sys
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio
import sklearn


class objectMySQL:
    '''
    用于对mysql数据库进行各种操作，包括：\n
    ①创建table，create table if not exists ...\n
    ②新增column（单），alter table ... add column ...\n
    ③新增row（单），insert into ... value ...\n
    ④更新value（单），update ... set ... = ...\n
    ⑤查询select，select ... from ... where ...\n
    【参数】\n
    dataBaseName=dbname\n
    数据库参数(缺省值，可自定义)包括：\n
    db_host = 'localhost'\n
    db_port = 3306\n
    db_user = 'root'\n
    db_password = '000000'\n
    charset='utf8mb4'\n
    '''
    def __init__(self, dataBaseName, **kwargs):
        self.dataBaseName = dataBaseName
        host = kwargs["db_host"] if kwargs["db_host"] else 'localhost'
        port = kwargs["db_port"] if kwargs["db_port"] else 3306
        userName = kwargs["db_user"] if kwargs["db_user"] else 'root'
        userPin = kwargs["db_password"] if kwargs["db_password"] else '000000'
        self.__con__ = pymysql.connect(host=host, port=port, db=self.dataBaseName, user=userName, passwd=userPin, charset='utf8mb4')
        self.__cur__ = self.__con__.cursor()

    def createTable(self, **kwargs):
        '''
        :param kwargs: tableName：表单名；columns：列名+数据类型+缺省控制，字符串形如'test01 float null'
        :return: None
        '''
        self.__cur__.execute('create table if not exists ' + kwargs['tbname'] + '(' + kwargs['columns'] + ')')
        self.__cur__.close()
        self.__con__.close()

    def addColumn(self, **kwargs):
        '''
        :param kwargs: tableName：表单名；column：初始列名、数据类型、缺省值，字符串形如'test02 float null'
        :return: None
        '''
        self.__cur__.execute('alter table ' + self.dataBaseName + '.' + kwargs['tbname'] + ' add column ' + kwargs['column'])
        self.__cur__.close()
        self.__con__.close()

    def insertRow(self, **kwargs):
        '''
        :param kwargs: tableName：表单名；values：新增值，字符串形如'510, 512'
        :return: None
        '''
        self.__cur__.execute('insert into ' + kwargs['tbname'] + ' value ' + '(' + kwargs['values'] + ')')
        self.__cur__.close()
        self.__con__.close()

    def updateValue(self, **kwargs):
        '''
        :param kwargs: tableName：表单名；targetColumn：更新列名，字符串形如'test02'；value：更新值，字符串形如'110'
        :return: None
        '''
        com = 'update ' + self.dataBaseName + '.' + kwargs['tbname'] + ' set ' + kwargs['targetColumn'] + '=' + kwargs['value']
        self.__cur__.execute(com)
        self.__cur__.close()
        self.__con__.close()

    def selectData(self, **kwargs):
        '''
        :param kwargs: tableName：表单名；content：输出的内容，字符串形如'*'或'test01'；condition：[可无]条件，字符串形如'test01=510'
        :return: None
        '''
        if kwargs['condition']:
            com = 'select ' + kwargs['content'] + ' from ' + self.dataBaseName + '.' + kwargs['tbname'] + ' where ' + kwargs['condition']
        else:
            com = 'select ' + kwargs['content'] + ' from ' + self.dataBaseName + '.' + kwargs['tbname']
        self.__cur__.execute(com)
        res = self.__cur__.fetchall()
        self.__cur__.close()
        self.__con__.close()
        return res
