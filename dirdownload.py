import paramiko
import os
import stat
import datetime as dt

from paramiko import AuthenticationException


def getRemoteFiles(remoteDir, sftp):
    # 加载sftp服务器文件对象(根目录)
    filesAttr = sftp.listdir_attr(remoteDir)
    try:
        # foreach遍历
        for fileAttr in filesAttr:
            # 判断是否为目录
            if stat.S_ISDIR(fileAttr.st_mode):
                # 1.当是文件夹时
                # 计算子文件夹在ftp服务器上的路径
                son_remoteDir = remoteDir + '/' + fileAttr.filename
                # 生成器, 迭代调用函数自身
                yield from getRemoteFiles(son_remoteDir, sftp)
            else:
                # 2.当是文件时
                # 生成器, 添加"路径+文件名"到迭代器"
                yield remoteDir + '/' + fileAttr.filename
    except Exception as e:
        print('getAllFilePath exception:', e)


# 远程目录remoteDir文件下载保存到本地目录localDir
def download_file(remoteDir, localDir, sftp):
    # 记录下载开始时间
    dt_start = dt.datetime.now()
    print('................. {} 开始下载!..................\n'.format(dt_start))

    # 判断输入的本地目录是否存在
    #    if not os.path.exists(localDir):
    #    # 若本地目录不存在,则创建该目录
    #    os.makedirs(localDir)

    # 实例化生成器, 获取sftp指定目录下的所有文件路径
    files = getRemoteFiles(remoteDir, sftp)
    print(files)
    # foreach遍历
    for file in files:
        # 要下载的远程文件, 本地时路径+文件名
        remoteFileName = file
        ###获取文件的全路径
        get_son_remote_dir = '/'.join(remoteFileName.split('/')[0:-1])
        # 定义下载保存到本地时的路径+全路径+文件名
        localFileName = os.path.join(localDir + get_son_remote_dir, file.split('/')[-1])
        if not os.path.exists(localDir + get_son_remote_dir):
            # 若本地目录不存在,则创建该目录
            os.makedirs(localDir + get_son_remote_dir)

        try:
            # 下载文件, 本地已有同名文件则覆盖
            sftp.get(remoteFileName, localFileName)
            print('sftp服务器文件 {} 下载成功!\n该文件保存本地位置是 {} !\n'.format(
                remoteFileName, localFileName))
        except Exception as e:
            print('%s下载出错!:\n' % (remoteFileName), e)
            # 下载失败, 关闭连接
            sftp.close()

    # 下载成功, 关闭连接

    # 记录下载结束时间
    dt_end = dt.datetime.now()
    print('..................... {} 下载完成!..................'.format(dt_end))
    # 记录下载时长
    dt_long = dt_end - dt_start
    print('................ 本次下载共用时间 {} !...............\n'.format(dt_long))


def getConnect(ip, cmd2):
    global sftp
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过了远程连接中选择‘是’的环节,
    try:
        #        ssh.connect(ip, 22, 'app', 'avc')
        ssh.connect(ip, 22, 'app', 'dsd')
        tran = ssh.get_transport()
        sftp = paramiko.SFTPClient.from_transport(tran)
        a = []
        stdin, stdout, stderr = ssh.exec_command(cmd2)
        for i in stdout.readlines():
            j = i.strip().split()
            a.append(j[0] + " " + ' '.join(j[10:]))
        b = list(set(a))
        c = sorted(b)
        for it in c:
            print(it)
        print((''.join(c)).lower())
        if ((''.join(c)).lower().find("zabbix")) >= 0:
            print("zabbix exists")
            remote_file_path = '/etc/zabbix/'
            local_file_path = '/root/' + ip + '/'
            download_file(remote_file_path, local_file_path, sftp)
        if ((''.join(c)).lower().find("keepalived")) >= 0:
            print("keepalived exists")
            remote_file_path = '/etc/keepalived/'
            local_file_path = '/root/' + ip + '/'
            download_file(remote_file_path, local_file_path, sftp)
        if ((''.join(c)).lower().find("haproxy")) >= 0:
            print("haproxy exists")
            remote_file_path = '/etc/haproxy/'
            local_file_path = '/root/' + ip + '/'
            download_file(remote_file_path, local_file_path, sftp)
        if ((''.join(c)).lower().find("postfix")) >= 0:
            print("postfix exists")
            remote_file_path = '/etc/postfix/'
            local_file_path = '/root/' + ip + '/'
            download_file(remote_file_path, local_file_path, sftp)

        print("************************************")
        # print("connect close")
    except AuthenticationException as e:
        print('主机%s密码错误' % ip)
    except Exception as e:
        print('未知错误:', e)
    finally:
        sftp.close()
        print("ssh")
        ssh.close()
        # print("关闭")


cmd = "curl -k -s -L 'https://titan.hikvision.com/agent/download?k=4fcf35eecf2f6c74df8e2b09e1ea866e33aace5c&group=78" \
      "&protocol=0' | bash "
# cmd2=r'ps aux|grep -v "\["'
###systemd进程为init进程
###lvmetad为LVM相关服务
###/sbin/auditd 为linux的审计服务
###/usr/sbin/NetworkManager
###/usr/sbin/irqbalance  中断服务，用于提升性能及手机系统数据
###/usr/bin/dbus-daemon  网络相关服务 dbus-daemon是一个后台进程，负责消息的转发。它就像个路由器
###/usr/sbin/crond
###/sbin/agetty
###qmgr -l -t unix -u
###pickup -l -t unix -u
cmd2 = r'ps aux|grep -v "\["|grep -v "/usr/lib/systemd"|grep -v "/usr/sbin/lvmetad"|grep -v "sshd"|grep -v "/sbin/auditd"|grep -v "/usr/sbin/NetworkManager"|\
     grep -v "/usr/sbin/irqbalance"|grep -v "/usr/bin/dbus-daemon"|grep -v "/usr/sbin/crond"|grep -v "/sbin/agetty"|grep -v "qmgr -l -t unix -u"|grep -v "pickup -l -t unix -u"|sort|uniq|grep -v uniq|grep -v sort|grep -v COMMAND'
ip_list = ['192.168.1.23', '192.168.3.23']
for ip in ip_list:
    print(ip)
    getConnect(ip, cmd2)
