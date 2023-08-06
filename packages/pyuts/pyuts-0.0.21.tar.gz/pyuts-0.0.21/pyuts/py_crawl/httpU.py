# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages import urllib3
urllib3.disable_warnings()


class HttpU(PyApiB):
    """
    接口请求
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self,proxy_host=None,proxy_port=None,proxy_user=None,proxy_pswd=None):
        from ..py_proxy.proxyU import ProxyU
        self.proxyU:ProxyU = ProxyU.produce("httpU")
        if proxy_host == None:
            proxy_host = os.getenv('proxy_host','')
        if proxy_port == None:
            proxy_port = os.getenv('proxy_port')
        if proxy_user == None:
            proxy_user = os.getenv('proxy_user')
        if proxy_pswd == None:
            proxy_pswd = os.getenv('proxy_pswd')
        self.proxies = None
        if len(proxy_host) > 0:
            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host" : proxy_host,
                "port" : proxy_port,
                "user" : proxy_user,
                "pass" : proxy_pswd,
            }
            self.proxies = {
                "http"  : proxyMeta,
                "https" : proxyMeta,
            }

    def get(self, url, headers=None, savePath=None, proxyMeta=None, **kwargs):
        """ get请求\n
        {url} 地址\n
        {headers} 头部\n
        {savePath} 返回内容保存为文件的路径，None则不保存，直接返回\n
        {proxyMeta} http代理，格式 “http://user:pswd@host:port”或“http://host:port”或{"host":"","port":"","user":"","pswd":""}\n
                             或 字符串"proxyU"表示引用proxyU模块的代理 \n
        {**kwargs} 其他http参数\n
        return: {"code": 200, "msg": "", "data":"xxxx"}\n
        """
        proxies = self.__getProxies(proxyMeta)
        print(f"Use Proxies:{proxies}")
        try:
            _requests = requests.Session()
            _requests.keep_alive = False
            _requests.mount('http://', HTTPAdapter(max_retries=0))
            _requests.mount('https://', HTTPAdapter(max_retries=0))
            if savePath == None:
                resp = _requests.get(url, verify=False, proxies=proxies, headers=headers, **kwargs)
                cookies = resp.cookies
                cookie = requests.utils.dict_from_cookiejar(cookies)
                return {'code':resp.status_code,'data':resp.text,'cookie':cookie}
            else:
                resp = _requests.get(url, verify=False, proxies=proxies, headers=headers, stream=True, **kwargs)
                with open(savePath, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=512):
                        if chunk:
                            f.write(chunk)
                return {'code': 200, 'msg': f"save in {savePath}"}
        except Exception as identifier:
            pass
        return {"code":"439","msg":"IO err!"}
    
    def __getProxies(self, proxyMeta=None):
        proxies = self.proxies
        if proxyMeta == "proxyU":
            proxyMeta = self.proxyU.getProxyMeta()
        if proxyMeta:
            if isinstance(proxyMeta,dict):
                proxyMeta = self.proxyU.proxyToMeta(proxyMeta)
            proxies = {
                "http"  : proxyMeta,
                "https" : proxyMeta,
            }
        return proxies
        
    def post(self, url, headers=None, data=None, json=None, savePath=None, proxyMeta=None, **kwargs):
        """ post请求\n
        {url} 地址\n
        {headers} 头部\n
        {data} post内容\n
        {json} post内容json格式\n
        {savePath} 返回内容保存为文件的路径，None则不保存，直接返回\n
        {proxyMeta} http代理，格式 “http://user:pswd@host:port”或“http://host:port”或{"host":"","port":"","user":"","pswd":""}\n
                             或 字符串"proxyU"表示引用proxyU模块的代理 \n
        {**kwargs} 其他http参数\n
        return: {"code": 200, "msg": "", "data":"xxxx"}\n
        """
        proxies = self.__getProxies(proxyMeta)
        print(f"Use Proxies:{proxies}")
        try:
            _requests = requests.Session()
            _requests.keep_alive = False
            _requests.mount('http://', HTTPAdapter(max_retries=0))
            _requests.mount('https://', HTTPAdapter(max_retries=0))
            if savePath == None:
                resp = _requests.post(url, verify=False, proxies=proxies, headers=headers, data=data, json=json, **kwargs)
                return {'code':resp.status_code,'data':resp.text}
            else:
                resp = _requests.post(url, verify=False, proxies=proxies, headers=headers, stream=True, data=data, json=json, **kwargs)
                with open(savePath, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=512):
                        if chunk:
                            f.write(chunk)
                return {'code': 200, 'msg': f"save in {savePath}"}
        except Exception as identifier:
            pass
        return {"code":"439","msg":"IO err!"}
    