import re

class readSqlFile():
    
    table_cnt = 0

    hs_file = ""
    src_file = ""
    hdfs_uri = ""    

    kudu_hash_size = []
    
    result = []
    table_name = ""
    pk_key = ""
    chaged_kudu_create_ddl = ""
    chaged_hive_csv_create_ddl = ""

    csv_path = ""
    kudu_path = ""    

    ddl_create_cnt = 0

    kudu_end_line_sql = """PARTITION BY HASH ( {pk} ) PARTITIONS {hash_cnt}
STORED AS KUDU
TBLPROPERTIES (
    'kudu.master_addresses' = 'test1.com,test2.com,test3.com'
);
    """

    hive_csv_end_line_sql = """ROW FORMAT DELIMITED (                                           
FIELDS TERMINATED BY ','),
LOCATION (
    'hdfs://{hdfs_uri}/user/hive/warehouse/{schema}.db/{table}';
),                                      
STORED AS INPUTFORMAT (                                           
  'org.apache.hadoop.mapred.TextInputFormat'),
OUTPUTFORMAT(                                                    
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' 
);
"""

    p = re.compile('[a-z|_.,\(\)|0-9|\"|;]+')
    pk_list = re.compile('[a-z]]+')

    def __init__(self, str1, str2, str3, str4, str5): 
        self.hs_file = str1
        self.src_file = str2
        self.hdfs_uri = str3
        self.kudu_path = str4
        self.csv_path = str5                      

    def read_hash_file(self):
        with open(self.hs_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                #print(line)
                self.kudu_hash_size = line.split(',')
                print(self.kudu_hash_size);
                #print("kudu_hash_size[0] :",self.kudu_hash_size[0]);

    def writeFile(self, ddl, path):     
        self.ddl_create_cnt += 1
        write_type = 'w'

        if self.ddl_create_cnt > 2:
            write_type = 'a'
        else:
            write_type = 'w'    
        
        f = open(path, write_type)
        f.write(ddl)
        f.close()
    
    def showMsg(self):
        print("##### XML File Write Cnt : {cnt} #####".format(cnt=self.ddl_create_cnt)) 


    def kudu_table_total(self, q, r, pk):
        self.chaged_kudu_create_ddl = q + self.kudu_end_line_sql.format(pk=pk, hash_cnt=int(self.kudu_hash_size[r]))
        print(self.chaged_kudu_create_ddl)
        self.writeFile(self.chaged_kudu_create_ddl, self.kudu_path)

    def hive_csv_table_total(self, q, url, sch, tab):
        #print("### q : ",q)
        self.chaged_hive_csv_create_ddl = re.sub(',\n\tprimary.*','', q) + self.hive_csv_end_line_sql.format(hdfs_uri=url, schema=sch, table=tab)
        print(self.chaged_hive_csv_create_ddl)
        self.writeFile(self.chaged_hive_csv_create_ddl, self.csv_path)    

   
    def table_rename(self, nm):
        chg_nm = "ipa." + nm.replace(".", "_")
        return chg_nm

    def read_file(self):       

        kudu_create_ddl = "" 
        hive_csv_create_ddl = ""
        csvSchema = ""
        csvTable = "" 
   
        with open(self.src_file, 'r') as f:
            lines = f.readlines()
            count = len(lines) 

            print('##### total_lines : {cnt} \n'.format(cnt=count))

            for line in lines:
                result = self.p.findall(line.lower())             

                if line.lower().find('primary') > -1:            
                    arr_str = re.findall('\(([^)]+)', line.lower())
                    for s in arr_str:
                        self.pk_key = s
                        #print('s :', s)
                    #print(pk_key) 
                    #print('pk_key : {0}'.format(pk_key))

                col_cnt = 0    
                for res in result:                    
                    chg_str = res.replace("\"","`")
                    
                    if chg_str.find('.') > -1:              
                        self.table_name = self.table_rename(chg_str)
                        csvSchema = self.table_name.split('.')[0]
                        csvTable = self.table_name.split('.')[1] + '_csv'                                            
                    
                    if chg_str.find('char') > -1 or chg_str.find('varchar') > -1:    
                        kudu_create_ddl += 'string '
                        hive_csv_create_ddl += 'string '
                    elif chg_str.find('integer') > -1:
                        kudu_create_ddl += 'int '
                        hive_csv_create_ddl += 'int '    
                    elif chg_str.find('numeric') > -1:
                        kudu_create_ddl += 'double '
                        hive_csv_create_ddl += 'double ' 
                    elif chg_str.find('.') > -1:
                        kudu_create_ddl += str(self.table_rename(chg_str)) + ' ' 
                        hive_csv_create_ddl += str(self.table_rename(chg_str)) + '_csv '               
                    elif chg_str.find(');') > -1:
                        kudu_create_ddl += ') '
                        hive_csv_create_ddl += ') '
                        self.kudu_table_total(kudu_create_ddl, self.table_cnt, self.pk_key)                        
                        self.hive_csv_table_total(hive_csv_create_ddl, self.hdfs_uri, csvSchema, csvTable)                        
                        self.table_cnt += 1
                        kudu_create_ddl = ""        # 초기화
                        hive_csv_create_ddl = ""    # 초기화                  
                    else:
                        if col_cnt == 0 and not (chg_str.find("create") > -1):
                            kudu_create_ddl += "\t"+ str(chg_str) + ' '
                        else:
                            kudu_create_ddl += str(chg_str) + ' '

                        if chg_str.find('not') > -1:
                            hive_csv_create_ddl += ''
                        elif chg_str.find('null') > -1:
                            hive_csv_create_ddl += ','                        
                        else:
                            if col_cnt == 0 and not (chg_str.find("create") > -1):
                                hive_csv_create_ddl += "\t"+ str(chg_str) + ' ' 
                            else:
                                hive_csv_create_ddl += str(chg_str) + ' ' 
            
                    col_cnt += 1

                kudu_create_ddl += '\n'
                hive_csv_create_ddl += '\n'
                #print(result)              
                
            f.close()

            try :                                                                                        
                print("##### Table Create Total Cnt :", self.table_cnt)
            except:
                print("*** read_kudu_file error!") 