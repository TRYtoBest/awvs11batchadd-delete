#-*- coding:utf-8 -*-
import urllib2
import ssl
import json
__author="jamesj"
#localhost:3443ȫ���滻Ϊawvs���ڵķ��������˿�
username='mail@mail.com'
#�˺�����
pw='sha256���ܺ������'
#sha256���ܺ������
#��������Ϊ�������ݣ�Ȼ���Ҫ��ӵ�url�б����testawvs.txt�ļ������ڸýű������иýű���
ssl._create_default_https_context = ssl._create_unverified_context
url_login="https://localhost:3443/api/v1/me/login"
send_headers_login={
'Host': 'localhost:3443',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'Content-Type': 'application/json;charset=utf-8'
}

data_login='{"email":"'+username+'","password":"'+pw+'","remember_me":false}'
#data_login�����������ܷ�ʽΪsha256,ͨ��burpץ���ɻ�ȡ,Ҳ����ʹ��(http://tool.oschina.net/encrypt?type=2)��������м���֮�����룬�����ִ�Сд����Ӣ���ַ���
req_login = urllib2.Request(url_login,headers=send_headers_login)
response_login = urllib2.urlopen(req_login,data_login)
xauth = response_login.headers['X-Auth']
COOOOOOOOkie = response_login.headers['Set-Cookie']
print "��ǰ��֤��Ϣ����\r\n cookie : %r  \r\n X-Auth : %r  "%(COOOOOOOOkie,xauth)
send_headers2={	
	'Host':'localhost:3443',
	'Accept': 'application/json, text/plain, */*',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Content-Type':'application/json;charset=utf-8',
	'X-Auth':xauth,
	'Cookie':COOOOOOOOkie
	}
#���ϴ���ʵ�ֵ�¼����ȡcookie����У��ֵ
def add_exec_scan():
	url="https://localhost:3443/api/v1/targets"
	try:
		urllist=open('testawvs.txt','r')#����Ҫ��ӵ�url�б�
		formaturl=urllist.readlines()
		for i in formaturl:
			target_url='http://'+i.strip()
			data='{"description":"222","address":"'+target_url+'","criticality":"10"}'
			#data = urllib.urlencode(data)����ʹ��json��ʽ���Բ������
			req = urllib2.Request(url,headers=send_headers2)
			response = urllib2.urlopen(req,data)
			jo=json.loads(response.read())
			target_id=jo['target_id']#��ȡ��Ӻ������ID
			#print target_id
	#���ϴ���ʵ���������

			url_scan="https://localhost:3443/api/v1/scans"
			headers_scan={
	'Host': 'localhost:3443',
	'Accept': 'application/json, text/plain, */*',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding': 'gzip, deflate, br',
	'Content-Type': 'application/json;charset=utf-8',
	'X-Auth':xauth,
	'Cookie':COOOOOOOOkie,
			}
			data_scan='{"target_id":'+'\"'+target_id+'\"'+',"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false},"ui_session_id":"66666666666666666666666666666666"}'
			req_scan=urllib2.Request(url_scan,headers=headers_scan)
			response_scan=urllib2.urlopen(req_scan,data_scan)
			print response_scan.read()+"��ӳɹ���"
	#���ϴ���ʵ����������ɨ��
		urllist.close()
	except Exception,e:
		print e

def count():
	url_count="https://localhost:3443/api/v1/notifications/count"
	req_count=urllib2.Request(url_count,headers=send_headers2)
	response_count=urllib2.urlopen(req_count)
	print "��ǰ����%r��֪ͨ��" % json.loads(response_count.read())['count']
	print "-" * 50
	print "�Ѵ�����������"
	url_info="https://localhost:3443/api/v1/scans"
	req_info=urllib2.Request(url_info,headers=send_headers2)
	response_info=urllib2.urlopen(req_info)
	all_info = json.loads(response_info.read())
	num = 0
	for website in all_info.get("scans"):
		num+=1
		print website.get("target").get("address")+" \r\n target_id:"+website.get("scan_id")
	print "�� %r��ɨ������" % num
		#count()
#scan��target��notification��
def del_scan():
	url_info="https://localhost:3443/api/v1/scans"
	req_info=urllib2.Request(url_info,headers=send_headers2)
	response_info=urllib2.urlopen(req_info)
	all_info = json.loads(response_info.read())
	counter = 0
	for website in all_info.get("scans"):
		#if (website.get("target").get("description"))== "222":
		url_scan_del="https://localhost:3443/api/v1/scans/"+str(website.get("scan_id"))
		req_del = urllib2.Request(url_scan_del,headers=send_headers2)
		req_del.get_method =lambda: 'DELETE'
		response_del = urllib2.urlopen(req_del)
		counter = counter+1
		print "�Ѿ�ɾ����%r��!" %  counter
#del_scan()			#ͨ�������ж��Ƿ�ʹ��ɨ�������ɨ������ӵ�ʱ������description=��222��
def del_targets():
	url_info="https://localhost:3443/api/v1/targets"
	req_info=urllib2.Request(url_info,headers=send_headers2)
	response_info=urllib2.urlopen(req_info)
	all_info = json.loads(response_info.read())
	for website in all_info.get("targets"):
		if (website.get("description"))== "222":
			url_scan_del="https://localhost:3443/api/v1/targets/"+str(website.get("target_id"))
			req_del = urllib2.Request(url_scan_del,headers=send_headers2)
			req_del.get_method =lambda: 'DELETE'
			response_del = urllib2.urlopen(req_del)
			print "ok!"	
#del_targets()
if __name__== "__main__":
	print "*" * 20
	count()
	print "1��ʹ��testawvs.txt���ɨ������ִ��������1��Ȼ��س�\r\n2��ɾ������ʹ�øýű���ӵ�����������2��Ȼ��س�\r\n3��ɾ����������������3��Ȼ��س�\r\n4���鿴�Ѵ�������������4��Ȼ��س�\r\n"
	choice = raw_input(">")
#	print type(choice)
	if choice =="1":
		add_exec_scan()
		count()
	elif  choice =="2":
		del_targets()
		count()
	elif  choice =="3":
		del_scan()
		count()
	elif  choice =="4":
		del_scan()
		count()
	else:
		print "������1��2��3��4ѡ��"
		
#��ͼ��ע����Ϣ��ɾ��֪ͨ����	
"""	
	counter= 0
	for website in all_info.get("notifications"):
		if (website["data"].get("address")== "www.ly.com"):
			counter = counter + 1
			url_del = "https://localhost:3443/api/v1/scans/"+str(website["data"].get("scan_id"))
			print url_del#print url_del
			req_del = urllib2.Request(url_del,headers=send_headers2)
			 #DELETE����
			try:
				req_del.get_method = lambda:"DELETE"
				response1 = urllib2.urlopen(req_del)
				
			except:
				print "error"
				continue
	print counter
			#print response1.read()
	#for address in need_info["address"]
	#	if address
del_all()
"""