import ctypes
import unittest
from public.config import Config,SDK_PATH,DOWNLOAD_PATH
import os
from public.log import logger
import time
from public.transfer_public  import upload_task,statechanged_func





class TestRaysyncDownload(unittest.TestCase):
    '''测试下载基本功能'''
    URL = Config().get('URL')
    port = Config().get('PORT')
    username = Config().get('USERNAME')
    password = Config().get('PASSWORD')
    lib = ctypes.CDLL(SDK_PATH)


    def setUp(self):
        self.instance = self.lib.Raysync_CreateRaysyncInterface()
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
        upload_task.task_state = 0  # 初始化upload_task.task_state = 0
        self.lib.Raysync_List(self.instance, "/")
        #list操作
        time.sleep(2)
        self.lib.Raysync_DeleteAllTask(self.instance)   #清空传输列表
        time.sleep(1)

    def test_download_1(self):
        '''正常下载单个文件'''
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        #设置任务状态回调
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'burpsuite_community_windows-x64_v1_7_36.exe')
        # 格式化167-mov.mov 文件
        self.lib.Raysync_Download(self.instance, bytes(DOWNLOAD_PATH, encoding='utf8'), '/', files, None, 'download_task_1')
        time.sleep(2)
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 10)
        self.assertTrue(os.path.exists(DOWNLOAD_PATH + '\\burpsuite_community_windows-x64_v1_7_36.exe'))

    def test_download_2(self):
        '''正常下载单个文件夹'''
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'upload_task')

        self.lib.Raysync_Download(self.instance,bytes(DOWNLOAD_PATH, encoding='utf8') ,'/',files,None,'download_task_2')
        #上传upload_task目录
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 10)
        self.assertTrue(os.path.exists(DOWNLOAD_PATH + '\\upload_task'))



    def test_download_3(self):
        '''正常下载多个文件'''
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        upload_file = ['167_MPG.mpg', '英文max-webm.webm', '中文maya_mp4格式.mp4', '中文maya—WNV.wmv']

        files = (ctypes.c_char_p * (len(upload_file) + 1))()
        #将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1

        a = 0
        for i in upload_file:
                files[a] = ctypes.c_char_p(bytes(i, encoding='utf8'))
                a = a + 1

        self.lib.Raysync_Download(self.instance,bytes(DOWNLOAD_PATH, encoding='utf8') , '/' , files , None , 'download_task_3')
        #判断raysync.exe文件是否在列表中，注意bytes格式，二进制格式
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 10)

    def test_download_4(self):
        '''下载单个文件至本地，指定名称为test.mov'''
        try:
            os.remove(DOWNLOAD_PATH,'167-mov.mov')
        except:
            logger.info('无需删除')
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        #设置任务状态回调
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'burpsuite_community_windows-x64_v1_7_36.exe')
        # 格式化167-mov.mov 文件
        files_download = (ctypes.c_char_p * 2)()
        files_download[0] = ctypes.c_char_p(b'test.mov')
        self.lib.Raysync_Download(self.instance, bytes(DOWNLOAD_PATH, encoding='utf8'), '/', files, files_download, 'download_task_4')
        # 上传单个167-mov.mov 文件
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 10)
        self.assertTrue(os.path.exists(DOWNLOAD_PATH + '\\test.mov'))





    def tearDown(self):
        self.lib.Raysync_DestroyRaysyncInterface(self.instance)
        #每个用例测试结束时，销毁实例