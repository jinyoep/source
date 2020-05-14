import re
import mysql.connector
import pymysql

mysql_con = None

def extractTable(sql_str):
    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql_str)

    lines = [line for line in q.splitlines() if not re.match("^\s*(--|#)", line)]

    q = " ".join([re.split("--:|#", line)[0] for line in lines])
    tokens = re.split(r"[\s)(;]+", q)

    result = set()
    get_next = False

    for tok in tokens:
        if get_next:
            if tok.lower() not in ["","select"]:
                result.add(tok)
            get_next = False
        get_next = tok.lower() in ["from", "join"]

    return result    

def query_executor(cursor, param):
    sql = "select * from mydb.id_info where name = %s ;"
    cursor.execute(sql, (param,))

def fn_QueryString():
    returnVal = f'''
select fab
    , wf
    , prod
    , end_dt
    , '' as conn
from etl.u_prod_oper t1 left join ipa.u_oper_parquet t2
on (1=1)
'''
    return  returnVal   

if __name__ == "__main__":
    print('# SQL Table Extract')    
    tables = extractTable(fn_QueryString())

    for t in tables:
        print(t)

    # My Sql Connection    
    '''
    try:
        mysql_con = mysql.connector.connect(host='localhost', port='3306', database='', user='root', password='han7992')
        mysql_cursor = mysql_con.cursor(dictionary=True)

        query_executor(mysql_cursor, '현대카드')

        for row in mysql_cursor:        
            print('ID is: '+str(row['id']))
       

        mysql_cursor.close()

    #except Exception as e:
    except :
        print("ERROR~~")


    finally:
        if mysql_con is not None:
            mysql_con.close()
    '''


    conn = pymysql.connect(host='localhost', user='root', password='han7992',
                       db='', charset='utf8')
 
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    
    # SQL문 실행
    sql = "select * from mydb.id_info"
    curs.execute(sql)
    
    # 데이타 Fetch
    rows = curs.fetchall()
    #print(rows)     # 전체 rows
    print(rows[0])
    for row in rows:
        print(row)
    
    # Connection 닫기
    conn.close()        

