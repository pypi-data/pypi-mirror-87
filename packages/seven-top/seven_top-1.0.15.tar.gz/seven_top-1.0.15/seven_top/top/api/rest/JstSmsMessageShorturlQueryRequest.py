'''
Created by auto_sdk on 2020.10.12
'''
from seven_top.top.api.base import RestApi
class JstSmsMessageShorturlQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.short_name = None

	def getapiname(self):
		return 'taobao.jst.sms.message.shorturl.query'
