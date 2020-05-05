from select_query_list import selQueryList
from readSqlFile import readSqlFile
from xmlTalendFile import xmlTalendFile
from jsonConfigFileManager import jsonConfigFileManager as jm

import os
import re

spare = "\\"

conf = jm(os.path.dirname(os.path.realpath(__file__)) + spare + 'config.json')
hs_file = os.path.dirname(os.path.realpath(__file__)) + spare + conf.values.hash
src_file = os.path.dirname(os.path.realpath(__file__)) + spare + conf.values.src

kudu_ddl_path = os.path.dirname(os.path.realpath(__file__)) + spare + conf.values.tar.no1
csv_ddl_path = os.path.dirname(os.path.realpath(__file__)) + spare + conf.values.tar.no2
sel_ddl_path = os.path.dirname(os.path.realpath(__file__)) + spare + conf.values.tar.no3


if __name__ == "__main__":
    print("##### Main Start #####");

   
    ''' sucess        '''
    # talend xml file create
    print("##### file read changing to xml #####")
    xl = xmlTalendFile(src_file, conf.values.db_info)
    xl.readFile() 
    xl.showMsg()
    
    # kudu, csv, select Sql list
    print("##### file read changing to kudu, csv, sel #####")
    ddl = readSqlFile(hs_file, src_file, conf.values.hdfs_uri, kudu_ddl_path, csv_ddl_path)    
    ddl.read_hash_file()
    ddl.read_file()
    ddl.showMsg() 

    # select query list
    sel = selQueryList(src_file, sel_ddl_path)
    sel.read_query()
    sel.showMsg()    

