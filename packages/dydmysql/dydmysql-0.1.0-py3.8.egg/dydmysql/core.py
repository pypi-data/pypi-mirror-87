# Insert your code here. 
import pymysql
#数据库操作类
class DB:
    conn=None;#这里的None相当于其它语言的NULL
    def __init__(self,host="127.0.0.1",user="root",passwd="root",db="test",port=3306):#构造函数
        self.conn=pymysql.connect(host=host,user=user,passwd=passwd,db=db,port=port)
        #数据库连接，localhost python不认，必须127.0.0.1
    def getBySql(self,sql,*param):
        cursor=self.conn.cursor();#初始化游标
        result=cursor.fetchmany(cursor.execute(sql,param))
        self.conn.commit();#提交上面的sql语句到数据库执行
        return result
    
    def getBySqlOne(self,sql,*param):
        cursor=self.conn.cursor();#初始化游标
        cursor.execute(sql,param)
        result=cursor.fetchone()
        self.conn.commit();#提交上面的sql语句到数据库执行
        return result

    def getBySql_result_unique(self,sql,*param):
        cursor=self.conn.cursor();#初始化游标
        result=cursor.fetchmany(cursor.execute(sql,param))
        self.conn.commit();#提交上面的sql语句到数据库执行
        return result[0][0]
    def setBySql(self,sql,*param):
        cursor=self.conn.cursor();#初始化游标
        cursor.execute(sql,param)
        self.conn.commit();#提交上面的sql语句到数据库执行
    def __del__(self):#析构函数
        self.conn.close();#关闭数据库连接
 
def test_print():
	    print("龙哥测试!")
     
if __name__ == '__main__':
    #主程序
    db=DB()
    print ("usertable中的条目数：")
    print (db.getBySql_result_unique("select count(*) from movie"))
    print ("usertable中id大于4的结果：")
    result=db.getBySql("select * from movie where id>%s",1)
    for row in result:
        for cell in row:
            print (str(cell)+",")
        
    
#增删改实例：db.setBySql("insert into usertable(username,password) values(%s,%s)","ff","s");

