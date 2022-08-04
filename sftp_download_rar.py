# -*- coding:utf-8 -*-
# http://npm.taobao.org/mirrors/chromedriver/ 谷歌驱动
import os
import sys
import stat
import paramiko
import traceback
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from para import log_local
from para.chrome_version import version_update
from para import parse_yaml

'''
使用paramiko类实现ssh的连接登陆,以及远程文件的上传与下载, 基本远程命令的实现等
'''


class SSH(object):

    def __init__(self, timeout=30):
        self.data = parse_yaml.ParseYaml(sys.argv[1]).parse()
        self.ip = self.data.get("ip")
        self.port = self.data.get("port")
        self.username = self.data.get("username")
        self.password = self.data.get("password")
        self.timeout = timeout
        self.ssh = paramiko.SSHClient()
        self.t = paramiko.Transport(sock=(self.ip, self.port))
        self.html = []
        self.browser = None
        self.wait = None
        self.log = log_local.Log("sftp_download")

    def password_connect(self):

        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip, port=22, username=self.username, password=self.password)

        self.t.connect(username=self.username, password=self.password)  # sptf 远程传输的连接

    def connect(self):
        try:
            self.password_connect()
        except Exception as e:
            self.log.error("远程连接失败: " + str(e))
            self.password_connect()

    def close(self):
        self.t.close()
        self.ssh.close()

    def execute_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        res, err = stdout.read(), stderr.read()
        if res:
            return res.decode()
        else:
            self.log.error(err)
            return False

    # 递归遍历远程服务器指定目录下的所有文件
    def get_all_files_in_remote_dir(self, sftp, remote_dir):
        all_files = list()
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        files = sftp.listdir_attr(remote_dir)
        for file in files:
            filename = remote_dir + '/' + file.filename

            if stat.S_ISDIR(file.st_mode):  # 如果是文件夹的话递归处理
                all_files.extend(self.get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files.append(filename)

        return all_files

    def sftp_get_dir(self, remote_dir, local_dir):
        try:

            sftp = paramiko.SFTPClient.from_transport(self.t)

            all_files = self.get_all_files_in_remote_dir(sftp, remote_dir)

            for file in all_files:
                # file = "/home/download_file/test/micro_class5.mp4"
                # remote_dir = "/home/download_file"    local_dir = r"E:\Pycharm_file\Data_collection\para\auto_makedir"
                # local_filename = r"E:\Pycharm_file\Data_collection\para\auto_makedir\download_file\micro_class5.mp4"
                local_filename = file.replace(os.path.dirname(remote_dir), local_dir).replace('/', '\\')
                local_filepath = os.path.dirname(local_filename)

                if file.__contains__("html"):
                    self.html.append(local_filename)

                if not os.path.exists(local_filepath):
                    os.makedirs(local_filepath)

                if os.path.exists(local_filename):
                    print("------------------文件：" + file + "本地已存在------------------")
                else:
                    sftp.get(file, local_filename)
        except Exception as e:
            self.log.error(e)
            print(traceback.format_exc())

    def open_html(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(0)
        self.wait = WebDriverWait(self.browser, 0)

        js = "window.open('{}','_blank');"
        for html in self.html:
            print(html)
            self.browser.get(html)
            self.browser.execute_script(js.format('https://www.baidu.com/'))
            self.browser.switch_to.window(self.browser.window_handles[-1])
            # time.sleep(3)
        self.browser.quit()

