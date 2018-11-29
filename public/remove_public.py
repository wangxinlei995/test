import ctypes

#remove用例调用
class remove_task_object:
    valid = False
    remove_result = 0
remove_task = remove_task_object

def GetRemove_cb(instance, result):
    print("GetRemove_cb!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    '''设置删除文件/文件夹函数'''
    global remove_task
    remove_task.valid = True
    remove_task.remove_result = result

CREMOVEFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int)
RemoveResult_cb = CREMOVEFUNC(GetRemove_cb)