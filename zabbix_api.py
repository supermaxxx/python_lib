#!/usr/bin/env python
import json
import urllib2

class ZabbixApi:
    def __init__(self,api_info):
        self.api_info = api_info
        self.header = {"Content-Type": "application/json"}
        self.api_data = {
                'jsonrpc':'2.0',
                'method':'',
                'params':'',
                'id':0
                }
        self._set_auth_session()
       
    def _set_auth_session(self):
        self.api_data['method'] = 'user.login'
        self.api_data['params']= {
                          'user':self.api_info['user'],
                          'password':self.api_info['password']
                        }
        response = self._request()
        self.api_data['auth'] = response['result']
        self.api_data['id'] = 1
       
    def _request(self):
        post_data = json.dumps(self.api_data)
        req = urllib2.Request(self.api_info['url'],post_data)
        for k,v in self.header.items():
            req.add_header(k,v)
       
        try:
            result = urllib2.urlopen(req)
        except urllib2.URLError as e:
            print e.code
        else:
            response = json.loads(result.read())
            result.close()
            return response
       
    def run(self,method,params):
        self.api_data['method'] = method
        self.api_data['params']= params
        return self._request()

'''
Useage:
>>> from zabbix_api import ZabbixApi
>>> api_info = {
            'url': 'http://192.168.200.25/zabbix/api_jsonrpc.php',
            'user':'admin',
            'password':'zabbix'
    }
>>> zbx = ZabbixApi(api_info)
   
>>> print zbx.run("host.get",{'output':"extend"})

>>> print zbx.run("hostgroup.get",{'output':"extend"})

>>> new_user = {"name":"wangyucheng",
                "alias":"wangyucheng",
                "passwd":"wangyucheng",
                "usrgrps":{"usrgrpid":admin_groupid},
                "user_medias":[{"mediatypeid":1,
                                "sendto":"wangyucheng@domain.com",
                                "active":0,
                                "severity": 63,
                                "period": "1-7,00:00-24:00"
                 }]
    }
>>> zbx.run("user.create",new_user)
{u'jsonrpc': u'2.0', u'result': {u'userids': [u'8']}, u'id': 1}
'''
