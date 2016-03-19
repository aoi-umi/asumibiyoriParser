#!/usr/bin/env python
#-*-coding:utf-8-*-
import os

os.makedirs('a/b/d')
dir = 'archives'
for i in range(1, 535):
    d = os.path.join(dir, str(i))
    if(os.path.exists(d)):
        for root, dirs, files in os.walk(d):
            if(len(files) == 0):
                print 'empty:', i

