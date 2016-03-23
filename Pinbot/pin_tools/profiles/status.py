# coding: utf-8

import hotshot.stats
import sys

"""
使用方式：在本文件目录内，python status.py 'log文件名'
将列出各个函数的调用时间
"""

if __name__ == '__main__':
    if len(sys.argv):
        stats = hotshot.stats.load(sys.argv[1])
        stats.sort_stats('time')
        stats.print_stats()
