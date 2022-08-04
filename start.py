# -*- coding:utf-8 -*-
from para.ssh_sftp_download import SSH
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def do():
    ssh = SSH()  # 创建一个ssh类对象

    ssh.connect()  # 连接远程服务器

    # 获取远程home/download_file目录最近两天内修改的二级目录
    remotes = ssh.execute_cmd("""find /home/download_file/* -maxdepth 0  -ctime -2 -type d""")
    if remotes is False:
        ssh.log.error("命令执行失败！")
        return
    if remotes == '':
        ssh.log.info("远程home/download_file目录没有最近两天内修改的二级目录")
        return

    ssh.log.info(remotes)
    remotes = remotes.strip().split()

    # version_update.check_update_chrome_driver()  # 更新ChromeDriver驱动程序

    for remote_dir in remotes:
        print("remote_dir = " + remote_dir)
        local_dir = r'E:\Pycharm_file\Data_collection\para\auto_makedir'
        ssh.sftp_get_dir(remote_dir, local_dir)  # 下载文件
        # ssh.open_html()

    ssh.close()


if __name__ == "__main__":
    schedule = BlockingScheduler()
    cronTrigger = CronTrigger(hour=9, minute=30, second=00, timezone='Asia/Shanghai')
    # schedule.add_job(do, cronTrigger, id='my_job')
    schedule.add_job(do, cronTrigger)
    schedule.start()