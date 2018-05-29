#coding=utf-8
import json
import urllib2 , time
from configAlert import zabbix_api , zabbix_user , zabbix_passwd

def getToken():
   url = zabbix_api
   header = {"Content-Type":"application/json"}
   data = json.dumps(
   {
      "jsonrpc": "2.0",
      "method": "user.login",
      "params": {
      "user": zabbix_user,
      "password": zabbix_passwd
   },
   "id": 0
   })
   request = urllib2.Request(url,data)
   for key in header:
      request.add_header(key,header[key])
   try:
      result = urllib2.urlopen(request)
   except Exception:
      print "Auth Failed, Please Check Your Name AndPassword:",Exception.code
   else:
      response = json.loads(result.read())
      result.close()
      return response['result']
   # print"Auth Successful. The Auth ID Is:",response['result']
   return ''


def getHistryId(itemid , valuetype , start , end):
   id = getToken()
   rslist = []
   header = {"Content-Type":"application/json"}

   data = json.dumps({
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": "extend",
        "time_from": start,
        "time_till": end,
        "history": valuetype,
        "itemids": itemid,
        "sortfield": "clock",
        "sortorder": "ASC", # DESC
        "limit": 100
    },
    "auth": id,
    "id": 1
   })
   request = urllib2.Request(zabbix_api,data)
   for key in header:
      request.add_header(key,header[key])
   try:
      result = urllib2.urlopen(request)
   except Exception as e:
      if hasattr(e, 'reason'):
          print 'We failed to reach a server.'
          print 'Reason: ', e.reason
      elif hasattr(e, 'code'):
          print 'The server could not fulfill the request.'
          print 'Error code: ', e.code
   else:
      response = json.loads(result.read())
      result.close()
      print response['result']
      for value in response['result']:
         list = []
         list.append(value['value'])
         list.append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(value['clock']))))
         rslist.append(list)
   return rslist


def getItemId(hostid , itemname):
   id = getToken()
   hostList = []
   header = {"Content-Type":"application/json"}

   data = json.dumps({
    "jsonrpc": "2.0",
    "method": "item.get",
    "params": {
        "output": "extend",
        "hostids": hostid,
        "search": {
            "name": itemname
        },
        "sortfield": "name"
    },
    "auth": id,
    "id": 2
   })
   request = urllib2.Request(zabbix_api,data)
   for key in header:
      request.add_header(key,header[key])
   try:
      result = urllib2.urlopen(request)
   except Exception as e:
      if hasattr(e, 'reason'):
          print 'We failed to reach a server.'
          print 'Reason: ', e.reason
      elif hasattr(e, 'code'):
          print 'The server could not fulfill the request.'
          print 'Error code: ', e.code
   else:
      response = json.loads(result.read())
      result.close()
      for item in response['result']:
         if item['name'] == itemname:
            print item['itemid']
            return item['itemid'] ,item['value_type']
   return ''



def getHostList(groupid):
   id = getToken()
   hostList = []
   header = {"Content-Type":"application/json"}
   data = json.dumps(
   {
      "jsonrpc":"2.0",
      "method":"host.get",
      "params":{
          "selectParentTemplates": "extend",
          "selectGroups": "extend",
          # "output":["hostid","name"],
          "groupids":groupid
      },
      "auth":id,
      "id":2,
   })
   request = urllib2.Request(zabbix_api,data)
   for key in header:
      request.add_header(key,header[key])
   try:
      result = urllib2.urlopen(request)
   except Exception as e:
      if hasattr(e, 'reason'):
          print 'We failed to reach a server.'
          print 'Reason: ', e.reason
      elif hasattr(e, 'code'):
          print 'The server could not fulfill the request.'
          print 'Error code: ', e.code
   else:
      response = json.loads(result.read())
      result.close()
      for host in response['result']:
         list = []
         list.append(host['name'])
         list.append(host['hostid'])
         hostList.append(list)
   return hostList


def getGroupList():
   id = getToken()
   groupList = []
   header = {"Content-Type":"application/json"}
   data = json.dumps(
   {
      "jsonrpc":"2.0",
      "method":"hostgroup.get",
      "params":{
          # "output":["groupid","name"],
      },
      "auth":id,
      "id":1,
   })
   request = urllib2.Request(zabbix_api,data)
   for key in header:
      request.add_header(key,header[key])
   try:
      result = urllib2.urlopen(request)
   except Exception as e:
      if hasattr(e, 'reason'):
          print 'We failed to reach a server.'
          print 'Reason: ', e.reason
      elif hasattr(e, 'code'):
          print 'The server could not fulfill the request.'
          print 'Error code: ', e.code
   else:
      response = json.loads(result.read())
      result.close()
      for group in response['result']:
         list = []
         list.append(group['name'])
         list.append(group['groupid'])
         groupList.append(list)
   return groupList