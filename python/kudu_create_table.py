from ddlparse.ddlparse import DdlParse
from xml.etree.ElementTree import Element,ElementTree,dump
import re
import threading, requests, time

p = re.compile('[a-z|_.,\(\)|0-9|\"]+')
pk_list = re.compile('[a-z]]+')

src_file = "I:\\git\\source\\python\\sql.txt"
tar_file = "I:\\git\\source\\python\\{tb}.txt"
tar_file_2 = "I:\\git\\source\\python\\{tb}.xml"

result = []
table_name = ""
pk_key = ""
kudu_create_ddl = """
"""

kudu_end_line_sql = """PARTITION BY HASH ( {pk} ) PARTITIONS {hash_cnt}
STORED AS KUDU
TBLPROPERTIES (
    'kudu.master_addresses' = 'test1.com,test2.com,test3.com'
);
"""

sample_ddl = """
CREATE TABLE My_Schema.Sample_Table (
  Id integer PRIMARY KEY COMMENT 'User ID',
  Name varchar(100) NOT NULL COMMENT 'User name',
  Total bigint NOT NULL,
  Avg decimal(5,1) NOT NULL,
  Created_At date, -- Oracle 'DATE' -> BigQuery 'DATETIME'
  UNIQUE (NAME)
);
"""



def sample_ddlParse():
    #table = DdlParse().parse(sample_ddl)
    #table = DdlParse().parse(ddl=sample_ddl, source_database=DdlParse.DATABASE.oracle)
    parser = DdlParse(sample_ddl)
    table = parser.parse()

    #print("* BigQuery Fields * : normal")
    #print(table.to_bigquery_fields())

    print("* BigQuery Fields - column name to lower case / upper case *")
    print(table.to_bigquery_fields(DdlParse.NAME_CASE.lower))
    print(table.to_bigquery_fields(DdlParse.NAME_CASE.upper))

    
    print("* COLUMN *")
    for col in table.columns.values():
        print("name = {} : data_type = {} : length = {} : precision(=length) = {} : scale = {} : constraint = {} : not_null =  {} : PK =  {} : unique =  {} : BQ {}".format(
            col.name,
            col.data_type,
            col.length,
            col.precision,
            col.scale,
            col.constraint,
            col.not_null,
            col.primary_key,
            col.unique,
            col.to_bigquery_field()
            ))

    print("* Get Column object (case insensitive) *")
    print(table.columns["total"])

def read_file(val):
    global kudu_create_ddl
    global table_name
    global pk_key
    
    f = open(src_file, 'r')  
    lines = f.readlines()
    count = len(lines)

    print('total_lines :', count)

    for line in lines:
        result = p.findall(line.lower())        
        #print(line.lower())
        #result = line.lower().split(' ')
        if line.lower().find('primary') > -1:            
            arr_str = re.findall('\(([^)]+)', line.lower())
            for s in arr_str:
                pk_key = s
                print('s :', s)
            #print(pk_key) 
            #print('pk_key : {0}'.format(pk_key))

        for res in result:
            chg_str = res.replace("\"","`")
            
            if chg_str.find('.') > -1:              
                table_name = chg_str

            if chg_str.find('varchar') > -1 or chg_str.find('timestamp') > -1:                
                kudu_create_ddl += 'string '
            elif chg_str.find('numeric') > -1:
                kudu_create_ddl += 'double '
            else:
                kudu_create_ddl += str(chg_str) + ' '
       
        kudu_create_ddl += '\n'
        #print(result)
        
    f.close()

    kudu_create_ddl += kudu_end_line_sql.format(pk=pk_key, hash_cnt=val)

    #print(result)
   
def write_file():
      f = open(tar_file.format(tb=table_name), 'w')
      f.write(kudu_create_ddl)
      f.close()


def xml_write_file():
    root = Element("schema", kind="hive")
    node1 = Element("table")
    node1.text = "hive"
    root.append(node1)
    node2 = Element("colums")
    node2.text = "fab"
    root.append(node2)
    indent(root)
    dump(root)

    #tree = Element()    
    #tree.parse(root)
    ElementTree(root).write(tar_file_2.format(tb='ipa.u_prod_oper'), encoding="utf-8", xml_declaration=True)

def indent(elem, level=0): 
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def getHtml(url):
    resp = requests.get(url)
    time.sleep(1)
    print(url, len(resp.text), 'chars')

class Member:
    name = ""

    def __init__(self, str): 
        self.name = str

    def showMsg(self):
        print(self.name)

class PowerMember(Member):
    mail = ""

    def __init__(self, str1, str2): 
        self.name = str1
        self.mail = str2

    def showMsg(self):
        print(self.name)
        print(self.mail)        

class HtmlGetter (threading.Thread):    
    def __init__(self, url):
        threading.Thread.__init__(self) 
        self.url = url
 
    def run(self):
        resp = requests.get(self.url)
        time.sleep(1)
        print(self.url, len(resp.text), 'chars')

if __name__ == "__main__":
    read_file(32)
    #print(kudu_end_line_sql.format(pk='fab, oper, prod', hash_cnt=32))
    #sample_ddlParse()
   
    #print(kudu_create_ddl)
    #print(table_name)
    #print(pk_key)
    
    write_file()

    #xml_write_file()

    '''
    iu = Member("IU")    
    iu.showMsg()

    han = PowerMember("Han", "han@flower.com")    
    han.showMsg()

    t1 = threading.Thread(target=getHtml, args=('http://google.com',))
    t1.start()

    t = HtmlGetter('http://google.com')
    t.start()

    t2 = threading.Thread(target=getHtml, args=('http://google.com',))
    t2.daemon = True 
    t2.start()
 
    print("### End ###")
    '''
    
    



