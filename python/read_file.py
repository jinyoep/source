import re, os
from xml.etree.ElementTree import Element,ElementTree,dump
import xml.etree.ElementTree as ET

hs_file = os.path.dirname(os.path.realpath(__file__)) + '/hash_size.txt'
sorce_file = os.path.dirname(os.path.realpath(__file__)) + '/sql.txt'
target_kudu_file = os.path.dirname(os.path.realpath(__file__)) + '/kudu_list.txt'
target_hive_csv_file = os.path.dirname(os.path.realpath(__file__)) + '/hive_csv_list.txt'
target_select_sql_file = os.path.dirname(os.path.realpath(__file__)) + '/select_query_list.txt'

pattern = re.compile('[a-z|_.,\(\)|0-9|\"|;]+')

# Table list
table_list = []

# Column list
column_list = [[]]
sorted_column_list = []

# Type list
type_list = [[]]
sorted_type_list = []

# Type list
nullable_list = [[]]
sorted_nullable_list = []

# Type len list
type_len_list = [[]]
sorted_type_len_list = []

# Table Pk
pk_key = [[]]

# Table Count
t_cnt = 0

# File Write Count
write_cnt = 0

# Changed Query
total_sel_sql = ""
total_hive_csv_sql = ""
total_kudu_sql = ""

# kudu hash size
kudu_hash_size = []

# list arr add
def arr_list_append():
    column_list.append([])
    type_list.append([])
    type_len_list.append([])
    nullable_list.append([])
    pk_key.append([])

def arr_sort_list_append():
    sorted_column_list.append([])
    sorted_type_list.append([])
    sorted_nullable_list.append([])
    sorted_type_len_list.append([])    

# Sort for pk
def pkSorting():
    print("##### VALUE SORTING START")

    r_cnt = 0
    for t in table_list:

        if r_cnt < t_cnt:
            arr_sort_list_append()


        for pkey in pk_key[r_cnt]:
            col_no = 0       
            for colum in column_list[r_cnt]:
                if colum ==  pkey:
                    sorted_column_list[r_cnt].append(colum)
                    if type_list[r_cnt][col_no].find("double") > -1:
                        sorted_type_list[r_cnt].append("integer")    
                    else :    
                        sorted_type_list[r_cnt].append(type_list[r_cnt][col_no])

                    sorted_nullable_list[r_cnt].append(nullable_list[r_cnt][col_no])
                    sorted_type_len_list[r_cnt].append(type_len_list[r_cnt][col_no])
                col_no += 1

        pk_not_col_no = 0            
        for colum in column_list[r_cnt]:
            if colum not in pk_key[r_cnt]:
                sorted_column_list[r_cnt].append(colum)    
                sorted_type_list[r_cnt].append(type_list[r_cnt][pk_not_col_no])
                sorted_nullable_list[r_cnt].append(nullable_list[r_cnt][pk_not_col_no])
                sorted_type_len_list[r_cnt].append(type_len_list[r_cnt][pk_not_col_no])
            pk_not_col_no += 1

        r_cnt += 1
 
    print("##### VALUE SORTING END")           


def read_file():
    print("##### READ FILE START")

    global t_cnt

    with open(sorce_file, 'r') as f:
        lines = f.readlines()

        for t in lines:
            if ');' in t:
                t_cnt += 1

        c_row = 0 
        for line in lines:
            result = pattern.findall(line.lower())            
            #print(result)

            if line.lower().find('primary') > -1:            
                arr_str = re.findall('\(([^)]+)', line.lower())
                for s in arr_str:
                    arr_temp = s.split(',')
                    #print(arr_temp)
                    for arr in arr_temp:
                        pk_key[c_row].append(arr.strip())            
                    
            
            col_cnt = 0
            if 'create' in result:                
                for word in result:
                    if col_cnt == 2:
                        table_list.append(word)
                    col_cnt += 1            
            else:
                #print(len(result))                              
                for word in result:                   

                    if col_cnt == 0:
                        if word.find('constraint') > -1:
                            if (t_cnt-1) > c_row:
                                arr_list_append() # 배열 추가                               
                                c_row += 1 
                        else :    
                            if word not in ');':
                                column_list[c_row].append(word.replace("\"","`"))
                    elif col_cnt == 1:
                        if word.find('pk') < 0:
                            type_list[c_row].append(re.sub('[0-9|\(\)|,]+', '', word.replace("\"","`")))
                            type_len_list[c_row].append(re.sub('[a-z|\(\)|,]+','',word))
                    elif col_cnt == 2:
                        if word.find('not') > -1:
                            nullable_list[c_row].append("not null")
                        else:
                            if word not in 'primary':
                                nullable_list[c_row].append("null")
                    col_cnt += 1

                if len(result) == 2:
                    nullable_list[c_row].append("null")
    print("##### READ FILE END")

def table_rename(nm):
    chg_nm = "ipa." + nm.replace(".", "_")
    return chg_nm

def sql_sel_complete():
    global total_sel_sql
    global total_kudu_sql

    select_frist = "SELECT "
    select_from = "\nFROM "
    select_end = "\n;\n\n"
    select_columns = ""
    table_name = ""  

    kudu_create_str = "CREATE TABLE {table_nm} (\n"
    kudu_colum_str = ""
    kudu_pkey_str = "primary key ( {pk_list} )\n" 
    kudu_end_str = ");\n\n"
    kudu_sql_str = ""

    line_enter_no = 5  
    line_enter_plus = 1
    row_cnt = 0    
    total_col_cnt = 0

    sel_sql = ""

    for t_nm in table_list:

        total_col_cnt = len(sorted_column_list[row_cnt])
        col_cnt = 0
        for column in sorted_column_list[row_cnt]:
            if col_cnt >= (line_enter_no-1):
                if col_cnt%((line_enter_no-1)+line_enter_plus) == 0:
                    if col_cnt < (total_col_cnt-1) :
                        select_columns  += "\n"
                        line_enter_plus += line_enter_no

            select_columns += column 
            if col_cnt < (total_col_cnt-1) :
                select_columns  += ", "
            else:
                select_columns  += " " 
                
                table_name = table_rename(t_nm) 
                sel_sql = select_frist + select_columns + select_from + table_name + select_end                       
                select_columns = ""
                line_enter_plus = 1
                print(sel_sql)

            col_cnt += 1
        total_sel_sql += sel_sql
        row_cnt += 1    
    print(total_sel_sql) 

def read_hash_file():
    global kudu_hash_size

    with open(hs_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            #print(line)
            kudu_hash_size = line.split(',')
            print("##### KUDU Hash Size : ", kudu_hash_size);
        
def sql_kudu_complete():
    global total_kudu_sql    

    row_cnt = 0    
    total_col_cnt = 0

    create_str = "CREATE TABLE {table_nm} (\n"
    coumn_str = ""
    pkey_str = "\tprimary key ( {pk_list} )\n" 
    end_str = """) PARTITION BY HASH ( {pk_list} ) PARTITIONS {hash_cnt}
STORED AS KUDU
TBLPROPERTIES (
    'kudu.master_addresses' = 'test1.com,test2.com,test3.com'
);

"""
    kudu_sql_str = ""
    pk_key_str = ""

    

    for t_nm in table_list:
        total_col_cnt = len(sorted_column_list[row_cnt])
        col_cnt = 0

        key_cnt = 1
        total_key_cnt = len(pk_key[row_cnt])
        for key in pk_key[row_cnt]:
            pk_key_str += key
            if total_key_cnt > key_cnt:
                pk_key_str += ", "
            key_cnt += 1


        for column in sorted_column_list[row_cnt]:
            
            if sorted_type_len_list[row_cnt][col_cnt] not in "":            
                 temp_len =  "("+ sorted_type_len_list[row_cnt][col_cnt] + ")"
            else:
                temp_len =  ""
            
            if sorted_type_list[row_cnt][col_cnt].find("varchar") > -1 or sorted_type_list[row_cnt][col_cnt].find("char") > -1:
                temp_type = "string"
                temp_len = "" 
            elif sorted_type_list[row_cnt][col_cnt].find("integer") > -1 :
                temp_type = "int"
            else:
                temp_type = sorted_type_list[row_cnt][col_cnt]

            temp_null = sorted_nullable_list[row_cnt][col_cnt]
            coumn_str += "\t" + column  + " " + temp_type + temp_len + " " + temp_null
            if col_cnt < (total_col_cnt-1) :
                coumn_str += ", \n"
            else:               
                coumn_str += ", \n"

                table_name = table_rename(t_nm) 
                
                kudu_sql_str = create_str.format(table_nm=table_name) + coumn_str + pkey_str.format(pk_list=pk_key_str) + end_str.format(pk_list=pk_key_str, hash_cnt=kudu_hash_size[row_cnt].strip())
                coumn_str = ""
                pk_key_str = ""
                line_enter_plus = 1
                #print(kudu_sql_str)

            col_cnt += 1
        total_kudu_sql += kudu_sql_str
        row_cnt += 1    
    print(total_kudu_sql) 


def sql_hive_csv_complete():
    global total_hive_csv_sql    

    row_cnt = 0    
    total_col_cnt = 0

    create_str = "CREATE TABLE {table_nm}_csv (\n"
    coumn_str = ""    
    end_str = """) ROW FORMAT DELIMITED (                                           
FIELDS TERMINATED BY ','
),
LOCATION (
    'hdfs://{hdfs_uri}/user/hive/warehouse/{schema}.db/{table}_csv';
),                                      
STORED AS INPUTFORMAT (                                           
  'org.apache.hadoop.mapred.TextInputFormat'),
OUTPUTFORMAT(                                                    
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' 
);

"""
    hive_csv_sql_str = ""
       
    csvSchema = ""
    csvTable = "" 

    for t_nm in table_list:
        total_col_cnt = len(sorted_column_list[row_cnt])
        col_cnt = 0

        for column in sorted_column_list[row_cnt]:
            
            if sorted_type_len_list[row_cnt][col_cnt] not in "":            
                 temp_len =  "("+ sorted_type_len_list[row_cnt][col_cnt] + ")"
            else:
                temp_len =  ""
            
            if sorted_type_list[row_cnt][col_cnt].find("varchar") > -1 or sorted_type_list[row_cnt][col_cnt].find("char") > -1:
                temp_type = "string"
                temp_len = "" 
            elif sorted_type_list[row_cnt][col_cnt].find("integer") > -1 :
                temp_type = "int"
            else:
                temp_type = sorted_type_list[row_cnt][col_cnt]

            
            coumn_str += "\t" + column  + " " + temp_type + temp_len + " "
            if col_cnt < (total_col_cnt-1) :
                coumn_str += ", \n"
            else:               
                coumn_str += " \n"

                table_name = table_rename(t_nm) 

                if table_name.find(".") > -1:
                    csvSchema = table_name.split('.')[0]
                    csvTable = table_name.split('.')[1]
                
                hive_csv_sql_str = create_str.format(table_nm=table_name) + coumn_str + end_str.format(hdfs_uri="hdfs_uri", schema=csvSchema, table=csvTable)
                coumn_str = ""
                pk_key_str = ""
                line_enter_plus = 1
                #print(hive_csv_sql_str)

            col_cnt += 1
        total_hive_csv_sql += hive_csv_sql_str
        row_cnt += 1    
    print(total_hive_csv_sql) 


def write_file(path, sql):
    print("##### WRITE FILE START")
    global write_cnt    
    write_cnt += 1
    write_type = 'w'

    if write_cnt > 2:
        write_type = 'a'
    else:
        write_type = 'w'

    with open(path, write_type) as f:        
        f.write(sql)
        
    print("##### WRITE FILE END")


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
def xmlWriteFile(xml, tName):            
    indent(xml)  
    print("##### XML File : {tn}.xml #####".format(tn=tName));
    dump(xml)
    tar_file = os.path.dirname(os.path.realpath(__file__)) + "\{tb}.xml".format(tb=tName)
    print("##### XML File Write PATH : {path}".format(path=tar_file));
    ElementTree(xml).write(tar_file, encoding="utf-8", xml_declaration=True)

def talendTypeChange(st):
    rtn = ""
    if st.find("integer") > -1:
        rtn = 'id_Integer'
    elif st.find("smailint") > -1:
        rtn = 'id_Short'
    elif st.find("double") > -1:
        rtn = 'id_Double'    
    elif st.find("nubmer") > -1:
        rtn = 'id_BigDecimal'    
    elif st.find("timestamp") > -1 or st.find("date") > -1:
        rtn = 'id_Date'        
    else :
        rtn = "id_String"

    return rtn

def xml_complete():

    row_cnt = 0
    for t_nm in table_list:
        total_col_cnt = len(sorted_column_list[row_cnt])

        root = Element("schema", dbasId="ibmdb2_id")        
        col_cnt = 0        
        for column in sorted_column_list[row_cnt]:
            node1 = Element("column")
            node1.attrib["comment"] = ''
            node1.attrib["default"] = ''

            if column in pk_key[row_cnt]:
                node1.attrib["key"] = 'true'
            else:    
                node1.attrib["key"] = 'false'

            node1.attrib["label"] = column.replace("`","").upper()
            node1.attrib["originalDbColumn"] = column.replace("`","").upper()
            node1.attrib["length"] = sorted_type_len_list[row_cnt][col_cnt]
            node1.attrib["originalLength"] = sorted_type_len_list[row_cnt][col_cnt]
            node1.attrib["precision"] = ''
            node1.attrib["type"] = sorted_type_list[row_cnt][col_cnt].upper()            
            node1.attrib["talendType"] = talendTypeChange(sorted_type_list[row_cnt][col_cnt])
            if sorted_type_list[row_cnt][col_cnt].find("timestamp") > -1 or sorted_type_list[row_cnt][col_cnt].find("date") > -1:
               node1.attrib["pattern"] = '&quot;dd-MM-yyyy&quot;'            
            else :
               node1.attrib["pattern"] = ''            

            if sorted_nullable_list[row_cnt][col_cnt].find("not") > -1:
                node1.attrib["nullable"] = 'false'
            else:    
                node1.attrib["nullable"] = 'true'
  
            root.append(node1)
            col_cnt += 1
        
        xmlWriteFile(root, t_nm)
        row_cnt += 1        



if __name__ == "__main__":
    
    # ddl file read 
    read_file()

    # valuses sorting
    pkSorting()                          

    # file writing
    sql_sel_complete()
    write_file(target_select_sql_file, total_sel_sql)

    # KUDU Hash Size Read
    read_hash_file()

    # KUDU SQL 
    sql_kudu_complete()    
    write_file(target_kudu_file, total_kudu_sql)

    # HIVE CSV SQL
    sql_hive_csv_complete()
    write_file(target_hive_csv_file, total_hive_csv_sql)

    # Talend Xml Schema
    xml_complete()

    print("##### TABLE CNT : {t_cnt}".format(t_cnt=t_cnt))

