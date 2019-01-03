linewidth = 30
def lineSplit(line):
    plist = ['，','？','。','……',',']
    for p in plist:
        line.replace(p,'\n')
    return line.split('\n')
def linePrint(line):
    global linewidth
    print(line.center(linewidth,chr(12288)))
if __name__=='__main__':
    import os
    import re
    a=[]
    # print(os.getcwd())
    # print(os.name)
    # path = 'C:\\Users\\t\\Desktop'
    # print(os.listdir(path))
    # f = open('C:\\Users\\t\\Desktop\\大周皇族.txt ',mode
    # ='r',encoding='utf-8')
    # a=f.read(5000)
    # b=lineSplit(str(a))
    #
    # for newline in b:
    #     linePrint(newline)
    #os.mkdir('C:\\Users\\t\\Desktop\\大周皇族 ')
    with open('C:\\Users\\t\\Desktop\\大周皇族.txt ', mode
     ='r',encoding='utf-8') as f:
        for line in f.readlines():
            pattern = re.compile('第(.*)章')
            for i in re.findall(pattern,line):
                if i != []:
                    a.append(re.findall(pattern,line))
        b=[]
        for i in a:
            if i not in b:
                b.append(i)
        print(b)
        for i in range(1,1000):
            open('C:\\Users\\t\\Desktop\\大周皇族\\{}.txt '
                 ,format(i),mode='r+',encoding='unicode')














