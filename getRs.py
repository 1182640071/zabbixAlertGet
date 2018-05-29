#!/usr/bin/python
#coding=utf-8
import psycopg2 , sys
import psycopg2.extras

class function(object):

    @staticmethod
    def getDbResult(start_time , end_time):
        conn = psycopg2.connect(host="10.10.60.45",port=5432,user="postgres",password="postgres",database="zabbix")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT  count(*) as cnt ,substring(subject , '.*时间') as new_subject from alerts where subject ~ '告警.*时间' and to_timestamp(clock) >= '" +start_time + "' and to_timestamp(clock) <= '" + end_time + "' and userid=3  and mediatypeid=4 group by new_subject order by cnt desc"
        print sql
        cur.execute(sql)
        list = cur.fetchall()
        conn.close()
        # list = []
        # list.append(['1','asdfasdf'])
        # list.append(['3','fffffffff'])
        return list



    def getHostAlert(self , sql):
        from configAlert import host , port , user , passwd , databases
        conn = psycopg2.connect(host=host,port=port,user=user,password=passwd,database=databases)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql)
        list = cur.fetchall()
        conn.close()
        return list

