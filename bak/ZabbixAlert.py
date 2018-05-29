#-*- coding: utf-8 -*-
'''
python api.py 8090 指定端口运行方式
'''
import web,logging , json , xlwt , StringIO
from getRs import function


urls = (
    '/GetzabbixAlert/getAlert/','GetList',
    '/GetzabbixAlert/downAlert/','DownAlert',
    '/GetzabbixAlert/getAllServers/','GetServersList',
    '/GetzabbixAlert/getStatics/' , 'GetStatics',
)


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
    def POST(self):
        return "Please send a GET request"

    def GET(self):
        i = web.input()
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
            ws.write(index,1,i[1])
            index = index + 1
        sio=StringIO.StringIO()
        wb.save(sio)   #这点很重要，传给save函数的不是保存文件名，而是一个StringIO流
        # sio.seek(0)
        return sio.getvalue()


class GetServersList:

    def GET(self):
        return "Please send a post request"

    def POST(self):
        dbf = function()
        rs = dbf.getSelectRs('select distinct host from zabbix_problem_info')
        serverlist = []
        for row in rs:
            serverlist.append(row[0])
        print serverlist
        # return serverlist
        return json.dumps(rs)



class GetStatics:

    def GET(self):
        return "Please send a post request"

    def POST(self):

        i = web.data()
        data = eval(i)
        start_tiime = str(data['start_time'])
        end_tiime = str(data['end_time'])
        _type = str(data['type'])
        servers = str(data['servers'])

        print start_tiime
        print end_tiime
        print _type
        print servers

        server_list = ''
        if servers.endswith(','):
            server_list = servers[0:len(servers)-1]
        server_list_c = ''
        for i in server_list.split(','):
            print server_list_c + "'" + i + "',"
            server_list_c = server_list_c + "'" + i + "',"

        server_list_c = server_list_c[0:len(server_list_c)-1]
        print server_list_c
        if _type == 'statics':
            sql = "select count(*) , content  from zabbix_problem_info where alert_time > '" + start_tiime + "' and alert_time < '" + end_tiime + "' and host in (" + server_list_c + ") group by content order by count(*) desc"
        else:
            sql = "select id , to_char(alert_time, 'YYYY-MM-DD HH24:MI:SS') , to_char(create_time, 'YYYY-MM-DD HH24:MI:SS') , host , content , value from zabbix_problem_info where alert_time > '" + start_tiime + "' and alert_time < '" + end_tiime + "'and host in (" + server_list_c + ")";
        print sql
        dbf = function()
        rs = dbf.getSelectRs(sql)
        serverlist = []
        # return serverlist
        print rs
        return json.dumps(rs)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    web.application(urls,globals()).run()