# -*- coding: utf-8-*-

import urllib2, urllib, sys, random, time
import os, re, StringIO
import datetime



##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s

##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}
    
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如>
        key=sz.group('name')#去除&;后entity,如>为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr

def repalce(s,re_exp,repl_string):
    return re_exp.sub(repl_string,s)

def main(timeout):

    starttime = time.time()
    org_gxrb_url = 'http://www.gxrb.com.cn/'

    f = open(r'UA_list.txt','rb')
    user_agents_list = []
    for xline in f.readlines():
        user_agents_list.append(xline)
    f.close()

    starttime = time.time()

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

    user_agent = random.choice(user_agents_list).replace('\r\n','').replace('\r','').replace('\n','')
    headers = { 'User-Agent' : user_agent , "Cache-Control" : "no-cache" , "Connection" : "keep-alive", "Referer": org_gxrb_url}

    #o_gxrb_url = 'http://paper.people.com.cn/gxrb/html/2014-06/22/node_5.htm'
    req = urllib2.Request(str(org_gxrb_url), headers=headers)
    try:
        fin = urllib2.urlopen(req,timeout=timeout).read()
    except:
        print '[-] wget error' , org_gxrb_url 
        raw_input('check')
        #sys.exit()
        #time.sleep(1)

    new_re = re.compile(r'URL=(.*?)"',re.DOTALL).findall(fin)
    o_gxrb_url = 'http://www.gxrb.com.cn/' + new_re[0]
    #http://www.gxrb.com.cn/html/2014-06/22/node_5.htm

    print 'o_gxrb_url:', o_gxrb_url
    #raw_input()

    #today = datetime.datetime.now().strftime('%Y-%m-%d')

    today_new_re = re.compile(r'html\/(.*?)\-(.*?)\/(.*?)\/',re.DOTALL).findall(new_re[0])
    today = today_new_re[0][0] + today_new_re[0][1] + today_new_re[0][2]
    print 'today', today
    #raw_input()

    savetxtpath = '广西日报' + '\\' + str(today)
    #z:\long_an\20140620\
    savetxtpath = savetxtpath.decode('utf-8').encode('gbk')

    if not os.path.isdir(savetxtpath):
        os.makedirs(savetxtpath)

    user_agent = random.choice(user_agents_list).replace('\r\n','').replace('\r','').replace('\n','')
    headers = { 'User-Agent' : user_agent , "Cache-Control" : "no-cache" , "Connection" : "keep-alive", "Referer": o_gxrb_url}

    #o_gxrb_url = 'http://paper.people.com.cn/gxrb/html/2014-06/20/node_1921.htm'  #etc...
    req = urllib2.Request(str(o_gxrb_url), headers=headers)
    try:
        fin = urllib2.urlopen(req,timeout=timeout).read()
    except:
        print '[-] wget error' , o_gxrb_url 
        raw_input('check')
        #sys.exit()
        #time.sleep(1)

    #new_re = re.compile(r'<li><a href=(.*?) class="blue".+?<li class="one"><a href=(.*?) class="blue"',re.DOTALL).findall(fin) #etc...

    new_re = re.compile(r'<LI><a id=pageLink href=(.*?)>',re.DOTALL).findall(fin)
    #http://www.gxrb.com.cn/html/2014-06/22/node_7.htm #for re_

    #o_day_url = 'http://www.gxrb.com.cn/html/2014-06/22/'
    o_day_url = 'http://www.gxrb.com.cn/html/' + today_new_re[0][0] + '-' + today_new_re[0][1] + '/' + today_new_re[0][2] + '/'
    print 'o_day_url:', o_day_url
    #raw_input()

    gxrb_list = []
    #gxrb_list.append(o_gxrb_url)
    for n_link in new_re:
        #print n_link
        gxrb_list.append(o_day_url + n_link)
        #gxrb_list.append(o_day_url + 'nbs' + n_link)

    #for n in gxrb_list:
    #    print n
    #raw_input()

    #o_day_url = 'https://webcache.googleusercontent.com/search?q=cache:' + o_day_url
    #enable google
    for n_link in gxrb_list:
        #n_link = 'https://webcache.googleusercontent.com/search?q=cache:' + n_link
        #enable google
        user_agent = random.choice(user_agents_list).replace('\r\n','').replace('\r','').replace('\n','')
        #user_agent = "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
        headers = { 'User-Agent' : user_agent , "Cache-Control" : "no-cache" , "Connection" : "keep-alive", "Referer": org_gxrb_url}
        #http://www.gxrb.com.cn/html/2014-06/22/node_5.htm
        req = urllib2.Request(str(n_link), headers=headers)
        try:
            fin = urllib2.urlopen(req,timeout=timeout).read()
        except:
            print '[-] wget1 error' , n_link 
            #raw_input('check')
            continue
        new_re_title = re.compile('<font style="padding-left:5px;">(.*?)</font>',re.DOTALL).findall(fin)
        the_title = new_re_title[0].decode('utf-8').encode('gbk').replace('\\','_').replace('*','_').replace('\/','_').replace('/','_').replace(':','_').replace('\*','_').replace('\|','_').replace('|','_').replace('?','_').replace('\?','_').replace('\"','_').replace('"','_').replace('\<','_').replace('<','_').replace(' ','').replace('\t','').replace('\r\n','').replace('\r','').replace('\n','').replace('·','.')
        print 'this title:', filter_tags(the_title)
        save_title_path = savetxtpath + '\\' + filter_tags(the_title)
        if not os.path.isdir(save_title_path):
            os.makedirs(save_title_path)
        time.sleep(1)
        #raw_input()


        new_re_link2 = re.compile(r'shape="polygon" href="(.*?)">',re.DOTALL).findall(fin)
        for m_link in new_re_link2:
            m_link = o_day_url + m_link
            print 'm_link:', m_link
            #
            user_agent = random.choice(user_agents_list).replace('\r\n','').replace('\r','').replace('\n','')
            headers = { 'User-Agent' : user_agent , "Cache-Control" : "no-cache" , "Connection" : "keep-alive", "Referer": org_gxrb_url}
            req = urllib2.Request(str(m_link), headers=headers)
            try:
                fin = urllib2.urlopen(req,timeout=timeout).read()
            except:
                print '[-] wget2 error' , m_link 
                #raw_input('check')
                continue

            new_re2 = re.compile(r'<h1>(.*?)</h1>.+?28px\;">(.*?)</span>.+?<founder-content>(.*?)</founder-content>',re.DOTALL).findall(fin)
            print 'go title', len(new_re2)
            for n in new_re2:
                print 'title1:', filter_tags(n[0]).decode('utf-8').encode('gbk')
                print 'title2:', filter_tags(n[1]).decode('utf-8').encode('gbk')
                print 'summary:', filter_tags(n[2]).decode('utf-8').encode('gbk')
                filename = filter_tags(n[0]).decode('utf-8').encode('gbk') + '_' + filter_tags(n[1]).decode('utf-8').encode('gbk')
                filename = filename.replace('\\','_').replace('*','_').replace('\/','_').replace('/','_').replace(':','_').replace('\*','_').replace('\|','_').replace('|','_').replace('?','_').replace('\?','_').replace('\"','_').replace('"','_').replace('\<','_').replace('<','_').replace('\t','_').replace('\r\n','_').replace('\r','_').replace('\n','_').replace('·','.') + '.txt'
                savefilename = os.path.join(save_title_path, filename)
                f = open(savefilename , 'wb')
                f.write(filter_tags(n[2]))
                f.close()
            #raw_input('check1')
        #raw_input('check')
    print 'finish times: %d seconds' % int(round(time.time()-starttime))


if __name__ == "__main__":
    timeout = 5  #下载超时
    main(timeout)
