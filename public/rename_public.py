import ctypes

#rename用例调用
class rename_task_object:
    valid = False
    rename_result = 0
rename_task = rename_task_object

def GetRename_cb(instance, result):
    '''设置重命名文件夹信息函数'''
    global rename_task
    rename_task.valid = True
    rename_task.rename_result = result

CRENAMEFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int)
RenameResult_cb = CRENAMEFUNC(GetRename_cb)