import paramiko
import os
import stat
import datetime as dt

from paramiko import AuthenticationException


def getRemoteFiles(remoteDir, sftp):
    # ����sftp�������ļ�����(��Ŀ¼)
    filesAttr = sftp.listdir_attr(remoteDir)
    try:
        # foreach����
        for fileAttr in filesAttr:
            # �ж��Ƿ�ΪĿ¼
            if stat.S_ISDIR(fileAttr.st_mode):
                # 1.�����ļ���ʱ
                # �������ļ�����ftp�������ϵ�·��
                son_remoteDir = remoteDir + '/' + fileAttr.filename
                # ������, �������ú�������
                yield from getRemoteFiles(son_remoteDir, sftp)
            else:
                # 2.�����ļ�ʱ
                # ������, ���"·��+�ļ���"��������"
                yield remoteDir + '/' + fileAttr.filename
    except Exception as e:
        print('getAllFilePath exception:', e)


# Զ��Ŀ¼remoteDir�ļ����ر��浽����Ŀ¼localDir
def download_file(remoteDir, localDir, sftp):
    # ��¼���ؿ�ʼʱ��
    dt_start = dt.datetime.now()
    print('................. {} ��ʼ����!..................\n'.format(dt_start))

    # �ж�����ı���Ŀ¼�Ƿ����
    #    if not os.path.exists(localDir):
    #    # ������Ŀ¼������,�򴴽���Ŀ¼
    #    os.makedirs(localDir)

    # ʵ����������, ��ȡsftpָ��Ŀ¼�µ������ļ�·��
    files = getRemoteFiles(remoteDir, sftp)
    print(files)
    # foreach����
    for file in files:
        # Ҫ���ص�Զ���ļ�, ����ʱ·��+�ļ���
        remoteFileName = file
        ###��ȡ�ļ���ȫ·��
        get_son_remote_dir = '/'.join(remoteFileName.split('/')[0:-1])
        # �������ر��浽����ʱ��·��+ȫ·��+�ļ���
        localFileName = os.path.join(localDir + get_son_remote_dir, file.split('/')[-1])
        if not os.path.exists(localDir + get_son_remote_dir):
            # ������Ŀ¼������,�򴴽���Ŀ¼
            os.makedirs(localDir + get_son_remote_dir)

        try:
            # �����ļ�, ��������ͬ���ļ��򸲸�
            sftp.get(remoteFileName, localFileName)
            print('sftp�������ļ� {} ���سɹ�!\n���ļ����汾��λ���� {} !\n'.format(
                remoteFileName, localFileName))
        except Exception as e:
            print('%s���س���!:\n' % (remoteFileName), e)
            # ����ʧ��, �ر�����
            sftp.close()

    # ���سɹ�, �ر�����

    # ��¼���ؽ���ʱ��
    dt_end = dt.datetime.now()
    print('..................... {} �������!..................'.format(dt_end))
    # ��¼����ʱ��
    dt_long = dt_end - dt_start
    print('................ �������ع���ʱ�� {} !...............\n'.format(dt_long))


def getConnect(ip, cmd2):
    global sftp
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # ������Զ��������ѡ���ǡ��Ļ���,
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
        print('����%s�������' % ip)
    except Exception as e:
        print('δ֪����:', e)
    finally:
        sftp.close()
        print("ssh")
        ssh.close()
        # print("�ر�")


cmd = "curl -k -s -L 'https://titan.hikvision.com/agent/download?k=4fcf35eecf2f6c74df8e2b09e1ea866e33aace5c&group=78" \
      "&protocol=0' | bash "
# cmd2=r'ps aux|grep -v "\["'
###systemd����Ϊinit����
###lvmetadΪLVM��ط���
###/sbin/auditd Ϊlinux����Ʒ���
###/usr/sbin/NetworkManager
###/usr/sbin/irqbalance  �жϷ��������������ܼ��ֻ�ϵͳ����
###/usr/bin/dbus-daemon  ������ط��� dbus-daemon��һ����̨���̣�������Ϣ��ת�����������·����
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
