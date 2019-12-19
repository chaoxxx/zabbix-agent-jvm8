#!/usr/bin/python
# coding=utf-8
import getopt
import json
import socket
import subprocess
import sys

# watchlook the jvm process or not
jvm_alive_time = 600
# zabbix host name
host_name = socket.gethostname()
try:
    opts, args = getopt.getopt(sys.argv[1:], "k:")
except getopt.GetoptError:
    print("Usage:get-jvm-gc.py -p <process id> -n <host name>")
    sys.exit(2)

key = ''
for opt, arg in opts:
    if opt == '-k':
        key = arg

count_cmd = "ps -ef|grep java|grep -v grep|wc -l"
r0 = subprocess.Popen(count_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

out0, err0 = r0.communicate()

state = 0
if len(err0) > 0:
    print(json.dumps({'state': state}, indent=4, separators=(',', ':')))
    sys.exit(1)
app_nums = int(out0)
apps = []
for num in range(1, app_nums + 1):
    if key == '':
        cmd = "ps -ef|grep java|grep -v grep|awk 'NR==" + str(num) + "{print $2}'"
    else:
        cmd = "ps -ef|grep java|grep " + key + "|grep -v grep|awk 'NR==" + str(num) + "{print $2}'"

    r1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = r1.communicate()
    res = out + err

    cmd2 = "ps -p " + res.strip() + " -o etimes|awk 'NR==2 {print $0}'"
    r2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    etimes, err2 = r2.communicate()

    app = dict()

    app['{#JVMPROCESS}'] = res.strip()  # java进程号
    app['{#HOSTNAME}'] = host_name

    # 判断是否监视此java进程
    if int(etimes.strip()) >= jvm_alive_time:
        app['{#WATCHOVER}'] = True
    else:
        app['{#WATCHOVER}'] = False
    apps.append(app)

state = 1
print(json.dumps({'data': apps}, indent=4, separators=(',', ':')))
