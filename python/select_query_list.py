import re

class selQueryList():
    
    sql = ""
    src_file = ""
    sel_path = ""

    sql_cnt = 0

    #p = re.compile('[a-z|0-9|._,\(\)`;|]+')
    p = re.compile('[a-z|_.|0-9]+')
    re_word = 'create|table|not|null|varchar|double|integer|smailint|char|timestamp|\(.+?\)|\(|\)|primary.*'
    
    db2_select_end_sql = """
WHERE 1=1
AND DW_UPDATE_DT_TM between '\"+Prop.startDateTime+\"' AND '\"+Prop.endDateTime+\"'
WITH UR\n
"""  
    sample_sql = """
        CREATE TABLE ipa.yms_u_pord_oper_2 (
            FAB VARCHAR(10) NOT NULL,    
            PRMT VARCHAR(100) NOT NULL,
            WF CHAR(2) NOT NULL,
            ROW INTEGER NULL,
            CNT SMAILINT NULL,
            `TYPE` VARCHAR(20) NULL,    
            INNO DOUBLE NULL,
            UPDATE_DT_TM TIMESTAMP NULL,
            PRIMARY KEY (FAB, PRMT)
        );      
    """

    def __init__(self, str1, str2): 
        self.src_file = str1
        self.sel_path = str2

    def writeFile(self, sql):     
        self.sql_cnt += 1
        write_type = 'w'
        if self.sql_cnt > 1:
            write_type = 'a'
        else:
            write_type = 'w'    
        
        f = open(self.sel_path, write_type)
        f.write(sql)
        f.close()

   
    def read_query(self):

           
        division_num = 5
        sel_str = "SELECT "
        sel_mid_str = "\nFROM "

        total_select_sql=""

        tb_str = ""
        columns_str = ""
        
        arr_columns = []

        with open(self.src_file, 'r') as f:
            lines = f.readlines()
            #print(lines)
            for line in lines:
                #result = self.p.findall(re.sub(self.re_word,'', line.lower()))
                result = self.p.findall(line.lower())

                col_cnt = 0    
                if 'create' in result:
                    for word in result:
                        if col_cnt == 2:
                            tb_str = word
                        col_cnt += 1
                elif 'primary' in result:
                    self.total_select_sql = sel_str + columns_str + sel_mid_str + tb_str + self.db2_select_end_sql
                    columns_str = ""
                    print(self.total_select_sql)
                    self.writeFile(self.total_select_sql)                    
                else:
                    for word in result:
                        if col_cnt == 0:
                            columns_str += word + ", "
                        col_cnt += 1

    def showMsg(self):
        print("##### Select SQL Write Cnt : {cnt} #####".format(cnt=self.sql_cnt)) 

    
        
