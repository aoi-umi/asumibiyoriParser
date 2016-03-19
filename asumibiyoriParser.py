#!/usr/bin/env python
#-*-coding:utf-8-*-
import urllib
import urllib2
import codecs
import HTMLParser
import re
import os
import sys

TEMPLATE = "template.html"
ERROR = []
def write_to_file(filename, data):
    r'write to file'
    with codecs.open(filename, 'a') as out_file:
        out_file.write(data)


class AsumibiyoriParser(HTMLParser.HTMLParser):
    r'Parser for asumibiyori'
    flag = {
    "title" : False,
    "h2" : False,
    "h3" : False,
    "date s" : False,
    "txt" : False,
    }
    div_class = ''
    div_ext = 0
    div = 0
    template = ''
    content = {
    'title' : '',
    'h2' : '',
    'h3' : '',
    'date s' : '',
    'txt' : ''
    }
    

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        for f in self.flag:
            self.flag[f] = False
        for c in self.content:
            self.content[c] = ''
        self.div_class = ''
        self.div_ext = 0
        self.div = 0
        if self.template == '':
            with open(TEMPLATE, 'r') as temp:
                self.template = temp.read()

    def handle_starttag(self, tag, attrs):
        for i in self.flag:
            if self.flag[i] and not self.div_ext:
                self.content[i] += self.get_starttag_text().encode('utf-8')
                break
        if tag == 'title' or tag == 'h2' or tag == 'h3':
            self.flag[tag] = True
        elif tag == 'div':
            self.div += 1
            for name, value in attrs:
                if name == 'class' and (value == 'txt' or value == 'date s'):
                    self.div = 1
                    self.flag[value] = True
                    self.div_class = value
                if name == 'class' and value == 'ext':
                    self.div_ext = self.div

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.div_ext == self.div:
                self.div_ext = 0
            self.div -= 1
        if self.div_class != '' and self.div == 0:
            self.flag[self.div_class] = False
            self.div_class = ''
        elif  tag == 'title' or tag == 'h2' or tag == 'h3':
            self.flag[tag] = False
        for i in self.flag:
            if self.flag[i] and not self.div_ext:
                self.content[i] += '</' + tag.encode('utf-8') + '>'
                break

    def handle_data(self, data):
        for i in self.flag:
            if self.flag[i] and not self.div_ext:
                self.content[i] += data.encode('utf-8')
                break

def getImg(html, dir = '.'):
    reg = r'<img.+?src="(.+?)".*?/?>'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    #print 'img match:', len(imglist)
    for imgurl in imglist:
        try:
            imgname = imgurl[imgurl.rfind('/') + 1:]
            #print '%s->%s/%s' % (imgurl, dir, imgname)
            urllib.urlretrieve(imgurl, '%s/%s' % (dir, imgname))
        except Exception, e:
            print e

def main(url):
    r'main'
    try:
        print url + ': start'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read()
        name = url[url.rfind('/') + 1:]
        dir = os.path.join('archives', name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        parser = AsumibiyoriParser()
        parser.feed(html.decode('shift_jisx0213'))
        filename =  os.path.join(dir, 'archive_' + name + '.html')
        with open(filename, 'w'):
            pass
        getImg(parser.content['txt'], dir)
        parser.content['txt'] = re.sub(r'(<img.+?src=")[^>]+/(.+?)"','\g<1>./\g<2>"', parser.content['txt'])
        write_to_file(filename, parser.template %(parser.content['title'], parser.content['h2'], 
        parser.content['h3'], parser.content['date s'], parser.content['txt']))
    except Exception ,ex:
        ERROR.append(url + ':' + str(ex))
        print ex
    finally:
        print url + ': end'
        

PATH = "file:/E:/baiduyundownload/asumi/asumi/20.html"
URL = "http://yaplog.jp/asumibiyori/archive/"
if __name__ == '__main__':
    reg = r'^([0-9]+)(-([0-9]+))?$'
    dict = {}
    for i in range (1, len(sys.argv)):
        try:
            m = re.match(reg, sys.argv[i])
            if m:
                if m.group(3):
                    start = int(m.group(1))
                    end = int(m.group(3)) + 1
                    if start > end:
                        t = start + 1
                        start = end - 1
                        end = t
                    for r in range(start, end):
                        print r
                        dict[r] = True
                else: dict[int(m.group(0))] = True
            else:
                print '%s: %s' % (sys.argv[i], u'格式不正确')
        except Exception, ex:
            print ex
            
    print u'\n处理开始,共:', len(dict)
    for each in dict:
        main('%s%d' %(URL, each))
    print u'\n处理结束,失败: ', len(ERROR)
    for e in ERROR:
        print e
    
    