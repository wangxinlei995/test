import unittest
import os,time
from public.config import DOWNLOAD_PATH,REPORT_PATH,TESTCASE_PATH
import shutil
from public.HTMLTestRunner import HTMLTestRunner
from public.mail import Email






if __name__ == '__main__':


    # 判断download_task是否为空，如果存在则用例执行前清空本地的download_task文件夹，不存在则创建
    if os.path.exists(DOWNLOAD_PATH):
        shutil.rmtree(DOWNLOAD_PATH)
        os.mkdir(DOWNLOAD_PATH)
    else:
        os.mkdir(DOWNLOAD_PATH)
    time.sleep(1)
    #测试开始时间
    start_time = time.clock()
    #测试用例地址
    testcase_dir = TESTCASE_PATH
    #遍历所有test_case下的test_*开头的文件
    discover = unittest.defaultTestLoader.discover(testcase_dir,pattern='test_raysync_*.py')
    runner = unittest.TextTestRunner()
    #生成测试报告名称，当前时间年月日+report.html
    now = time.strftime('%Y-%m-%d')
    report = REPORT_PATH + '\\%s_result.html' % now
    #生成自动化测试报告
    fp = open(report, 'wb')
    runner = HTMLTestRunner(stream=fp, verbosity=2, title='Raysync 自动化测试报告', description='用例执行情况')
    #通过邮件发送自动化测试报告
    runner.run(discover)
    fp.close()
    e = Email(title = 'Raysync自动化测试报告',
                  message = 'Raysync 自动化测试！',
                  receiver = '@rayvision.com , @rayvision.com',
                  server = 'smtp.exmail.qq.com',
                  sender = '@rayvision.com',
                  password = '',
                  path = report
                  )
    #结束时间
    end_time = time.clock()
    #用例耗时
    all_time = end_time - start_time
    # print('总共用时 %.0f 秒' % all_time)
    #发送邮件
    e.send()