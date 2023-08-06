# -*- coding: utf-8 -*-
import os
DB_URL = {'sly': 'mysql+mysqlconnector://reader:reader@172.17.0.2/seleya' if 'SYL_DB' not in os.environ else os.environ['SYL_DB']}

server = ('192.168.199.137', 50006, 'api.jdw.smartdata-x.top', 443)