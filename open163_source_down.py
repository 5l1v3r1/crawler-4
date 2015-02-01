# -*- coding: utf-8-*-
#for windows


import urllib2, urllib, sys, random, time
import os, re
import datetime

timeout = 10 #download for timeout
starttime = time.time()
try_time = 3
mov1_url = 'http://open.163.com/special/Khan/khstatistics.html'
#可汗学院公开课：统计学

starttime = time.time()

'''
f = open(r'UA_list.txt','rb')
user_agents_list = []
for xline in f.readlines():
    user_agents_list.append(xline)
f.close()

user_proxy = "http://127.0.0.1:88" 
#user_proxy = random.choice(user_proxys_list)
enable_proxy = False     ##False
#enable_proxy = True     ##False
proxy_handler = urllib2.ProxyHandler({"http" : user_proxy})
null_proxy_handler = urllib2.ProxyHandler({})

if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)

urllib2.install_opener(opener)   ## set global
'''

#user_agent = random.choice(user_agents_list).replace('\r\n','').replace('\r','').replace('\n','')
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/22.0"
headers = { 'User-Agent' : user_agent , "Cache-Control" : "no-cache" , "Connection" : "keep-alive", "Referer": mov1_url}

req = urllib2.Request(str(mov1_url), headers=headers)
try:
    fin = urllib2.urlopen(req,timeout=timeout).read()
except:
    print '[-] wget error' , mov1_url 
    sys.exit('check your network, or maybe that websize was down.')

mov_list = re.compile(r'<td class="u-ctitle">.*?\[(.*?)\].*?href="(.*?)">(.*?)</a>',re.DOTALL).findall(fin)

#print type(mov_list)
#print mov_list[0]

raw_mov_url_list = []
#raw_input()
#列出视频文件名和各个视频地址

#截取某一集
cut1 = 1
no_cut = 0
cut_name = '第21集'
cut_name = cut_name.decode('utf8').encode('gbk')    #for windows CMD


for name1, mov_url2, name2 in mov_list:
    mov_name = (name1 + "_" + name2).replace(' ','_')
    if mov_url2 not in raw_mov_url_list:
        print mov_name
        print mov_url2
        raw_mov_url_list.append(mov_url2)
        ###2015-2-1
        req = urllib2.Request(str(mov_url2), headers=headers)
        try:
            fin = urllib2.urlopen(req,timeout=timeout).read()
        except:
            print '[-] wget error' , mov_url2 
            print mov_name
            #raw_input('check')
            sys.exit('check your network, or maybe that websize was down.')
            #time.sleep(1)
        mov_list2 = re.compile(r"appsrc : '(.*?)',",re.DOTALL).findall(fin)
        # 持续前一个下载，重新开始则设置空
        if cut_name in mov_name :
            no_cut = 1        
        elif no_cut == cut1 :
            no_cut = 1
        else:
            continue
        
        print '[+] downloading...'
        # 地址加上 mp4
        mov_list_single = mov_list2[0][0:-4] + "mp4"
        print 'mov_list2:' , mov_list_single

        mov_url3 = urllib2.Request(str(mov_list_single), headers=headers)
        down_num = 0
        #下载尝试3次，保存当前目录
        while down_num < try_time:
            try:
                fin = urllib2.urlopen(mov_url3,timeout=timeout).read()
                down_num = 10
            except:
                print 'retry:', down_num
                print '[-] wget error' , mov_list_single
                print mov_name
                #raw_input('[+] check.')
        if down_num < 8:pass
        else:sys.exit('check your network, or maybe that websize was down.')
                
        mov_name = mov_name + ".mp4"
        f = open(mov_name,'wb')
        f.write(fin)
        f.close()
        #raw_input('wait2')

print 'finish times: %d seconds' % int(round(time.time()-starttime))
sys.exit()

