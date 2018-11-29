import ctypes



#task测试用例调用
class task_object:
    TaskID = 0
task = task_object

def GetTaskInfo_cb(instance, ID):
    '''设置文件传输状态信息函数'''
    global task
    if ID[0]:
        task.TaskID = ID[0]

CGETTASKINFOFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint))
TaskInfo_cb = CGETTASKINFOFUNC(GetTaskInfo_cb)