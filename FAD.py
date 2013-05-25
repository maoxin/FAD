#coding:utf-8
import urllib2, cookielib, re, os

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)


account = "userid=maox12&userpass=Myahoo445&submit1=%B5%C7%C2%BC"
url_login = "https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp"
url_all_index = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?language=cn"


def login_index():
    urllib2.urlopen(url_login, account)
    index = urllib2.urlopen(url_all_index)
    index = tidy_main_index(index)
    
    return index


def new(index):
    for course in index:
        new = False
        for i in range(2, 5):
            if course[i] != "0":
                new = True
                break
        if new == True:
            print 'Course Name:',           unicode(course[1], 'utf-8')
            if course[2] != '0':
                print 'Unhanded works:',    course[2]
            if course[3] != '0':
                print 'Unread bulletins:',  course[3]
            if course[4] != '0':
                print 'New Files:',         course[4]
            print '\n' 
    


def new_bulletins(index):
    for course in index:
        if course[3] != '0':
            print unicode(course[1], 'utf-8')



def new_download(index):
    count = 0
    
    for course in index:
        if course[4] != '0':  
            count_one_piece = 0
            download_url   = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/download.jsp?course_id=%d" % int(course[0])
            download_index = urllib2.urlopen(download_url)
            download_index = tidy_index_download(download_index)
        
            print unicode(course[1], 'utf-8') ,"miss you!!\n"
            for item in download_index:
                if item[4] == '新文件':
                    if not download(course, item):
                        count_one_piece += 1
                        count += 1
                    else: pass
                
                else:pass
            
            print "\n*****************************\n"
            print unicode("You pick up %d files in %s!!", 'utf-8') % (count_one_piece, course[1])
            print "\n*****************************\n"
            
    print unicode("\n***************下载已完成，卡卡***************\n", 'utf-8')
    print ("********You pick up %d files in all!!********") % count
                            


def tidy_index(index, pat):
    filter_purify_1 = r'&nbsp;'
    filter_purify_2 = r'<font.*?>(.*?)</font>'
    pat_purify_1 = re.compile(filter_purify_1)
    pat_purify_2 = re.compile(filter_purify_2)
    
    line_all = ''
    for line in index:
        line_all+=line.strip()
    # 去空格以便正则检测
    
    line_all = pat_purify_1.sub('', line_all)
    line_all = pat_purify_2.sub(r'\1', line_all)
    index = pat.findall(line_all)
    
    return index


def tidy_main_index(index):
    filter_extract = r'<a href=\".+?\?course_id=([0-9]+?)\".*?>(.+?)\(.+?</a>.+?>([0-9]+?)</span>个未交作业.+?([0-9]+?)</span>个未读公告.+?([0-9]+?)</span>个新文件'
    # in find_all, (0) is course number, (1) is course name, (2) is unhanded works, (3) is unread bulletins, (4) is new files.
    
    pat = re.compile(filter_extract)
    
    
    return tidy_index(index, pat)
    
    
def tidy_index_download(index):
    filter_extract = r'<!--.+?\"download_locate.jsp\?.+?(\.[^\.]+?)&id=[0-9]+?\".*?<.+?href=\"(.+?)\".*?>(.*?)</a></td><td .+?>.*?</td><td .+?>(.*?)</td><td .+?>.*?</td><td .+?>(.*?)</td>'
    # in find_all, (0) for file format, (1)for address for downloading, (2)for file name, (3) for file size, (4) for check new.
    pat = re.compile(filter_extract)
    
    return tidy_index(index, pat)
    

def download(course, item):
    exist = False
    file_name = '/Users/apple/Downloads/subject_download/%s/%s%s' % (course[1], item[2], item[0])
    
    try:
        file = open(file_name)
        file.close()
        
        exist = True
        
    except IOError:
        try:
            file = open(file_name, 'wb')
        except IOError:
            file = open(file_name_second, 'wb')
            
        print "\"", unicode(item[2], 'utf-8'), "\"", "to be download: \n"
        print unicode("-*-勇敢的少年请耐心，少女默默祈祷中-*-", 'utf-8')
        
        d_url = "http://learn.tsinghua.edu.cn" + item[1]
        temp = urllib2.urlopen(d_url)
        file.write(temp.read())
        file.close()
        
        print "\n" , "Bingo!!", "\n"
        
    return exist
        




def build_library(index):
    for course in index:
        make_directory = "mkdir /Users/apple/Downloads/subject_download/%s" % course[1]
        os.system(make_directory)
        




# new(login_index())    
# build_library(login_index())
new_download(login_index())
# new_bulletins(login_index())






# a log record what I did is needed.
# we should save a duplicate of bulletin.
    