# -*- coding:utf-8 -*-
import os
import requests
import winreg
import zipfile
from para import log_local


class ChromeDriverUpdate(object):

    def __init__(self):
        # self.file_path = "E:/Python3.8/Scripts/"
        self.abs_path = os.path.abspath('.')
        self.file_path = os.path.join(self.abs_path, "chrome_driver_path/").replace('\\', '/')
        self.cd_url = 'http://npm.taobao.org/mirrors/chromedriver/'
        self.chrome_driver_url = "https://registry.npmmirror.com/-/binary/chromedriver/"
        self.log = log_local.Log("chrome_driver_update")

    # 获取本地Chrome浏览器的版本
    @staticmethod
    def get_Chrome_version():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
        version, types = winreg.QueryValueEx(key, 'version')
        return version

    # 获取网页中所有的ChromeDriver版本
    def get_server_chrome_driver_versions(self):
        versionList = []
        rep = requests.get(self.chrome_driver_url).json()
        for item in rep:
            versionList.append(item["name"])
        return versionList

    # 下载需要的ChromeDriver文件
    def download_driver(self, download_url):
        file = requests.get(download_url)
        with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
            zip_file.write(file.content)
            self.log.info('下载成功')

    def get_version(self):
        # 查询系统内的ChromeDriver版本号
        local_chrome_driver_version = os.popen(self.file_path + 'chromedriver --version').read()
        return local_chrome_driver_version.split(' ')[1]

    def unzip_driver(self):
        # 解压ChromeDriver压缩包到指定目录
        # f = zipfile.ZipFile("chromedriver.zip", 'r')
        f = zipfile.ZipFile("log2.zip", 'r')
        for file in f.namelist():
            f.extract(file, self.file_path)

    def check_update_chrome_driver(self):
        chromeVersion = self.get_Chrome_version()  # 获取本地Chrome浏览器的版本号
        chrome_main_version = int(chromeVersion.split(".")[0])  # 本地Chrome浏览器主版本号
        driver_main_version = ''  # 初始化ChromeDriver的主版本号
        if not os.path.isdir(self.file_path):
            os.makedirs(self.file_path)
            self.log.info("没有该目录，将自动创建" + self.file_path + "目录")
        if os.path.exists(os.path.join(self.file_path, "chromedriver.exe")):  # 查询是否本地存在chromedriver.exe文件
            driverVersion = self.get_version()
            driver_main_version = int(driverVersion.split(".")[0])  # 获取本地ChromeDriver主版本号
        download_url = ''
        if driver_main_version != chrome_main_version:
            if driver_main_version == '':
                self.log.info("本地不存在ChromeDriver驱动程序！")
            versionList = self.get_server_chrome_driver_versions()
            if chromeVersion in versionList:
                download_url = f"{self.cd_url}{chromeVersion}/chromedriver_win32.zip"
            else:
                for version in versionList:
                    if version.startswith(str(chrome_main_version)):
                        download_url = f"{self.cd_url}{version}/chromedriver_win32.zip"
                        break
                if download_url == "":
                    self.log.info("暂无法找到与chrome兼容的ChromeDriver版本！")
                    return

            self.download_driver(download_url=download_url)
            self.unzip_driver()
            os.remove("chromedriver.zip")
            self.log.info('更新后的Chromedriver版本为：' + self.get_version())
        else:
            self.log.info("chromedriver版本与chrome浏览器相兼容，无需更新chromedriver版本！")
        return os.path.join(self.file_path, "chromedriver.exe")


if __name__ == "__main__":
    version_update = ChromeDriverUpdate()
    version_update.unzip_driver()
    # version_update.check_update_chrome_driver()

