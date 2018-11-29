'''
读取配置，这里配置文件用的yaml，也可以其他的XML,INI等，需要在file_reader中添加对应的Reader进行处理
'''

import os
from public.file_reader import YamlReader

# 通过当前文件的绝对路径，其父级目录一定是框架的base目录，然后确定各层的绝对路径。如果你的结构不同，可自行修改。
# 之前直接拼接的路径，修改了一下，用现在下面这种方法，可以支持linux和windows等不同的平台

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH,'config','config.yml')
DATA_PATH = os.path.join(BASE_PATH,'data')
MKDIR_WIREFILE_PATH = os.path.join(BASE_PATH,'data','mkdir_test.txt')
RENAME_WIREFILE_PATH = os.path.join(BASE_PATH,'data','rename_test.txt')
REMOVE_WIREFILE_PATH = os.path.join(BASE_PATH,'data','remove_test.txt')
SDK_PATH = os.path.join(BASE_PATH,'sdk','RaysyncSDK.dll')
LOG_PATH = os.path.join(BASE_PATH,'log')
REPORT_PATH = os.path.join(BASE_PATH,'report')
UPLOAD_PATH = os.path.join(BASE_PATH,'upload_task')
DOWNLOAD_PATH = os.path.join(BASE_PATH,'download_task')
TESTCASE_PATH = os.path.join(BASE_PATH,'test')


class Config:
    def __init__(self,config = CONFIG_FILE):
        self.config = YamlReader(config).data

    def get(self, element, index = 0):
        '''
         yaml是可以通过'---'分节的。用YamlReader读取返回的是一个list，第一项是默认的节，如果有多个节，可以传入index来获取。
        这样我们其实可以把框架相关的配置放在默认节，其他的关于项目的配置放在其他节中。可以在框架中实现多个项目的测试。
        '''
        return self.config[index].get(element)