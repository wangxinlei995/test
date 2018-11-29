import ctypes
import time

#upload download上传下载测试用例调用
class upload_task_object:
    task_state = 0

upload_task = upload_task_object

def statechanged_cb(instance, TaskID, State):
    '''设置传输文件状态变化函数'''
    global upload_task
    upload_task.task_state = State
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), "任务ID", TaskID, "状态码", State)

TASK_STATE_CHANGED = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint)
statechanged_func = TASK_STATE_CHANGED(statechanged_cb)