#coding:utf-8
import urllib2, cookielib, re

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

account = "userid=maox12&userpass=Myahoo445&submit1=%B5%C7%C2%BC"
url_login = "https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp"
url_all_index = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?language=cn"


def in_index():
    urllib2.urlopen(url_login, account)
    pass    # a check should be here
    index = urllib2.urlopen(url_all_index)
    index = tidy_index(index)
    
    return index


def new(index):
    for course in index:
        new = False
        for i in range(2, 5):
            if course[i] != "0":
                new = True
                break
        if new == True:
            print 'Course Name:',       unicode(course[1], 'utf-8')
            if course[2] != '0':
                print 'Unhanded works:',    course[2]
            if course[3] != '0':
                print 'Unread bulletins:',  course[3]
            if course[4] != '0':
                print 'New Files:',         course[4]
            print '\n' 
    


def download(index):
    for course in index:
        # if course[4] != '0':
        if course[1] == "中国近现代史纲要":    
            download_url = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/download.jsp?course_id=%d" % int(course[0])
            download_index = urllib2.urlopen(download_url)
            download_index = tidy_index_download(download_index)
        
            print unicode(course[1], 'utf-8') ,"miss you!!", "\n"
            for item in download_index:
                # if item[4] == '新文件':
                print "\"", unicode(item[2], 'utf-8'), "\"", "to be download: ", "\n"
                print "-----------By Maox------------"
            
                file_name = '/Users/apple/Downloads/%s%s' % (item[2], item[0])
                file_name_second = '/Users/apple/Downloads/%s%s' % (item[2][16:-13], item[0])
                # To support our history class...
                
                try:
                    file = open(file_name, 'wb')
                except IOError:
                    file = open(file_name_second, 'wb')
            
                d_url = "http://learn.tsinghua.edu.cn" + item[1]
                temp = urllib2.urlopen(d_url)
                file.write(temp.read())
                file.close()
            
                print "\n" , "Bingo!!", "\n"
                
            
def tidy_index(index):
    pat = re.compile(r'<a href=\".+?\?course_id=([0-9]+?)\".*?>(.+?)\(.+?</a>.+?>([0-9]+?)</span>个未交作业.+?([0-9]+?)</span>个未读公告.+?([0-9]+?)</span>个新文件')
    # group(0) is course number, group(1) is course name, (2) is unhanded works, (3) is unread bulletins, (4) is new files.
    
    line_all = ''
    for line in index:
        line_all+=line.strip()
    # 去空格以便正则检测
    
    index = pat.findall(line_all)
    
    return index
    
    
def tidy_index_download(index):
    filter = r'<!--.+?\"download_locate.jsp\?.+?(\.[^\.]+?)&id=[0-9]+?\".*?<.+?href=\"(.+?)\".*?>(.*?)</a></td><td .+?>.*?</td><td .+?>(.*?)</td><td .+?>.*?</td><td .+?>(.*?)</td>'
    # (0) for file format, (1)for address for downloading, (2)for file name, (3) for file size, (4) for check new.
    pat = re.compile(filter)
    
    line_all = ''
    for line in index:
        line_all+=line.strip()
    
    index = pat.findall(line_all)
    
    return index
    
# new(in_index())    
download(in_index())







# a log record what I did is needed.
# we should save a duplicate of bulletin.
    