#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os,sys,getopt



helpstr = '''
    用法：   renfilename.py -h -d path -b beforestr -a afterstr -c clearstr -r oldstr,newstr -s ext1,ext2,... -S [file1,file2,...
            目录名为必需参数，配合其它参数实现对目录下的文件进行文件名修改操作,同时可进行多项操作，每项操作完成后对下项操作有影响，顺序按：
　　　　　　　　　　　　-s,-S,-b,-a,-r,-c
            -h 打印使用说明
            -d path 对该目录下的文件进行处理
            -a afterstr 增加后缀
            -b beforestr  增加前缀
            -c clearstr  删除字符
　　　　　　　-r oldstr,newstr 替换字符,前面为旧串，后面为新串，用逗号分隔(',')
            -p 清除所有空格（中文、英文、ＴＡＢ等）
            -s ext1,ext2,.... 过滤文件类型,以逗号分隔，中间不能有空格
            -S file1,file2,... 过滤文件，以逗号分隔，中间不能有空格
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


def addcharbefore(addstr,fileslist):
    '''在文件名前增加一个字符串，参数：新加的串、元组（绝对路径,文件名）列表'''
    if len(addstr) == 0:
        return(False,'新的串不能为空！')

    for onefile in fileslist:
        newfilename = os.path.join(onefile[0],addstr + onefile[1])
        oldfilename = os.path.join(onefile[0],onefile[1])
        os.rename(oldfilename,newfilename)
        '''重命名文件，另有 renames()可以带目录一起重命名'''

def addcharafter(addstr,fileslist):
    '''在文件名后增加一个字符串，参数：新加的串、元组（绝对路径,文件名）列表'''
    if len(addstr) == 0:
        return(False,'新的串不能为空！')

    for onefile in fileslist:
        tmptuple = os.path.splitext(onefile[1])
        newfilename = os.path.join(onefile[0],tmptuple[0] + addstr + tmptuple[1])  #先分解扩展名，再组合成新的文件名
        oldfilename = os.path.join(onefile[0],onefile[1])
        os.rename(oldfilename,newfilename)

def replacechar(replstr,fileslist):
    '''替换字符串'''
    if len(replstr) == 0:
        return(False,'新的串不能为空！')

    for onefile in fileslist:
        tmptuple = replstr.split(',')
        if len(tmptuple) == 1:
            print('字符串错误，请按帮助，按使用格式使用本工具！')
            return

        newfilename = os.path.join(onefile[0],onefile[1].replace(tmptuple[0],tmptuple[1]))#替换
        oldfilename = os.path.join(onefile[0],onefile[1])
        os.rename(oldfilename,newfilename)

def delchar(clearstr,fileslist):
    '''删除字符串'''
    if len(clearstr) == 0:
        return(False,'新的串不能为空！')

    for onefile in fileslist:
        newfilename = os.path.join(onefile[0],onefile[1].replace(clearstr,''))#替换
        oldfilename = os.path.join(onefile[0],onefile[1])
        os.rename(oldfilename,newfilename)

def delspace(fileslist):
    '''删除所有空格,主要有　\r\n,\r,\n,\t,\x20,\u3000'''
    for onefile in fileslist:
        tmpstr = onefile[1].replace('\r\n','')
        tmpstr = tmpstr.replace('\r','')
        tmpstr = tmpstr.replace('\n','')
        tmpstr = tmpstr.replace('\t','')
        tmpstr = tmpstr.replace('\x20','') #空格
        tmpstr = tmpstr.replace('\u3000','') #中文空格

        newfilename = os.path.join(onefile[0],tmpstr)
        oldfilename = os.path.join(onefile[0],onefile[1])
        os.rename(oldfilename,newfilename)


def getargvs():
    '''得到命令行参数信息，以参数选项为程序的输入输出及控制，用短选项为主'''
    optstrs = 'hd:a:b:c:r:s:S:p'
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
        return optdict

    for opt,value in opts:
        optdict[opt] = value

    return optdict


def dowork():
    '''实际操作'''
    optdict = getargvs()  #得到参数字典
    if len(optdict) == 0 or '-h' in optdict:
        print(helpstr)
        return

    if '-d' not in optdict:
        print('缺少目录名，请看使用说明')
        print(helpstr)
        return

    rltdir = getlistbydir(optdict['-d'])

    if not rltdir[0]:
        print(rltdir[1])
        return
    removelist = []  #保存待移走的文件名元组
    if '-s' in optdict: #先过滤文件类别
        filterlist = ['.' + item.upper() for item in optdict['-s'].split(',')] #得到过滤文件类型扩展名，带点，转为大写
        for onefile in rltdir[1]:
            tmpext = os.path.splitext(onefile[1])[1].upper() #得到文件扩展名
            if tmpext in filterlist:
                removelist.append(onefile)
        #print(removelist)

    if len(removelist) != 0:
        '''移走过滤了的文件类别'''
        tmplist = rltdir[1]
        for item in removelist:
            tmplist.remove(item)

    removelist = []  #保存待移走的文件名元组
    if '-S' in optdict: #先过滤文件列表
        filterlist = [item.upper() for item in optdict['-S'].split(',')] #得到过滤文件名，转为大写
        for onefile in rltdir[1]:
            if onefile[1].upper() in filterlist:
                removelist.append(onefile)

    if len(removelist) != 0:
        '''移走过滤了的文件'''
        tmplist = rltdir[1]
        for item in removelist:
            tmplist.remove(item)
    #上面分两次移走是有必要的，因为在前面的移走类别是可能已经把后面指定的文件已经过滤了，后面就不会再执行此文件移走操作，
    #如果放一起，移走列表时可能会出异常。


    '''以下设计，同时可进行多项操作，但有顺序'''
    if '-b' in optdict:  #所有文件增加前前缀
        addcharbefore(optdict['-b'],rltdir[1]) #要加的前缀、文件列表（是一个元组，包含路径和文件名）

    if '-a' in optdict: #后缀
        addcharafter(optdict['-a'],rltdir[1])

    if '-r' in optdict: #替换
        replacechar(optdict['-r'],rltdir[1])

    if '-c' in optdict: #删除
        delchar(optdict['-c'],rltdir[1])

    if '-p' in optdict: #清除空格
        delspace(rltdir[1])


if __name__ == '__main__':

    dowork()