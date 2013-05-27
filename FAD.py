#coding:utf-8
import urllib2, cookielib, re, os

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)


account = "userid=&userpass=&submit1=%B5%C7%C2%BC"
url_login = "https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp"
url_all_index = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?language=cn"


def login_index():
    urllib2.urlopen(url_login, account)
    index = urllib2.urlopen(url_all_index)
    index = tidy_main_index(index)
    
    return index


def new_info(index):
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
    count = 0
    for course in index:
        count += int(course[3])
    if count == 0:
        print "Ok! You have already read them.."
    else:
        print "Hey! There are %d new bulletins!\n" % count
        print "********************************\n"
        count = 0

        for course in index:
            if course[3] != '0':
                count_one_piece = 1
                bulletins_url = "http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/getnoteid_student.jsp?course_id=%d" % int(course[0])
                bulletins_index = urllib2.urlopen(bulletins_url)
                bulletins_index = tidy_index_bulletins(bulletins_index)
            
                print unicode(course[1], 'utf-8'), "want to tell you.."
                print "You have %d new bulletins..\n" % int(course[3])
            
                for item in bulletins_index:
                    if item[5] != '已读':
                        b_url = "http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/" + item[1]

                        bulletin = text_view(urllib2.urlopen(b_url)).strip()
                        print str(count_one_piece) + "."
                        print item[4] + "\n"
                        print unicode(bulletin, 'utf-8') + "\n\n"
                    
                        count_one_piece += 1
                        count += 1
        print unicode("\n***************叮！索取完成***************\n", 'utf-8')
        print ("********You get %d bulletins in all!!********") % count
                    
                    


def new_downloads(index):
    count = 0
    for course in index:
        count += int(course[4])
    # if count == 0:
        # print "Oh..There's no file left.."
    # else:
    if 1>0:
        print "You have %d new files to pick up!" % count
        count = 0
    
        for course in index:
            # if course[4] != '0':  
            if course[4] != 0:
                count_one_piece = 0
                download_url   = "http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/download.jsp?course_id=%d" % int(course[0])
                download_index = urllib2.urlopen(download_url)
                download_index = tidy_index_download(download_index)
        
                print unicode(course[1], 'utf-8') ,"miss you!!\n"
                for item in download_index:
                    # if item[4] == '新文件':
                    if 1>0:
                        if not download(course, item):
                            count_one_piece += 1
                            count += 1
                        else: pass
                
                    else:pass
            
                print "\n*****************************\n"
                print unicode("You pick up %d files in %s!!" % (count_one_piece, course[1]), 'utf-8') 
                print "\n*****************************\n"
            
        print unicode("\n***************下载已完成，卡卡***************\n", 'utf-8')
        print ("********You pick up %d files in all!!********") % count
                            


def tidy_index(index, pat):
    line_all = pure_world(index)
    # no <p>, don't worry!
    index = pat.findall(line_all)
    
    return index


def tidy_main_index(index):
    filter_extract = r'<a href=\".+?\?course_id=([0-9]+?)\".*?>(.+?)\(.+?</a>.+?>([0-9]+?)</span>个未交作业.+?([0-9]+?)</span>个未读公告.+?([0-9]+?)</span>个新文件'
    # in find_all, (0) is course number, (1) is course name, (2) is unhanded works, (3) is unread bulletins, (4) is new files.
    
    pat = re.compile(filter_extract)
    
    
    return tidy_index(index, pat)
    
    
def tidy_index_download(index):
    filter_extract = r'<!--.+?\"download_locate.jsp\?.+?(\.[^\.]+?)&id=[0-9]+?\".*?<.+?href=\"(.+?)\".*?>(.*?)</a></td><td .+?>.*?</td><td .+?>(.*?)</td><td .+?>.*?</td><td .+?>(.*?)</td>'
    # in find_all, (0) for file format, (1)for address for downloading, (2) for file name, (3) for file size, (4) for check new.
    pat = re.compile(filter_extract)
    
    return tidy_index(index, pat)
    
def tidy_index_bulletins(index):
    filter_extract = r'<tr class=\"tr(1|2)\".*?><td.*?</td><td.*?><a.*?href=\'(.*?)\'>(.*?)</a></td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td>'
    # in find_all, (0) for row number, (1) for address for bulletin, (2) for bulletin name, (3) for author, (4) for time, (5) for check new.
    pat = re.compile(filter_extract)
    return tidy_index(index, pat)

def download(course, item):
    pat_1 = re.compile(r'\(')
    pat_2 = re.compile(r'\)')
    pat_3 = re.compile(r'/')
    # file_name = pat_1.sub('\(',item[2])
    # file_name = pat_2.sub('\)', file_name)
    file_name = pat_3.sub(r':', item[2])
    
    exist = False
    file_name = '/Users/apple/Downloads/subject_downloads/%s/%s%s' % (course[1], file_name, item[0])
    # print unicode(file_name, 'utf-8')
    try:
        file = open(file_name)
        file.close()
        
        exist = True
    
        
    except IOError:
        file = open(file_name, 'wb')
            
        print "\"", unicode(item[2], 'utf-8'), "\"", "to be download: \n"
        # we can do something intersting more!! 
        print unicode("-*-勇敢的少年请耐心，少女默默祈祷中-*-", 'utf-8')
        
        d_url = "http://learn.tsinghua.edu.cn" + item[1]
        temp = urllib2.urlopen(d_url)
        file.write(temp.read())
        file.close()
        
        print "\n" , "------Bingo!!------", "\n"
        
    return exist
        




def build_library(index):
    for course in index:
        make_directory = "mkdir /Users/apple/Downloads/subject_downloads/%s" % course[1]
        os.system(make_directory)
        

def text_view(text):
    line_all = pure_world(text)
    
    pat_1 = re.compile(r'<td.*?class=\"info_title\".*?>.*?</td>')
    pat_2 = re.compile(r'(<br />|<td>|</td>|<p>|</p>)')  
    pat_3 = re.compile(r'&gt;=')
    pat_4 = re.compile(r'&lt;')
    pat_purify_1 = re.compile(r'.*?(<p.*?>|<body.*?>)')
    pat_purify_2 = re.compile(r'(</body>|</p>).*')
    pat_purify_3 = re.compile(r'.*?<tr><td.+?>标题</td><td.+?>(.*?)</td></tr><tr.*?><td.*?>(.*?)</td><td.+?<p>')
    pat_purify_4 = re.compile(r'<.*?>')
    
    line_all = pat_purify_1.sub(r'', line_all)
    line_all = pat_purify_2.sub(r'</p>', line_all)
    line_all = pat_purify_3.sub(r'<td>\1</td><td>\2</td><p>', line_all)
    line_all = pat_1.sub(r'', line_all)
    line_all = pat_2.sub(r'\n', line_all)
    line_all = pat_3.sub(r'>=', line_all)
    line_all = pat_4.sub(r'<', line_all)
    line_all = pat_purify_4.sub(r'', line_all)
      
    return line_all

def pure_world(text):
    filter_purify_1 = r'(&nbsp;|&rsquo;|&ldquo;|&rdquo;|&mdash;|&gt;|&laquo;|&bull;|&hellip;|&raquo;)'
    filter_purify_2 = r'<font.*?>(.*?)</font>'
    pat_purify_1 = re.compile(filter_purify_1)
    pat_purify_2 = re.compile(filter_purify_2)
    
    
    line_all = ''
    for line in text:
        line_all+=line.strip()

    line_all = pat_purify_1.sub('', line_all)
    line_all = pat_purify_2.sub(r'\1', line_all)
    
    
    return line_all


new_info(login_index())    
# build_library(login_index())
new_downloads(login_index())
new_bulletins(login_index())






# a log record what I did is needed.
# we should save a duplicate of bulletin.
    
