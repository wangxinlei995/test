import time
import ctypes
import unittest
from public.config import Config, SDK_PATH, UPLOAD_PATH
from public.list_public import ls_cb
from public.mkdir_public import MkdirResult_cb, mkdir_task
from public.rename_public import rename_task, RenameResult_cb
from public.log import logger


class TestRaysyncRename(unittest.TestCase):
    '''测试重命名基本功能'''
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
            #登录客户端，地址，端口号，用户名，密码可在config.yml中修改
            #登录server
        except:
            logger.info('登录失败，请检查服务器地址/端口/用户名/密码是否正确')

        rename_task.valid = False
        mkdir_task.valid = False
        self.lib.Raysync_List(self.instance, "/")
        #list操作
        time.sleep(2)

    def test_rename_1(self):
        '''测试正常重命名文件夹'''
        self.lib.Raysync_SetRenameCallback(self.instance, RenameResult_cb)
        #设置创建文件夹回调，在public中设置回调时的格式，re_cb为重命名的回调
        self.lib.Raysync_Rename(self.instance, bytes("/", encoding='utf8'), bytes("AutoTestMkdir", encoding='utf8'),bytes("AutoTestMkdir_New", encoding='utf8') )
        #重命名AutoTestMkdir文件夹为AutoTestMkdir_New
        while not rename_task.valid:
            time.sleep(1)
        self.assertTrue(rename_task.rename_result == 0)

    def test_rename_2(self):
        '''测试正常重命名文件'''
        self.lib.Raysync_SetRenameCallback(self.instance, RenameResult_cb)
        #设置创建文件夹回调，在public中设置回调时的格式，re_cb为重命名的回调
        self.lib.Raysync_SetListCallback(self.instance, ls_cb)
        #设置回调，在public中设置回调时的格式
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'Raysync.exe')
        # 格式化Raysync.exe 文件
        self.lib.Raysync_Upload(self.instance, bytes(UPLOAD_PATH, encoding='utf8'), '/', files, None, 'upload_task_0')
        # 上传单个Raysync.exe 文件
        time.sleep(10)
        self.lib.Raysync_Rename(self.instance, "/", bytes("Raysync.exe", encoding='utf8'),bytes("Raysync_New.exe", encoding='utf8') )
        #重命名Raysync.exe文件为Raysync_New.exe
        self.lib.Raysync_List(self.instance, "/")
        while not rename_task.valid:
            time.sleep(1)
        self.assertTrue(rename_task.rename_result == 0)

    def test_rename_3(self):
        '''测试重命名文件夹失败：重命名名字已存在'''
        self.lib.Raysync_SetCreateFolderCallback(self.instance, MkdirResult_cb)
        #设置创建文件夹回调，在public中设置回调时的格式
        self.lib.Raysync_CreateFolder(self.instance, "/", bytes("AutoTestMkdir", encoding='utf8'))
        #创建AutoTestMkdir文件夹
        self.lib.Raysync_SetRenameCallback(self.instance, RenameResult_cb)
        #设置重命名文件夹回调，在public中设置回调时的格式
        self.lib.Raysync_Rename(self.instance, "/", bytes("AutoTestMkdir_New", encoding='utf8'),bytes("AutoTestMkdir", encoding='utf8') )
        #重命名AutoTestMkdir_New为刚刚创建的AutoTestMkdir文件夹
        while not mkdir_task.valid:
            time.sleep(1)
            while not rename_task.valid:
                time.sleep(1)
        self.assertTrue(rename_task.rename_result != 0)


    def tearDown(self):
        self.lib.Raysync_DestroyRaysyncInterface(self.instance)
        #每个用例测试结束时，销毁实例