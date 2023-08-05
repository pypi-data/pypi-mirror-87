'''
Created by auto_sdk on 2018.07.25
'''
from seven_top.top.api.base import RestApi
class FuwuSaleLinkGenRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.nick = None
		self.param_str = None

	def getapiname(self):
		return 'taobao.fuwu.sale.link.gen'
