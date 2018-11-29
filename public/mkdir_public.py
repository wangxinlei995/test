import ctypes

#mkdir用例调用
class mkdir_task_object:
    valid = False
    mkdir_result = 0
mkdir_task = mkdir_task_object

def GetMkdir_cb(instance, result):
    '''设置创建文件夹信息函数'''
    global mkdir_task
    mkdir_task.valid = True
    mkdir_task.mkdir_result = result

CMKDIRFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int)
MkdirResult_cb = CMKDIRFUNC(GetMkdir_cb)