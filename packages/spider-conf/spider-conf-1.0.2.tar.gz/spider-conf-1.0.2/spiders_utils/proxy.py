# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 16:20
# @Author  : Navy

class ProxyAbuyun(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def proxy(self):
        # 代理服务器
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = self.username
        proxyPass = self.password
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta
        }
        return proxies


def proxy(user, pwd):
    return ProxyAbuyun(user, pwd).proxy
