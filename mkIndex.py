#!/usr/bin/env python
#-*-coding:utf-8-*-
import os
import re

MONTHS = {
'january' : 1,
'february' : 2,
'march' : 3,
'april' : 4,
'may' : 5,
'june' : 6,
'july' : 7,
'august' : 8,
'september' : 9,
'october' : 10,
'november' : 11,
'december' : 12
}

TEMPLATE = 'indexTemplate.html'
INDEX = 'index.html'
COLLAPSE = '<div class="side_text"><div class="icon"><img src="./images/icon.gif"><a data-toggle="collapse" href="#%s">%s</a></div><div id="%s" class="panel-collapse collapse">%s</div></div>'
DIV = '<div class="side_text"><div class="icon">&nbsp;&nbsp;<img src="./images/icon.gif"><a href="%s" target="_top">%s</a></div></div>'
#<h3>新ブログ完成記念日</h3>
#<div class="date s">January 16 [Wed], 2008, 23:10</div>
title_date_reg = r'<h3>(.+?)</h3>\n<div class="date s">(.+?)</div>'
title_date_re = re.compile(title_date_reg)

date_reg = r'([a-zA-Z]+?) ([0-9]+?) (\[[a-zA-Z]+?\]), ([0-9]+?), ([0-9]+?:[0-9]+?)'
date_re = re.compile(date_reg)
dir = 'archives'
tmp = {}
for root, dirs, files in os.walk(dir):
    try:
        for file in os.listdir(root):
            if file.endswith('.html'):
                html_path = os.path.join(root, file)
                with open(html_path, 'r') as in_file:
                    data = in_file.read()
                    list = re.findall(title_date_re, data)
                    if len(list):
                        title, date = list[0]
                        date_list = re.findall(date_re, date)
                        if len(date_list):
                            month, day, week, year, time = date_list[0]
                            l = '%s-%02d' %(year, MONTHS[month.lower()])
                            if l not in tmp:
                                tmp[l] = []
                            tmp[l].append([html_path, title])
    except Exception, ex:
        print root + ':', ex
        
sort_list = sorted(tmp.items(), key=lambda d:d[0])
data = ''
for t in sort_list:
    try:
        div = ''
        for each in t[1]:
            div += DIV %('./' + each[0].replace('\\','/'), each[1])
        collapse = COLLAPSE % (t[0], '%s(%d)' % (t[0], len(t[1])), t[0], div)
        data += collapse
    except Exception, ex:
        print ex
        
with open(TEMPLATE, 'r') as temp:
    template = temp.read()
    with open(INDEX, 'w') as index:
        index.write(template % data)

        
