添加数据库收集告警信息
create table zabbix_problem_info (id varchar(20) NOT NULL ,alert_time timestamp without time zone NOT NULL, create_time timestamp without time zone NOT NULL, host varchar(100) NOT NULL , content varchar(2000) NOT NULL , value varchar(100) NOT NULL , item varchar(100) NOT NULL , CONSTRAINT zabbix_problem_info_pkey PRIMARY KEY (id));

添加action 设置告警信息
Default subject:  {"area":"local","TRIGGER.NAME":"{TRIGGER.NAME}","TIME":"{EVENT.DATE} {EVENT.TIME}","HOST":"{HOST.NAME}","VALUE":"{ITEM.VALUE}","ITEM":"{ITEM.NAME}"}

添加告警事件脚本
#!/usr/bin/python
#coding=utf-8


import os,sys
import psycopg2 , sys
import psycopg2.extras
from datetime import datetime
import random

try:
    _id = "AWS2" + str(datetime.now().strftime('%Y%m%d%H%M%S')) + str(random.randint(0,9))


    info = sys.argv[1]
    x = eval(info)

    content = x['TRIGGER.NAME']
    alert_time = x['TIME'].replace('.','-')
    host = x['HOST']
    value = x['VALUE']
    item = x['ITEM']


    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = psycopg2.connect(host="0.0.0.0",port=5432,user="postgres" ,password="postgres" , database="zabbix")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = 'INSERT INTO zabbix_problem_info(id, alert_time, create_time, host, content, value ,item) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    values = (_id , alert_time , create_time , host , content , value ,item )
    cur.execute(sql , values)
    conn.commit()
    conn.close()
except Exception , e:
    conn.close()