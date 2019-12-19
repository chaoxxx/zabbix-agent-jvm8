#!/usr/bin/python
# coding=utf-8

# author cosmo zhu
# date 2019-12-18 17:00:25
import getopt
import subprocess
import sys

from pyzabbix import ZabbixMetric, ZabbixSender

# zabbix-server config
zbserver = '192.168.4.37'
zbport = 10051
# JDK config
JAVA_HOME = '/usr/share/java-1.8.0'
# which jstat options you need
methods = ['gc', 'gccapacity', 'gcnew', 'gcnewcapacity', 'gcold', 'gcoldcapacity', 'gcmetacapacity', 'gcutil']


# methods = ['gc','gccapacity']
#  垃圾回收统计
def gc(hostname, items, packet, pid):
    S0C, S1C, S0U, S1U, EC, EU, OC, OU, MC, MU, CCSC, CCSU, YGC, YGCT, FGC, FGCT, GCT = items[:18]
    packet.append(ZabbixMetric(hostname, "GC.S0C[" + str(pid) + "]", S0C))
    packet.append(ZabbixMetric(hostname, "GC.S1C[" + str(pid) + "]", S1C))
    packet.append(ZabbixMetric(hostname, "GC.S0U[" + str(pid) + "]", S0U))
    packet.append(ZabbixMetric(hostname, "GC.S1U[" + str(pid) + "]", S1U))
    packet.append(ZabbixMetric(hostname, "GC.EC[" + str(pid) + "]", EC))
    packet.append(ZabbixMetric(hostname, "GC.EU[" + str(pid) + "]", EU))
    packet.append(ZabbixMetric(hostname, "GC.OC[" + str(pid) + "]", OC))
    packet.append(ZabbixMetric(hostname, "GC.OU[" + str(pid) + "]", OU))
    packet.append(ZabbixMetric(hostname, "GC.MC[" + str(pid) + "]", MC))
    packet.append(ZabbixMetric(hostname, "GC.MU[" + str(pid) + "]", MU))
    packet.append(ZabbixMetric(hostname, "GC.CCSC[" + str(pid) + "]", CCSC))
    packet.append(ZabbixMetric(hostname, "GC.CCSU[" + str(pid) + "]", CCSU))
    packet.append(ZabbixMetric(hostname, "GC.YGC[" + str(pid) + "]", YGC))
    packet.append(ZabbixMetric(hostname, "GC.YGCT[" + str(pid) + "]", YGCT))
    packet.append(ZabbixMetric(hostname, "GC.FGC[" + str(pid) + "]", FGC))
    packet.append(ZabbixMetric(hostname, "GC.FGCT[" + str(pid) + "]", FGCT))
    packet.append(ZabbixMetric(hostname, "GC.GCT[" + str(pid) + "]", GCT))


# 堆内存统计
def gccapacity(hostname, items, packet, pid):
    NGCMN, NGCMX, NGC, S0C, S1C, EC, OGCMN, OGCMX, OGC, OC, MCMN, MCMX, MC, CCSMN, CCSMX, CCSC, YGC, FGC = items[:19]
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.NGCMN[" + str(pid) + "]", NGCMN))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.NGCMX[" + str(pid) + "]", NGCMX))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.NGC[" + str(pid) + "]", NGC))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.S0C[" + str(pid) + "]", S0C))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.S1C[" + str(pid) + "]", S1C))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.EC[" + str(pid) + "]", EC))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.OGCMN[" + str(pid) + "]", OGCMN))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.OGCMX[" + str(pid) + "]", OGCMX))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.OGC[" + str(pid) + "]", OGC))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.OC[" + str(pid) + "]", OC))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.MCMN[" + str(pid) + "]", MCMN))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.MCMX[" + str(pid) + "]", MCMX))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.MC[" + str(pid) + "]", MC))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.CCSMN[" + str(pid) + "]", CCSMN))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.CCSMX[" + str(pid) + "]", CCSMX))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.CCSC[" + str(pid) + "]", CCSC))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.YGC[" + str(pid) + "]", YGC))
    packet.append(ZabbixMetric(hostname, "GCCAPACITY.FGC[" + str(pid) + "]", FGC))


#  新生代垃圾回收统计
def gcnew(hostname, items, packet, pid):
    S0C, S1C, S0U, S1U, TT, MTT, DSS, EC, EU, YGC, YGCT = items[:12]
    packet.append(ZabbixMetric(hostname, "GCNEW.S0C[" + str(pid) + "]", S0C))
    packet.append(ZabbixMetric(hostname, "GCNEW.S1C[" + str(pid) + "]", S1C))
    packet.append(ZabbixMetric(hostname, "GCNEW.S0U[" + str(pid) + "]", S0U))
    packet.append(ZabbixMetric(hostname, "GCNEW.S1U[" + str(pid) + "]", S1U))
    packet.append(ZabbixMetric(hostname, "GCNEW.TT[" + str(pid) + "]", TT))
    packet.append(ZabbixMetric(hostname, "GCNEW.MTT[" + str(pid) + "]", MTT))
    packet.append(ZabbixMetric(hostname, "GCNEW.DSS[" + str(pid) + "]", DSS))
    packet.append(ZabbixMetric(hostname, "GCNEW.EC[" + str(pid) + "]", EC))
    packet.append(ZabbixMetric(hostname, "GCNEW.EU[" + str(pid) + "]", EU))
    packet.append(ZabbixMetric(hostname, "GCNEW.YGC[" + str(pid) + "]", YGC))
    packet.append(ZabbixMetric(hostname, "GCNEW.YGCT[" + str(pid) + "]", YGCT))


# 新生代内存统计
def gcnewcapacity(hostname, items, packet, pid):
    NGCMN, NGCMX, NGC, S0CMX, S0C, S1CMX, S1C, ECMX, EC, YGC, FGC = items[:12]
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.NGCMN[" + str(pid) + "]", NGCMN))
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.NGCMX[" + str(pid) + "]", NGCMX))
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.NGC[" + str(pid) + "]", NGC))
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.S0CMX[" + str(pid) + "]", S0CMX))
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.S0C[" + str(pid) + "]", S0C))
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.S1CMX[" + str(pid) + "]", S1CMX))
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.S1C[" + str(pid) + "]", S1C))
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.ECMX[" + str(pid) + "]", ECMX))
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.EC[" + str(pid) + "]", EC))
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.YGC[" + str(pid) + "]", YGC))
    packet.append(ZabbixMetric(hostname, "GCNEWCAPACITY.FGC[" + str(pid) + "]", FGC))


# 老年代垃圾回收统计
def gcold(hostname, items, packet, pid):
    MC, MU, CCSC, CCSU, OC, OU, YGC, FGC, FGCT, GCT = items[:11]
    packet.append(ZabbixMetric(hostname, "GCOLD.MC[" + str(pid) + "]", MC))
    packet.append(ZabbixMetric(hostname, "GCOLD.MU[" + str(pid) + "]", MU))
    packet.append(ZabbixMetric(hostname, "GCOLD.CCSC[" + str(pid) + "]", CCSC))
    packet.append(ZabbixMetric(hostname, "GCOLD.CCSU[" + str(pid) + "]", CCSU))
    packet.append(ZabbixMetric(hostname, "GCOLD.OC[" + str(pid) + "]", OC))
    packet.append(ZabbixMetric(hostname, "GCOLD.OU[" + str(pid) + "]", OU))
    packet.append(ZabbixMetric(hostname, "GCOLD.YGC[" + str(pid) + "]", YGC))
    packet.append(ZabbixMetric(hostname, "GCOLD.FGC[" + str(pid) + "]", FGC))
    packet.append(ZabbixMetric(hostname, "GCOLD.FGCT[" + str(pid) + "]", FGCT))
    packet.append(ZabbixMetric(hostname, "GCOLD.GCT[" + str(pid) + "]", GCT))


# 老年代内存统计
def gcoldcapacity(hostname, items, packet, pid):
    OGCMN, OGCMX, OGC, OC, YGC, FGC, FGCT, GCT = items[:9]
    packet.append(ZabbixMetric(hostname, "GCOLDCAPACITY.OGCMN[" + str(pid) + "]", OGCMN))
    packet.append(ZabbixMetric(hostname, "GCOLDCAPACITY.OGCMX[" + str(pid) + "]", OGCMX))
    packet.append(ZabbixMetric(hostname, "GCOLDCAPACITY.OGC[" + str(pid) + "]", OGC))
    packet.append(ZabbixMetric(hostname, "GCOLDCAPACITY.OC[" + str(pid) + "]", OC))
    packet.append(ZabbixMetric(hostname, "GCOLDCAPACITY.YGC[" + str(pid) + "]", YGC))
    packet.append(ZabbixMetric(hostname, "GCOLDCAPACITY.FGC[" + str(pid) + "]", FGC))
    packet.append(ZabbixMetric(hostname, "GCOLDCAPACITY.FGCT[" + str(pid) + "]", FGCT))
    packet.append(ZabbixMetric(hostname, "GCOLDCAPACITY.GCT[" + str(pid) + "]", GCT))


# 元数据空间统计
def gcmetacapacity(hostname, items, packet, pid):
    MCMN, MCMX, MC, CCSMN, CCSMX, CCSC, YGC, FGC, FGCT, GCT = items[:11]
    packet.append(ZabbixMetric(hostname, "GCMETACAPACITY.MCMN[" + str(pid) + "]", MCMN))
    packet.append(ZabbixMetric(hostname, "GCMETACAPACITY.MCMX[" + str(pid) + "]", MCMX))
    packet.append(ZabbixMetric(hostname, "GCMETACAPACITY.MC[" + str(pid) + "]", MC))
    packet.append(ZabbixMetric(hostname, "GCMETACAPACITY.CCSMN[" + str(pid) + "]", CCSMN))
    packet.append(ZabbixMetric(hostname, "GCMETACAPACITY.CCSMX[" + str(pid) + "]", CCSMX))
    packet.append(ZabbixMetric(hostname, "GCMETACAPACITY.CCSC[" + str(pid) + "]", CCSC))
    packet.append(ZabbixMetric(hostname, "GCMETACAPACITY.YGC[" + str(pid) + "]", YGC))
    packet.append(ZabbixMetric(hostname, "GCMETACAPACITY.FGC[" + str(pid) + "]", FGC))
    packet.append(ZabbixMetric(hostname, "GCMETACAPACITY.FGCT[" + str(pid) + "]", FGCT))
    packet.append(ZabbixMetric(hostname, "GCMETACAPACITY.GCT[" + str(pid) + "]", GCT))


#  总结垃圾回收统计
def gcutil(hostname, items, packet, pid):
    S0, S1, E, O, M, CCS, YGC, YGCT, FGC, FGCT, GCT = items[:12]
    packet.append(ZabbixMetric(hostname, "GCUTIL.S0[" + str(pid) + "]", S0))
    packet.append(ZabbixMetric(hostname, "GCUTIL.S1[" + str(pid) + "]", S1))
    packet.append(ZabbixMetric(hostname, "GCUTIL.E[" + str(pid) + "]", E))
    packet.append(ZabbixMetric(hostname, "GCUTIL.O[" + str(pid) + "]", O))
    packet.append(ZabbixMetric(hostname, "GCUTIL.M[" + str(pid) + "]", M))
    packet.append(ZabbixMetric(hostname, "GCUTIL.CCS[" + str(pid) + "]", CCS))
    packet.append(ZabbixMetric(hostname, "GCUTIL.YGC[" + str(pid) + "]", YGC))
    packet.append(ZabbixMetric(hostname, "GCUTIL.YGCT[" + str(pid) + "]", YGCT))
    packet.append(ZabbixMetric(hostname, "GCUTIL.FGC[" + str(pid) + "]", FGC))
    packet.append(ZabbixMetric(hostname, "GCUTIL.FGCT[" + str(pid) + "]", FGCT))
    packet.append(ZabbixMetric(hostname, "GCUTIL.GCT[" + str(pid) + "]", GCT))


try:
    opts, args = getopt.getopt(sys.argv[1:], "p:n:")
except getopt.GetoptError:
    print("Usage:get-jvm-gc.py -p <process id> -n <host name>")
    sys.exit(2)

for opt, arg in opts:
    if opt == '-p':
        pid = arg
    if opt == '-n':
        zbhost = arg

if JAVA_HOME == '':
    state = 0
    packet = [ZabbixMetric(zbhost, 'jvm_state', state),
              ZabbixMetric(zbhost, 'jvm_errstr', '系统未配置JAVA_HOME')]
    result = ZabbixSender(zabbix_port=zbport, zabbix_server=zbserver).send(packet)
    sys.exit(1)

state = 1
packet = [ZabbixMetric(zbhost, ':jvm_state', state)]

for method in methods:
    # print("method" + method)

    cmd = JAVA_HOME + "/bin/jstat -" + method + " " + str(pid) + "|" + " awk 'NR==2 {print $0}'"
    # print("cmd:"+cmd)
    r = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = r.communicate()
    res = out + err
    # print("DEBUG: RES: " + res)

    if len(err) > 0:
        state = 0
        packet = [ZabbixMetric(zbhost, 'jvm_state', state),
                  ZabbixMetric(zbhost, 'jvm_errstr', err)]
        result = ZabbixSender(zabbix_port=zbport, zabbix_server=zbserver).send(packet)
        sys.exit(1)

    items = res.split()
    # get jvm data
    if method == 'gc':
        gc(zbhost, items, packet, pid)
    elif method == 'gccapacity':
        gccapacity(zbhost, items, packet, pid)
    elif method == 'gcnew':
        gcnew(zbhost, items, packet, pid)
    elif method == 'gcnewcapacity':
        gcnewcapacity(zbhost, items, packet, pid)
    elif method == 'gcold':
        gcold(zbhost, items, packet, pid)
    elif method == 'gcoldcapacity':
        gcoldcapacity(zbhost, items, packet, pid)
    elif method == 'gcmetacapacity':
        gcmetacapacity(zbhost, items, packet, pid)
    elif method == 'gcutil':
        gcutil(zbhost, items, packet, pid)

# send data to zabbix-server
result = ZabbixSender(zabbix_port=zbport, zabbix_server=zbserver).send(packet)
# print(result)
print("all complete!")
