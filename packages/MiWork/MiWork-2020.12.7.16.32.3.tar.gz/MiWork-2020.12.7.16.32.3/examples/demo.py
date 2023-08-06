#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MiWork.
# @File         : demo
# @Time         : 2020/12/7 4:30 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from miwork import OpenLark


ol = OpenLark(app_id='cli_9e42f87464f3d063', app_secret='n0UD5GRg9Bm02OSGawLOTeyK6pUUUOE1')

print(ol.tenant_access_token)