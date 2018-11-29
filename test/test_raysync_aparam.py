import time
import ctypes
import unittest
from public.config import Config, SDK_PATH
from public.log import logger
from public.remove_public import RemoveResult_cb, remove_task
from public.list_public import ls_cb, list_result


class TestRaysyncSetParams(unittest.TestCase):
    '''测试新建文件夹基本功能'''
    URL = Config().get('URL')
    port = Config().get('PORT')
    username = Config().get('USERNAME')
    password = Config().get('PASSWORD')
    lib = ctypes.CDLL(SDK_PATH)

    def setUp(self):
        self.instance = self.lib.Raysync_CreateRaysyncInterface()
        #创建实例
        try:
            self.lib
        except:
            logger.info("dll文件不存在")
        #确认是否存在dll文件
        try:
            self.lib.Raysync_Connect(self.instance, 500)
        except:
            logger.info("Raysync_Connect 失败")
        #与dll文件建连
        try:
            self.lib.Raysync_Login(self.instance, bytes(self.URL, encoding='gbk'), self.port, bytes(self.username, encoding='gbk'),
                                 bytes(self.password, encoding='gbk'))
        except:
            logger.info('登录失败，请检查服务器地址/端口/用户名/密码是否正确')
            #登录客户端，地址，端口号，用户名，密码可在config.yml中修改
            #登录server
        self.lib.Raysync_List(self.instance, "/")
        time.sleep(2)
        remove_task.valid = False
        #list,sleep2-3s 再进行下一步的操作

    def test_SetParams_1(self):
        '''测试设置客户端运行参数'''

        self.lib.Raysync_SetParams(self.instance, 10, 10, 1200, 0, 0)
        self.lib.Raysync_SetRemoveCallback(self.instance, RemoveResult_cb)
        self.lib.Raysync_SetListCallback(self.instance,ls_cb)
        self.lib.Raysync_List(self.instance,'/')
        #设置创建文件夹回调，在public中设置回调时的格式
        time.sleep(2)
        if len(list_result) > 0:
            files = (ctypes.c_char_p * (len(list_result) + 1))()
            a = 0
            for i in list_result:
                    files[a] = ctypes.c_char_p(i)
                    a = a + 1
            # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
            self.lib.Raysync_Remove(self.instance, "/", files)
            while not remove_task.valid:
                time.sleep(1)

    def tearDown(self):
        self.lib.Raysync_DestroyRaysyncInterface(self.instance)
        #每个用例测试结束时，销毁实例
