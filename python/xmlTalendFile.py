import re, os
from xml.etree.ElementTree import Element,ElementTree,dump


class xmlTalendFile():

    src_file = ""
    db_info = ""
    tName = ""
    xml = ""

    xml_total = 0

    def __init__(self, str1, str2):         
        self.src_file = str1
        self.db_info = str2
        
    def indent(self, elem, level=0): 
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i  

    def xmlWriteFile(self):
        self.indent(self.xml)
        print("##### XML File : {tn}.xml #####".format(tn=self.tName));
        dump(self.xml)
        tar_file = os.path.dirname(os.path.realpath(__file__)) + "\{tb}.xml".format(tb=self.tName)
        print("##### XML File Write PATH : {path}".format(path=tar_file));        
        ElementTree(self.xml).write(tar_file, encoding="utf-8", xml_declaration=True)

        self.xml_total += 1
    def table_rename(self, nm):
        chg_nm = "IPA." + nm.replace(".", "_")
        return chg_nm    

    def showMsg(self):
        print("##### XML File Write Cnt : {cnt} #####".format(cnt=self.xml_total))

    def readFile(self):
        print(self.src_file) 

        p = re.compile('[A-Z|0-9|._,\(\)`;|]+')
        t_num = re.compile('[0-9]+')
        t_str = re.compile('[A-Z|_]+')        

        root = ""
        node1 = ""

        with open(self.src_file, 'r') as f:
            lines = f.readlines()            

            for line in lines:
                result = p.findall(line.upper())
                print(result)

                if 'CREATE' in result:
                    root = Element("schema", dbasId=self.db_info)
                    for wd in result:
                        if wd.find('.') > -1:                            
                            self.tName = self.table_rename(wd)
                elif 'PRIMARY' in result:
                    pk_cnt = 0
                    for wd in result:
                        pk_cnt += 1                                                
                        if pk_cnt > 2:
                            for st in t_str.findall(wd):                                
                                print("################# PK :", st)  #PK 추출
                                #node1.attrib[st].replace("stag", "prod")
                                #print('node : ', node1)
                                #for node in node1.findall('column'):
                                #    print("# child_node : ", node)
                elif ');' in result:
                    self.xml = root
                    self.xmlWriteFile();
                else :
                    col_cnt = 0
                    if len(result) > 2 :
                        node1 = Element("column")                   
                        for wd in result:                            
                            if col_cnt == 0:   #column                                      
                                node1.attrib["comment"] = ''
                                node1.attrib["default"] = ''
                                node1.attrib["key"] = 'false'
                                node1.attrib["label"] = wd
                                node1.attrib["originalDbColumn"] = wd
                            elif col_cnt == 1: #type 
                                for num in t_num.findall(wd):                                                                
                                    node1.attrib["length"] = num
                                    node1.attrib["originalLength"] = num
                                    node1.attrib["precision"] = ''                                      
                                for st in t_str.findall(wd):                                    
                                    node1.attrib["type"] = st
                                    if st.find("INTEGER") > -1:
                                        node1.attrib["talendType"] = 'id_Integer'
                                    elif st.find("SMAILINT") > -1:
                                        node1.attrib["talendType"] = 'id_Short'
                                    elif st.find("DOUBLE") > -1:
                                        node1.attrib["talendType"] = 'id_Double'    
                                    elif st.find("NUMBER") > -1:
                                        node1.attrib["talendType"] = 'id_BigDecimal'    
                                    elif st.find("TIMESTAMP") > -1 or st.find("DATE") > -1:
                                        node1.attrib["talendType"] = 'id_Date'
                                        node1.attrib["pattern"] = '&quot;dd-MM-yyyy&quot;'    
                                    else :
                                       node1.attrib["talendType"] = 'id_String'     
                                       node1.attrib["pattern"] = ''
                            elif col_cnt == 2: #NOT NULL
                                if(wd.find('NOT') > -1):                                    
                                    node1.attrib["nullable"] = 'false'
                                else:
                                    node1.attrib["nullable"] = 'true'
                            col_cnt += 1
                        root.append(node1)



              

            

       

           



        
        
       