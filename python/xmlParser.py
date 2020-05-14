import re, os
import io
import xml.etree.ElementTree as ET
from datetime import datetime
#from xml.etree.ElementTree import Element,ElementTree,dump

import texttable as tt


xml = """
<?xml version='1.0' encoding='utf-8'?>
<schema dbasId="ibmdb2_id">
  <column comment="" default="" key="false" label="FAB" length="10" nullable="false" originalDbColumn="FAB" originalLength="10" pattern="" precision="" talendType="id_String" type="VARCHAR" />
  <column comment="" default="" key="false" label="OPER" length="50" nullable="false" originalDbColumn="OPER" originalLength="50" pattern="" precision="" talendType="id_String" type="VARCHAR" />
  <column comment="" default="" key="false" label="PROD" length="100" nullable="false" originalDbColumn="PROD" originalLength="100" pattern="" precision="" talendType="id_String" type="VARCHAR" />
  <column comment="" default="" key="false" label="WF" length="2" nullable="false" originalDbColumn="WF" originalLength="2" pattern="" precision="" talendType="id_String" type="CHAR" />
  <column comment="" default="" key="false" label="ROW" nullable="true" originalDbColumn="ROW" talendType="id_Integer" type="INTEGER" />
  <column comment="" default="" key="false" label="CNT" nullable="true" originalDbColumn="CNT" talendType="id_Short" type="SMAILINT" />
  <column comment="" default="" key="false" label="TYPE" length="20" nullable="true" originalDbColumn="TYPE" originalLength="20" pattern="" precision="" talendType="id_String" type="VARCHAR" />
  <column comment="" default="" key="false" label="INNO" nullable="true" originalDbColumn="INNO" talendType="id_Double" type="DOUBLE" />
  <column comment="" default="" key="false" label="UPDATE_DT_TM" nullable="true" originalDbColumn="UPDATE_DT_TM" pattern="&amp;quot;dd-MM-yyyy&amp;quot;" talendType="id_Date" type="TIMESTAMP" />
</schema>
"""

if __name__ == "__main__":
    print("### xmlParser")

    now = datetime.now()
    print(now)

    year = now.strftime("%Y")
    print("year:", year)

    month = now.strftime("%m")
    print("month:", month)

    day = now.strftime("%d")
    print("day:", day)

    time = now.strftime("%H:%M:%S")
    print("time:", time)

    #date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("date and time:",date_time)

    timestamp = 1528797322
    date_time = datetime.fromtimestamp(timestamp)

    print("Date time object:", date_time)

    d = date_time.strftime("%m/%d/%Y, %H:%M:%S")
    print("Output 2:", d)	

    d = date_time.strftime("%d %b, %Y")
    print("Output 3:", d)

    d = date_time.strftime("%d %B, %Y")
    print("Output 4:", d)

    d = date_time.strftime("%I%p")
    print("Output 5:", d)

    '''
    #tree = ET.parse(r'D:\\git_source\\python\\IPA.YMS_U_PROD_OPER.xml') # File read
    tree = ET.ElementTree(ET.fromstring(xml.strip())) # String value
    
    root = tree.getroot()

    elem = tree.findall('column')

    for elem1 in elem:
        if elem1.attrib["label"] == "FAB":
            elem1.attrib["key"] = "true"

        print(ET.dump(elem1))    

    print(ET.dump(root))    


    tab = tt.Texttable()
    header = ['Manager', 'Club', 'Year']
    tab.header(header)  
    row = ['Ottmar Hitzfeld', 'Borussia Dortmund, Bayern Munich', '1997 and 2001']
    tab.add_row(row)
    row = ['Ernst Happel', 'Feyenoord, Hamburg', '1970 and 1983']
    tab.add_row(row)
    row = ['Jose Mourinho', 'Porto, Inter Milan', '2004 and 2010']
    tab.add_row(row)
    tab.set_cols_width([18,35,15])
    tab.set_cols_align(['l','r','c'])
    tab.set_cols_valign(['t','b', 'm'])
    tab.set_deco(tab.HEADER | tab.VLINES)
    tab.set_chars(['-','|','+','#'])

    s = tab.draw()
    print(s)

    '''