import ctypes
import unittest
from public.config import Config, SDK_PATH, UPLOAD_PATH, BASE_PATH
from public.log import logger
import time
from public.task_public import task, TaskInfo_cb
from public.transfer_public import statechanged_func, upload_task
from public.remove_public import RemoveResult_cb, remove_task



class TestRaysyncTask(unittest.TestCase):
    '''测试任务状态基本功能'''
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
        task.TaskID = 0  # 初始化task.TaskID = 0
        remove_task.valid = False
        self.lib.Raysync_List(self.instance, "/")
        #list操作
        time.sleep(2)
        self.lib.Raysync_DeleteAllTask(self.instance)   #清空传输列表
        time.sleep(1)

    def test_task_1(self):
        '''正常暂停单个文件上传传输'''
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        #设置任务状态回调
        self.lib.Raysync_SetTaskListCallback(self.instance, TaskInfo_cb)
        #设置任务列表回调，获取任务ID
        self.lib.Raysync_SetRemoveCallback(self.instance, RemoveResult_cb)
        #设置文件删除回调
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'burpsuite_community_windows-x64_v1_7_36.exe')
        # 格式化167167_MPG.mpg 文件
        try:
            self.lib.Raysync_Remove(self.instance,'/',files)
            while not remove_task.valid:
                time.sleep(1)
        except:
            logger.info('服务器不存在该文件，无需删除')
        self.lib.Raysync_Upload(self.instance, bytes(UPLOAD_PATH, encoding='utf8'), '/', files, None, 'upload_task_1')
        time.sleep(1)
        self.lib.Raysync_GetTaskList(self.instance)
        while True:
            if task.TaskID != 0:
                break
            else:
                time.sleep(1)
        # 上传单个167-mov.mov 文件
        time.sleep(2)
        self.lib.Raysync_StopTask(self.instance, task.TaskID)
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 9)


    def test_task_2(self):
        '''正常开始单个文件上传传输'''
        self.lib.Raysync_SetTaskListCallback(self.instance, TaskInfo_cb)
        #设置任务列表回调，获取任务ID
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        self.lib.Raysync_SetRemoveCallback(self.instance, RemoveResult_cb)
        #设置文件删除回调
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'burpsuite_community_windows-x64_v1_7_36.exe')
        # 格式化167-mov.mov 文件
        try:
            self.lib.Raysync_Remove(self.instance,'/',files)
            while not remove_task.valid:
                time.sleep(1)
        except:
            logger.info('服务器不存在该文件，无需删除')
        self.lib.Raysync_Upload(self.instance, bytes(UPLOAD_PATH, encoding='utf8'), '/', files, None, 'upload_task_2')
        # 上传单个167-mov.mov 文件
        self.lib.Raysync_GetTaskList(self.instance)

        while True:
            if task.TaskID != 0:
                break
            else:
                time.sleep(1)
        #循环获取taskID，如果不为0则退出循环
        self.lib.Raysync_StopTask(self.instance, task.TaskID)
        #停止任务
        time.sleep(2)
        self.assertTrue(upload_task.task_state == 9)
        self.lib.Raysync_StartTask(self.instance, task.TaskID)
        time.sleep(2)
        #开始任务
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 10)


    def test_task_3(self):
        '''正常暂停单个文件夹上传传输'''
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        #设置任务状态回调
        self.lib.Raysync_SetTaskListCallback(self.instance, TaskInfo_cb)
        #设置任务列表回调，获取任务ID
        self.lib.Raysync_SetRemoveCallback(self.instance, RemoveResult_cb)
        #设置文件删除回调
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'upload_task')
        # 格式化upload_task
        try:
            self.lib.Raysync_Remove(self.instance,'/',files)
            while not remove_task.valid:
                time.sleep(1)
        except:
            logger.info('服务器不存在该文件，无需删除')
        time.sleep(1)
        self.lib.Raysync_Upload(self.instance, bytes(BASE_PATH, encoding='utf8'), '/', files, None, 'upload_task_3')
        self.lib.Raysync_GetTaskList(self.instance)
        while True:
            if task.TaskID != 0:
                break
            else:
                time.sleep(1)
        # 上传单个167-mov.mov 文件
        time.sleep(5)
        self.lib.Raysync_StopTask(self.instance, task.TaskID)
        #停止任务
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 9)


    def test_task_4(self):
        '''正常开始单个文件夹上传传输'''
        self.lib.Raysync_SetTaskListCallback(self.instance, TaskInfo_cb)
        #设置任务列表回调，获取任务ID
        self.lib.Raysync_SetTaskStateChangedCallback(self.instance, statechanged_func)
        self.lib.Raysync_SetRemoveCallback(self.instance, RemoveResult_cb)
        #设置文件删除回调
        files = (ctypes.c_char_p * 2)()
        # 将上传文件转化为c的数组，ctyps.c_char_p * 文件数量 + 1
        files[0] = ctypes.c_char_p(b'upload_task')
        # 格式化upload_task
        try:
            self.lib.Raysync_Remove(self.instance,'/',files)
            while not remove_task.valid:
                time.sleep(1)
        except:
            logger.info('服务器不存在该文件，无需删除')
        self.lib.Raysync_Upload(self.instance, bytes(BASE_PATH, encoding='utf8'), '/', files, None, 'upload_task_4')
        self.lib.Raysync_GetTaskList(self.instance)
        while True:
            if task.TaskID != 0:
                break
            else:
                time.sleep(1)
        #循环获取taskID，如果不为0则退出循环
        time.sleep(2)
        self.lib.Raysync_StopTask(self.instance, task.TaskID)
        #停止任务
        time.sleep(2)
        self.assertTrue(upload_task.task_state == 9)
        self.lib.Raysync_StartTask(self.instance, task.TaskID)
        time.sleep(2)
        #开始任务
        while True:
            if upload_task.task_state >= 9:
                break
            else:
                time.sleep(1)
        self.assertTrue(upload_task.task_state == 10)

    def tearDown(self):
        self.lib.Raysync_DestroyRaysyncInterface(self.instance)
        #每个用例测试结束时，销毁实例
