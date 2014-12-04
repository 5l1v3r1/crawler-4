# -*- coding: utf-8-*-

import urllib2, urllib, sys, random, time
import os, re, StringIO
import cookielib

#有井号的表示后面这句话是对于这一行或者这一段代码的注解
#XLS部分，复制下来保存成TXT，用以脚本解析

f = open(r'新报名花名册.txt','rb')  #打开从XLS转换好的TXT文件，内容因为有中文，文档必须用utf-8编码保存
#f = open(r'11.txt','rb')
run_times = 1
starttime = time.time()
timeout=10  #设定10秒网络延迟

for line in f.readlines():      #循环读文件，每读一行分析一行
    list_value = line.split("||")     #用两竖 || 分割每一行里每一列的数据，脚本因此而得以知道内容分割
    username = list_value[0]    #列表内的第一个内容数据， 0 在脚本里表示第一个内容
    password = list_value[1]    #第二个内容
    print 'username:', username #测试打印

    first_login_url = 'https://account.chsi.com.cn/passport/login?service=http%3A%2F%2Fwww.gfbzb.gov.cn%2Fj_spring_cas_security_check'  #登陆接口，第一次POST数据

    _cookie = cookielib.CookieJar()
    cookie = urllib2.build_opener(urllib2.HTTPCookieProcessor(_cookie))
    urllib2.install_opener(cookie)      #这一段是保存访问网页时的 cookies  脚本需要

    #user_agent = random.choice(user_agents_list).replace('\r\n','').replace('\r','').replace('\n','')
    user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.8.1.6) Gecko/20071125 Firefox/2.8 Safari/408'  #伪装浏览器UA

    headers = { 'User-Agent' : user_agent , "Cache-Control" : "no-cache" , "Connection" : "keep-alive"}
    #发送HTTP请求的头部分

    req = urllib2.Request(first_login_url, headers=headers) #封装HTTP，用于脚本
    try:
        fin = urllib2.urlopen(req,timeout=timeout).read()   #开始请求
    except:
        print '[-] wget error' , first_login_url  
        raw_input('check')  #出错返回等待
        #sys.exit() #是否退出当前运行脚本
        #time.sleep(1)  

    new_re = re.compile(r'<form id="fm1" action="(.*?)"',re.DOTALL).findall(fin)
    #这一段用正则表达式去查找本次访问网页的sessionid，必须有这个sessionid才能正确地登陆

    #这里如果网络出错，或者对方服务器挂了而没有获取到网页，这段正则表达式会出错，不过因为是半自动，故没有修改
    #具体解决方法加延迟等待，判断是否能查找到sessionid，若没有则返回重试，重试因用户而定，无人职守可设定1000次

    post_login_url = 'https://account.chsi.com.cn' + new_re[0]  #拼接成类似下面这段
    #https://account.chsi.com.cn/passport/login?service=http%3A%2F%2Fwww.gfbzb.gov.cn%2Fj_spring_cas_security_check%3Bjsessionid%3D747945FA8E9ABD3BAA4CAA7484942788

    print 'post_login_url:', post_login_url

    #username = '452126199612240319'    # 是前面开头一段 username = list_value[0] 的例子数据
    #username = '452126199602100312'
    #password = '123456'

    new_re = re.compile(r'name="lt" value="(.*?)"',re.DOTALL).findall(fin)
    #这段正则表达式则是查找本次访问网页的accesskey，必须有这个“访问密钥”才可以继续本次登陆

    lt_value = new_re[0]    #賦值
    #print 'lt_value:', lt_value    #在控制台打印查看本次密钥

    postdata = urllib.urlencode({"username" : username, "password":password, "lt": lt_value, "_eventId": "submit", "submit":"%E7%99%BB+%E5%BD%95", })
    #封装本次HTTP POST的数据 
    #这里大概详解下HTTPS下抓取不到POST数据的方法。
    #查看网页源代码，查找输入框部分的源代码，找到input部分，即是输入部分，'name'后的选项是该段需要POST的

    #例1  <input id="username" name="username" class="logininput l_login_name" tabindex="1" accesskey="n" type="text" value="" size="25"/>   这一段里 name下的选项即是 username 
    #例2  <input id="password" name="password" class="logininput l_login_password" tabindex="2" accesskey="p" type="password" value="" size="25"/>     这一段里 name下的选项即是 password
    #例3  <input name="lt" value="_c14552B47-32CC-073C-BF8F-ABAD6EF46DD4_k7B4F49B8-3158-ABC8-5A32-AEE156B55512" type="hidden">      这一段里 name下的选项即是 lt
    #例4  <input name="_eventId" value="submit" type="hidden">   这一段里 name下的选项即是 _eventId
    #例5  <input class="button01" name="submit" accesskey="l" value="登 录" tabindex="4" title="登录" type="submit">   这一段的选项是 submit 


    #找到了当前需要POST的表单的各个选项，下面找各个选项的值(value)
    #例1里，value就是该段选项需要的值，为空则一般是自己需要填的，这里填的是用户名
    #例2同上
 #例3，值是"_c14552B47-32CC-073C-BF8F-ABAD6EF46DD4_k7B4F49B8-3158-ABC8-5A32-AEE156B55512"，有多长就要填多长
    #例4，(value)值是submit
    #例5，(value)值是登陆，  这里需要说明的是，中文在发送给服务器是不认的，需要转换成 “url编码” 
    #这里的登陆在url编码后即是 %E7%99%BB+%E5%BD%95


    #找完表单的选项和值后，每一个选项和值拼接起来后用 '&' 连接
    #完毕后大概是下面这样
    #username=450123199609190313&password=123456&lt=_c1885828C-F46A-7A2F-9EAB-5FCFB2F9299A_kFA69B5AF-AED0-5F2A-189C-7D5C393B40DE&_eventId=submit&submit=%E7%99%BB+%E5%BD%95


    print postdata  #打印显示本次POST数据

    post_respo = urllib2.Request(post_login_url, data=postdata, headers=headers)    #封装HTTP

    try:
        post_response = urllib2.urlopen(post_respo,timeout=timeout) #访问Firstlogin url
        time.sleep(1)  #延迟等待一秒
    except:
        print 'wget error post_login url'
        #_error += 1
        #time.sleep(3)
        sys.exit()  #出错直接退出

#这里需要注意的是，如果是第一次查找登陆部分的表单代码，需要保存登陆后的网页测试看看是否登陆成功，用下面代码保存本次访问的网页。登陆成功一般都会在网页上显示用户名，和其他信息。
#如果登陆不成功，则返回前面找表单部分继续查找，直到查找完，确认在正确地POST后登陆成功。

#测试完毕后这段可以不要
    #f = open(r'savefisrtlogin.html','wb')  #临时保存用
    #f.write(post_response.read())
    #f.close()

##以上是解决第一步的登陆部分
######################


#在到填写注册信息的时，需要访问三个网页，地址如下
#这里理解成一般注册时候的“用户需知”即可，必须要按照顺序访问url_1，2，3的网页。
#访问完成后才可以填写
#这里已经注册填过所以跳到其他地方了，正常未填写是一步步来

    signup_url = 'http://www.gfbzb.gov.cn/wb/signupform.action?fg=1'    #url_1
    signup_url2 = 'http://www.gfbzb.gov.cn/wb/confirmbaseinfo.action'   #url 2
    signup_url3 = 'http://www.gfbzb.gov.cn/wb/xieyi!malexy.action'      #url 3

    #postdata2 = urllib.urlencode({"fg" : "1", })
    try:
        req = urllib2.Request(signup_url, headers=headers)
        fin = urllib2.urlopen(req,timeout=timeout).read()
    except:
        print 'wget error url', signup_url
        sys.exit()
    try:
        req = urllib2.Request(signup_url2, headers=headers)
        fin = urllib2.urlopen(req,timeout=timeout).read()
    except:
        print 'wget error url', signup_url2
        sys.exit()
    try:
        req = urllib2.Request(signup_url3, headers=headers)
        fin = urllib2.urlopen(req,timeout=timeout).read()
    except:
        print 'wget error url', signup_url3
        sys.exit()
    time.sleep(1)   #访问完三个网页，延迟一秒

    ###这里再次访问“填写注册”信息的url
    try:
        req = urllib2.Request(signup_url, headers=headers)
        fin = urllib2.urlopen(req,timeout=timeout).read()
    except:
        print 'wget error fin_token_url', signup_url
        #sys.exit()
#-- end get token
    try:
        new_re = re.compile(r'name="token" value="(.*?)"',re.DOTALL).findall(fin)
        token = new_re[0]
    except:
        token = 'im'        #出错未解决时随便填个

#用正则表达式显示出填写本次注册信息的 token ，理解成“访问密钥”，有这个才能填写注册。
#类似下面这段
#<input type="hidden" name="token" value="MJ585QY12M7T62PGR9IVBMHXDFK1MLCR" />
#<input type="hidden" name="token" value="IM1FGAB92A276FDP3BTV8FIJFOXUHT8O" />
#每次访问的 token 都不同

    print 'token:', token   #打印显示本次 token 给控制台



    #POST form    表单部分显示

    #list_value = line.split("||")

    #下面这段是调试部分，用列表显示出'花名册'中的内容信息，然后再按照网站需求从中选取后发送

    #来测试显示下表单部分
    #'''
    print '用户名', list_value[0].decode('utf-8').encode('gbk')
    print '密码', list_value[1].decode('utf-8').encode('gbk')
    print '姓名', list_value[2].decode('utf-8').encode('gbk')
    print '性别', list_value[3].decode('utf-8').encode('gbk')
    print '身份证号', list_value[4].decode('utf-8').encode('gbk')
    print '曾用名', list_value[5].decode('utf-8').encode('gbk')
    print '民族', list_value[6].decode('utf-8').encode('gbk')
    print '政治面貌', list_value[7].decode('utf-8').encode('gbk')
    print '宗教信仰', list_value[8].decode('utf-8').encode('gbk')
    print '常住户籍所在地', list_value[9].decode('utf-8').encode('gbk')
    print '籍贯', list_value[10].decode('utf-8').encode('gbk')
    print '毕业学校', list_value[11].decode('utf-8').encode('gbk')
    print '从业类别', list_value[12].decode('utf-8').encode('gbk')
    print '学历', list_value[13].decode('utf-8').encode('gbk')
    print '入学日期', list_value[14].decode('utf-8').encode('gbk')
    print '毕业日期', list_value[15].decode('utf-8').encode('gbk')
    print '学制', list_value[16].decode('utf-8').encode('gbk')
    print '职业资格证书', list_value[17].decode('utf-8').encode('gbk')
    print '户籍类别', list_value[18].decode('utf-8').encode('gbk')
    print '独生子女', list_value[19].decode('utf-8').encode('gbk')
    print '婚姻状况', list_value[20].decode('utf-8').encode('gbk')
    print '本人手机号', list_value[21].decode('utf-8').encode('gbk')
    print '家庭电话', list_value[22].decode('utf-8').encode('gbk')
    print '家庭住址邮编', list_value[23].decode('utf-8').encode('gbk')
    print '身高', list_value[24].decode('utf-8').encode('gbk')
    print '体重', list_value[25].decode('utf-8').encode('gbk')
    print '左眼裸视力', list_value[26].decode('utf-8').encode('gbk')
    print '右眼裸视力', list_value[27].decode('utf-8').encode('gbk')
    print '选择应征地', list_value[28].decode('utf-8').encode('gbk')
    print '参军意愿1', list_value[29].decode('utf-8').encode('gbk')
    print '参军意愿2', list_value[30].decode('utf-8').encode('gbk')
    print '家庭住址', list_value[31].decode('utf-8').encode('gbk')
    #'''

    if '高中' in list_value[13].decode('utf-8').encode('gbk'):
        #print '学历是高中'
        xueli = '70'
    else:
        #print '学历是初中'
        xueli = '80'

    # 学历是高中和初中时各个表单的选项都不同，按照实际情况修改

    print 'cc:', list_value[13].decode('utf-8').encode('gbk')
    #raw_input('wait')
    
    #rxrq = list_value[14].decode('utf-8').encode('gbk')
    rxrq = list_value[14].decode('utf-8').encode('utf-8')
    byrq = list_value[15].decode('utf-8').encode('utf-8')
    yxmc = list_value[11].decode('utf-8').encode('utf-8')
    xz = list_value[16].decode('utf-8').encode('utf-8')
    brlxdh = list_value[21].decode('utf-8').encode('utf-8')
    jtlxdh = list_value[22].decode('utf-8').encode('utf-8')
    xjtdzdetail = list_value[31].decode('utf-8').encode('utf-8')
    xjtdzpost = list_value[23].decode('utf-8').encode('utf-8')
    sg = list_value[24].decode('utf-8').encode('utf-8')
    tz = list_value[25].decode('utf-8').encode('utf-8')
    zysl = list_value[26].decode('utf-8').encode('utf-8')
    yysl = list_value[27].decode('utf-8').encode('utf-8')
    jsdj = '无'.decode('gbk').encode('utf-8')

    if xueli == '80': #初中
        fin_postdata = urllib.urlencode({'cym' : '', 'mz':'08', 'zzmm': '03', 'zjxy':'', \
        'czfkszdprovice':'17471', 'czfkszdcity':'17475', 'czfkszdxq':'17507', 'czfkszdxz':'925291823', \
        'jgprov':'17471', 'jgcity':'17475', 'jgdist':'17507', 'career':'01', 'cc':xueli, \
        'zymc': '', 'xxxs': '' , 'xyqk': '', 'rxrq': rxrq, 'byrq':byrq, 'yxmc':yxmc, \
        'yxszdprov': '', 'yxszdcity':'', 'yxszdqxdm':'', 'yxszdtown':'', 'yxszd':'', 'yxszdpost':'', \
        'xh':'', 'nianji':'', 'bh':'', 'xz':xz,  'jsdj': jsdj, 'hjlx':'02', 'dszn':'0', 'hyzk':'02', \
        'brlxdh': brlxdh, 'jtlxdh':jtlxdh, 'xjtdzprovince':'17471', 'xjtdzcity':'17475', \
        'xjtdzqx':'17507', 'xjtdzdetail':xjtdzdetail , 'xjtdzpost': xjtdzpost, 'sg':sg , 'tz':tz, \
        'zysl':zysl, 'yysl':yysl, 'yzdtype':'1', 'sydprovince':'17471', 'sydcity':'17475', \
        'syddist':'17507', 'sydtown':'925291823', 'yxprovince':'', 'yxcity':'', 'yxdist':'', \
        'yxtown':'', 'cjyy':'01', 'cjyy2':'01', '__checkbox_zhcj':'true', 'healthavaliable':'1', \
        'unavaliablereason':'', 'struts.token.name':'token', 'token':token , 
        })
    elif xueli == '70': #高中
        #rxrq = '2011.09.01'
        #byrq = '2014.07.01'
        fin_postdata = urllib.urlencode({'cym' : '', 'mz':'08', 'zzmm': '03', 'zjxy':'', \
        'czfkszdprovice':'17471', 'czfkszdcity':'17475', 'czfkszdxq':'17507', 'czfkszdxz':'925291823', \
        'jgprov':'17471', 'jgcity':'17475', 'jgdist':'17507', 'career':'01', 'cc':xueli, \
        'zymc': '', 'xxxs': '' , 'xyqk': 'BYS', 'rxrq': rxrq, 'byrq':byrq, 'yxmc':yxmc, \
        'yxszdprov': '', 'yxszdcity':'', 'yxszdqxdm':'', 'yxszdtown':'', 'yxszd':'', 'yxszdpost':'', \
        'xh':'', 'nianji':'', 'bh':'', 'xz':xz,  'jsdj': jsdj, 'hjlx':'02', 'dszn':'0', 'hyzk':'02', \
        'brlxdh': brlxdh, 'jtlxdh':jtlxdh, 'xjtdzprovince':'17471', 'xjtdzcity':'17475', \
        'xjtdzqx':'17507', 'xjtdzdetail':xjtdzdetail , 'xjtdzpost': xjtdzpost, 'sg':sg , 'tz':tz, \
        'zysl':zysl, 'yysl':yysl, 'yzdtype':'1', 'sydprovince':'17471', 'sydcity':'17475', \
        'syddist':'17507', 'sydtown':'925291823', 'yxprovince':'', 'yxcity':'', 'yxdist':'', \
        'yxtown':'', 'cjyy':'01', 'cjyy2':'01', '__checkbox_zhcj':'true', 'healthavaliable':'1', \
        'unavaliablereason':'', 'struts.token.name':'token', 'token':token , 
        })
        
##上面表单部分过于繁杂就略过，详细查看 first login url 部分的例12345，大致相同


    post_fin_url = 'http://www.gfbzb.gov.cn/wb/dosignupaction.action'

    headers = { 'User-Agent' : user_agent , "Cache-Control" : "no-cache" , "Connection" : "keep-alive", "Referer": "http://www.gfbzb.gov.cn/wb/signupform.action?fg=1" }

    post_fin_respo = urllib2.Request(post_fin_url, data=fin_postdata, headers=headers)
#封装后发送
    try:
        post_response = urllib2.urlopen(post_fin_respo,timeout=timeout)
        time.sleep(1)
    except:
        print 'wget error post_fin_url', post_fin_url
        #sys.exit()

#发送表单完毕，用下面代码保存在本地硬盘，用户查看是否成功地保存了注册信息，


    filename = list_value[2].decode('utf-8').encode('gbk') + '.html'
    f = open(filename,'wb')
    f.write(fin)
    f.close()

    print 'ok times', run_times
    run_times += 1
    #time.sleep(20)     #完成一次循环填表单后 延迟等待 秒。
    #raw_input('wait')

f.close()   #关闭文件句柄

print 'done'
print 'finish times: %d seconds' % int(round(time.time()-starttime))




#完毕，这样就会半自动化地填写了
