#encoding=utf-8
import os
import sys
import serial  
import time
import requests
import json
import imp
import thread
import threading
from struct import *

#Yeelink接口相关信息
api_url='http://api.yeelink.net/v1.0'
api_key='your_api_key'
api_headers={'U-ApiKey':api_key,'content-type': 'application/json'}

#设备与传感器ID
DeviceID = 'yourID'
PM1_SensorID = 'yourID'
PM2_5_SensorID = 'yourID'
PM10_SensorID = 'yourID'
PM1_CF_SensorID = 'yourID'
PM2_5_CF_SensorID  ='yourID'
PM10_CF_SensorID = 'yourID'

# 打开串口  
ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=2.0)
print "Serial Connected"

#从端口读取数据
def getdata(port):
	data = b''
	while True:
		ch1 = port.read()
		if ch1 == b'\x42':
			ch2 = port.read()
			if ch2 == b'\x4d':
				data += ch1 + ch2
				data += port.read(30)
				return data

#上传数据到Yeelink的一个方法
def upload(device, sensor, data):
	url=r'%s/device/%s/sensor/%s/datapoints' % (api_url,device,sensor)
	strftime=time.strftime("%Y-%m-%dT%H:%M:%S")
	data={"timestamp":strftime , "value": data}
	res=requests.post(url,headers=api_headers,data=json.dumps(data),timeout=30)
	if res.status_code != 200:
		return False
	else:
		return True

def main(): 
	flag = 1
	while flag > 0:  
		recv = getdata(ser)
		print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		print len(recv), "Bytes in total:",
		tmp = recv
		datas = unpack('>hhhhhhhhhhhhhhhh', tmp)
		
		os.system('clear') 
		print('\n====== PMS5003 ========\n'
			'PM1.0(CF=1): {}\n'
			'PM2.5(CF=1): {}\n'
			'PM10 (CF=1): {}\n'
			'PM1.0 (STD): {}\n'
			'PM2.5 (STD): {}\n'
			'PM10  (STD): {}\n'
			'>0.3um     : {}\n'
			'>0.5um     : {}\n'
			'>1.0um     : {}\n'
			'>2.5um     : {}\n'
			'>5.0um     : {}\n'.format(datas[3], datas[4], datas[5], datas[6], datas[7], datas[8], datas[9], datas[10], datas[11], datas[12], datas[13],))
		print upload(DeviceID, PM1_SensorID, datas[6])
		monitor = upload(DeviceID, PM2_5_SensorID, datas[7])
		if monitor == False:
			flag = flag + 1
		print upload(DeviceID, PM10_SensorID, datas[8])
		print upload(DeviceID, PM1_CF_SensorID, datas[3])
		print upload(DeviceID, PM2_5_CF_SensorID, datas[4])
		print upload(DeviceID, PM10_CF_SensorID, datas[5])
		flag = flag - 1
		ser.flushInput()
		time.sleep(0.1)  


if __name__ == '__main__':  
	try:  
		main()  
	except KeyboardInterrupt:  
		if ser != None:  
			ser.close()
