# -*- coding: utf-8-*-
#for windows


import urllib2, urllib, sys, random, time
import os, re
import datetime

timeout = 5 #download for timeout
starttime = time.time()
xs_url = 'http://xs.dmzj.com/982/index.shtml'
#xs_url = 'http://xs.dmzj.com/1085/index.shtml'

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
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0"
headers = { 'User-Agent' : user_agent , "Cache-Control" : "no-cache" , "Connection" : "keep-alive", "Referer": xs_url}

req = urllib2.Request(str(xs_url), headers=headers)
try:
    fin = urllib2.urlopen(req,timeout=timeout).read()
except:
    print '[-] wget error' , xs_url 
    #raw_input('check')
    sys.exit('check your network, or maybe that websize was down.')
    #time.sleep(1)

#new_re = re.compile(r'"download_rtx".+?</a></span>(.*?)</li>.+?title="(.*?)">',re.DOTALL).findall(fin)
novel = re.compile(r'"download_rtx"(.*?)<div class="clearfix">',re.DOTALL).findall(fin)

#print novel[0]
#raw_input('wait...')
for o_theme_tile in novel:
    #print o_theme_tile.decode('utf-8').encode('gbk')
    novel_theme = re.compile(r'</a></span>(.*?)</li>',re.DOTALL).findall(o_theme_tile)
    print novel_theme[0].decode('utf-8').encode('gbk')
    
    f = open(r'list_novel.txt', 'ab')
    f.write(novel_theme[0].decode('utf-8').encode('gbk') + os.linesep )
    f.close()

    novel_title = re.compile(r'title="(.*?)">',re.DOTALL).findall(o_theme_tile)
    for title in novel_title:
        print title.decode('utf-8').encode('gbk')
        f = open(r'list_novel.txt', 'ab')
        f.write(title.decode('utf-8').encode('gbk') + os.linesep )
        f.close()
    f = open(r'list_novel.txt', 'ab')
    f.write( os.linesep )
    f.close()
    #raw_input('[+] check.')


print 'finish times: %d seconds' % int(round(time.time()-starttime))

