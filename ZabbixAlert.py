#-*- coding: utf-8 -*-
'''
python api.py 8090 指定端口运行方式
'''
import web,logging , json , xlwt , StringIO,sys , datetime , time
from getRs import function
from zabbixFunction import getGroupList , getHostList , getItemId , getHistryId

urls = (
    '/GetzabbixAlert/getAlert/','GetList',
    '/GetzabbixAlert/downAlert/','DownAlert',
    '/GetzabbixAlert/getGroup/', 'GetGroupList',
    '/GetzabbixAlert/getHost/', 'GetHostList',
    '/GetzabbixAlert/getHostAlert/', 'GetHostAlert',
    '/GetzabbixAlert/getHistry/', 'GetHistry',
)


class GetHistry:
    def GET(self):
        return "Please send a post request"

    def POST(self):
        i = web.input()
        itemname = i.get('itemname')
        hostid = str(i.get('hostid'))
        alert_time = str(i.get('alert_time'))
        print alert_time
        _time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(alert_time,"%Y-%m-%d %H:%M:%S")))
        start_time = _time - datetime.timedelta(hours=0.5)
        end_time = _time + datetime.timedelta(hours=0.5)
        itemid , valuetype = getItemId(hostid , itemname)
        x = getHistryId(itemid , valuetype , str(int(time.mktime(time.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')))) , str(int(time.mktime(time.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')))))
        return json.dumps(x)


class GetHostAlert:

    def GET(self):
        return "Please send a post request"

    def POST(self):
        i = web.input()
        hostname = str(i.get('hostname'))
        start_time = str(i.get('start_time'))
        end_time = str(i.get('end_time'))
        sql = "SELECT  id , to_char(alert_time, 'YYYY-MM-DD HH24:MI:SS') as alert_time , to_char(create_time, 'YYYY-MM-DD HH24:MI:SS')  as create_time, host , content , value , item from  zabbix_problem_info where alert_time >= '" +start_time + "' and alert_time <= '" + end_time + "' and host = '" + hostname + "' order by alert_time desc"
        dbf = function()
        rs = dbf.getHostAlert(sql)
        print rs
        return json.dumps(rs)


class GetHostList:

    def GET(self):
        return "Please send a post request"

    def POST(self):
        i = web.input()
        groupid = str(i.get('groupid'))
        rs = getHostList(groupid)
        return json.dumps(rs)



class GetGroupList:

    def GET(self):
        return "Please send a post request"

    def POST(self):
        rs = getGroupList()
        return json.dumps(rs)


class GetList:

    def GET(self):
        return "Please send a post request"

    def POST(self):
        i = web.input()
        start_tiime = str(i.get('start_time'))
        end_tiime = str(i.get('end_time'))
        rs = function.getDbResult(start_tiime , end_tiime)
        return json.dumps(rs)


class DownAlert:
    def GET(self):
        return "Please send a POST request"

    def POST(self):
        i = web.input()
        print i
        start_tiime = str(i['starttime'])
        end_tiime = str(i['endtime'])
        rs = function.getDbResult(start_tiime , end_tiime)
        web.header('Content-type','application/vnd.ms-excel')  #指定返回的类型
        web.header('Transfer-Encoding','chunked')
        web.header('Content-Disposition','attachment;filename="export.xls"') #设定用户浏览器显示的保存文件名
        wb=xlwt.Workbook(encoding = 'utf-8')
        ws=wb.add_sheet('1')
        ws.write(0,0,u"数量")
        ws.write(0,1,u"报警内容")
        index = 1
        for i in rs:
            ws.write(index,0,i[0])
            content = i[1]
            ws.write(index,1,content)
            index = index + 1
        sio=StringIO.StringIO()
        wb.save(sio)   #这点很重要，传给save函数的不是保存文件名，而是一个StringIO流
        #sio.seek(0) 
        return sio.getvalue()


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    web.application(urls,globals()).run()
