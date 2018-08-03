#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os,sys,getopt



helpstr = '''
    用法：   renfilename.py -h -d path -a frontstr -b endstr -r oldstr,newstr -s [ext1,ext2,...]
            目录名为必需参数，配合其它参数实现对目录下的文件进行文件名修改操作
            -h 打印使用说明
            -d path 对该目录下的文件进行处理
            -a frontstr 增加前缀
            -b endstr  增加后缀
            -r oldstr,newstr 替换字符
            -s [ext1,ext2,....] 过滤文件类型
            -S [file1,file2,...] 过滤文件
            '''


def getlistbydir(path = '.'):
    '''返回目录下所有文件元组（绝对路径,文件名）列表，不含子目录'''

    abspath = os.path.abspath(path)
    if not os.path.exists(abspath):
        return (False,'文件/目录[{0}]不存在.'.format(path))

    filesdirlist = os.listdir(path)
    fileslist = []
    for onefile in filesdirlist:
        allpathname = os.path.join(path,onefile)
        if os.path.isfile(allpathname):
            fileslist.append((abspath,onefile))

    return (True,fileslist)


def addcharfront(frontstr,fileslist):
    '''在文件名前增加一个字符串，参数：新加的串、元组（绝对路径,文件名）列表'''
    if len(frontstr) == 0:
        return(False,'新的串不能为空.')

    for onefile in fileslist[1]:
        newfilename = os.path.join(fileslist[0],frontstr + onefile)
        oldfilename = os.path.join(filelist[0],onefil)
        os.rename(oldfilename,newfilename)
        '''重命名文件，另有 renames()可以带目录一起重命名'''

def getargvs():
    '''得到命令行参数信息，以参数选项为程序的输入输出及控制，用短选项为主'''
    optstrs = 'hd:a:b:r:s:S:'
    opts,argvs = getopt.getopt(sys.argv[1:],optstrs)
    '''
    选项说明：-h 打印使用帮助，-d dirname 目录
    opts返回两元组列表（选项、选项参数）,argvs为非格式化参数，
    getotp函数第一个参数为传入的命令行选项列表，第一个（0）为脚本本身，故从第2个（1）开始，
    第二个参数为程序使用的选项，短选项使用 -,如-h,如果该选项不需要具体参数只作为一个开关用，则直接用字符表示，如果还有带参数则后面跟:
    还有第三个参数[]列表为长选项参数，如["version","file=","help"]表示 --version等
    '''

    optdict = {}


    if len(sys.argv) == 1:
        optdict['-h'] = helpstr
        return optdict

    for opt,value in opts:
        optdict[opt] = value

    return optdict


def dowork():
    '''实际操作'''
    optdict = getargvs()  #得到参数字典
    if '-h' in optdict:
        print(optdict['-h'])
        return

    if '-d' not in optdict:
        print('缺少目录名，请看使用说明')
        return

if __name__ == '__main__':

    dowork()