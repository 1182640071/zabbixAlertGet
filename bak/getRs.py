#!/usr/bin/python
#coding=utf-8
import psycopg2 , sys
import psycopg2.extras

class function(object):
    # host = '10.9.70.42'
    # port = '3433'
    # user = 'ctilink_zabbix'
    # passwd = ''
    # databases = 'zabbix'
    host = '52.83.137.53'
    port = '5432'
    user = 'postgres'
    passwd = 'postgres'
    databases = 'Zabbix_alert_collect'

    @staticmethod
    def getDbResult(start_time , end_time):
        # conn = psycopg2.connect(host="172.31.0.81",port=5432,user="postgres",password="postgres",database="zabbix")
        # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # sql = "SELECT  count(*) as cnt ,substring(subject , '.*时间') as new_subject from alerts where subject ~ '告警.*时间' and to_timestamp(clock) >= '" +start_time + "' and to_timestamp(clock) <= '" + end_time + "' and userid=3  and mediatypeid=4 group by new_subject order by cnt desc"
        # cur.execute(sql)
        # list = cur.fetchall()
        # # print rows
        # #for row in rows:
        # #    print row
        # #    for i in row:
        # #        print i
        # #    print '==================='
        # conn.close()
        list = []
        list.append(['1','asdfasdf'])
        list.append(['3','fffffffff'])
        return list

    def getSelectRs(self , sql):
        conn = psycopg2.connect(host=self.host,port=self.port,user=self.user,password=self.passwd,database=self.databases)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows