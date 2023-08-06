import sys
import pyuts

def getArgv(index,defValue=None):
    if len(sys.argv) > index:
        return sys.argv[index]
    return defValue

def getParms(key,defValue=None):
    if 1 >= len(sys.argv):
        return defValue
    for i in range(1, len(sys.argv), 2):
        pkey = getArgv(i)
        if key == pkey:
            return getArgv(i+1,defValue)
    return defValue
  
def printHelp():
    print('python crawl.py command testCrawl -p 【projectName】 -a paramstr -l Y|m|d|H|M|S|w')  
    print('python crawl.py spider Test -p 【projectName】 -a paramstr -l Y|m|d|H|M|S|w')

def doCommand(projectName, commandName, paramStr=None):
    _a = f' {paramStr}' if len(paramStr) > 0 else ''
    cmd = f"scrapy {commandName}{_a}"
    pyuts.cmdU().run(cmd, cwd=f'./{projectName}')

def doSpider(projectName, spiderName, paramStr=None):
    _a = f' -a {paramStr}' if len(paramStr) > 0 else ''
    cmd = f"scrapy crawl {spiderName}{_a}"
    pyuts.cmdU().run(cmd, cwd=f'./{projectName}')

if __name__ == "__main__":
    option = getArgv(1,'')
    if option in ['help','h','--help','-help','-h']:
        printHelp()
    elif option in ['command','c','-c','-command','--command']:
        commandName = getParms(option,'')
        projectName = getParms('-p','') 
        if len(commandName) == 0 or len(projectName) == 0:
            printHelp()
            exit()
        params = getParms('-a','')
        loopStr = getParms('-l','')
        if len(loopStr) > 0:
            pyuts.ctrlCU().loopdoWhen(loopStr, doCommand, projectName,commandName, params)
        else:
            doCommand(projectName,commandName,params)
    elif option in ['spider','s','-s','-spider','--spider']:
        spiderName = getParms(option,'')
        projectName = getParms('-p','') 
        if len(spiderName) == 0 or len(projectName) == 0:
            printHelp()
            exit()
        params = getParms('-a','')
        loopStr = getParms('-l','')
        print(loopStr)
        if len(loopStr) > 0:
            pyuts.ctrlCU().loopdoWhen(loopStr, doSpider, projectName,spiderName, params)
        else:
            doSpider(projectName,spiderName,params)
        