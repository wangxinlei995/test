import ctypes
import time
from public.log import logger




list_result = list() #获取list结果的list


def list_cb(instance, err_code, path, files, size, file_time, is_folder):
    '''创建list回调格式函数'''
    global list_result
    list_result.clear()
    if not err_code:
        print("path: ", path)
        pos = 0
        while True:
            if not files[pos]:
                break

            list_result.append(files[pos])
            print("====================================================")
            print("file", pos + 1, ":", files[pos])
            print("size", pos + 1, ":", size[pos])
            print("time", pos + 1, ":", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_time[pos])))
            print("is folder", pos + 1, ":", is_folder[pos])
            print("====================================================")
            logger.info("====================================================")
            logger.info("file " + str(pos + 1) + " : " + str(files[pos]))
            logger.info("size " + str(pos + 1) + " : " + str(size[pos]))
            logger.info("time " + str(pos + 1) + " : " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_time[pos])))
            logger.info("is folder " +  str(pos + 1) + " : " + str(is_folder[pos]))
            logger.info("====================================================")
            pos += 1

CLISTFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p),
                                 ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_int),
                                 ctypes.POINTER(ctypes.c_bool))
ls_cb = CLISTFUNC(list_cb)








