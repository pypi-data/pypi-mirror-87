# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 09:23:15) 
# [Clang 10.0.1 (clang-1001.0.46.3)]
# Embedded file name: /Users/jack/WorkSpace/testCrawl/pyuts/py_crawl/__main__.py
# Compiled at: 2020-05-13 16:20:28
# Size of source mod 2**32: 1132 bytes

def initScrapySpider(projectName,spiderName):
    copyName = projectName
    if '/' in projectName:
        names = projectName.split('/')
        projectName = names[-1]
    import pyuts
    pyutsPath = pyuts.__file__[:-12]
    from pyuts.py_file.fileU import FileU
    fileU = FileU()
    settingStr = fileU.read_str(f'{pyutsPath}/py_crawl/scrapySpiderDemo.py')
    settingStr = settingStr.replace('scrapyprojectname', f"{projectName[:1].lower()}{projectName[1:]}")
    settingStr = settingStr.replace('Scrapyprojectname', f"{projectName[:1].upper()}{projectName[1:]}")
    settingStr = settingStr.replace('scrapyspidername', f"{spiderName[:1].lower()}{spiderName[1:]}")
    settingStr = settingStr.replace('Scrapyspidername', f"{spiderName[:1].upper()}{spiderName[1:]}")
    fileU.write_str(f"{projectName}/{projectName}/spiders/{spiderName}.py", settingStr)
    if copyName != projectName:
        fileU.move(projectName,copyName)
        
def initScrapyCommand(projectName,commandName):
    copyName = projectName
    if '/' in projectName:
        names = projectName.split('/')
        projectName = names[-1]
    import pyuts
    pyutsPath = pyuts.__file__[:-12]
    from pyuts.py_file.fileU import FileU
    fileU = FileU()
    settingStr = fileU.read_str(f'{pyutsPath}/py_crawl/scrapyCommandDemo.py')
    settingStr = settingStr.replace('scrapyprojectname', f"{projectName[:1].lower()}{projectName[1:]}")
    settingStr = settingStr.replace('Scrapyprojectname', f"{projectName[:1].upper()}{projectName[1:]}")
    settingStr = settingStr.replace('scrapycommandname', f"{commandName[:1].lower()}{commandName[1:]}")
    settingStr = settingStr.replace('Scrapycommandname', f"{commandName[:1].upper()}{commandName[1:]}")
    fileU.write_str(f"{projectName}/{projectName}/commands/{commandName[:1].lower()}{commandName[1:]}.py", settingStr)
    if copyName != projectName:
        fileU.move(projectName,copyName)

def initScrapyProject(projectName):
    from pyuts.py_mix.cmdU import CmdU
    import pyuts
    pyutsPath = pyuts.__file__[:-12]
    copyName = projectName
    if '/' in projectName:
        names = projectName.split('/')
        projectName = names[-1]
    CmdU.produce('scrapy').run(f"scrapy startproject {projectName}")
    from pyuts.py_file.fileU import FileU
    fileU = FileU()
    # copy settings.py
    settingStr = fileU.read_str(f'{pyutsPath}/py_crawl/scrapySettings.py')
    settingStr = settingStr.replace('scrapyprojectname', f"{projectName[:1].lower()}{projectName[1:]}")
    settingStr = settingStr.replace('Scrapyprojectname', f"{projectName[:1].upper()}{projectName[1:]}")
    fileU.write_str(f"{projectName}/{projectName}/settings.py", settingStr)
    # copy Middle.py
    settingStr = fileU.read_str(f'{pyutsPath}/py_crawl/scrapyMiddleware.py')
    settingStr = settingStr.replace('scrapyprojectname', f"{projectName[:1].lower()}{projectName[1:]}")
    settingStr = settingStr.replace('Scrapyprojectname', f"{projectName[:1].upper()}{projectName[1:]}")
    fileU.write_str(f"{projectName}/{projectName}/pyutsmiddlewares.py", settingStr)
    # copy pipelines.py
    settingStr = fileU.read_str(f'{pyutsPath}/py_crawl/scrapyPipline.py')
    settingStr = settingStr.replace('scrapyprojectname', f"{projectName[:1].lower()}{projectName[1:]}")
    settingStr = settingStr.replace('Scrapyprojectname', f"{projectName[:1].upper()}{projectName[1:]}")
    fileU.write_str(f"{projectName}/{projectName}/pipelines.py", settingStr)
    # init testSpider
    initScrapySpider(projectName,'test')
    # init commands __init__.py
    fileU.write_str(f"{projectName}/{projectName}/commands/__init__.py",'# -*- coding: utf-8 -*-\n')
    # copy commands.testCrawl.py
    initScrapyCommand(projectName,'testCrawl')
    # init config commands file
    settingss = fileU.read_str("./command_lines.txt")
    if len(settingss) == 0:
        settingStr = '# mac or linux\n'
        settingStr += 'export proxy_host=\n'
        settingStr += 'export proxy_port=\n'
        settingStr += 'export proxy_user=\n'
        settingStr += 'export proxy_pswd=\n'
        settingStr += 'export mongo_host=\n'
        settingStr += 'export mongo_port=\n'
        settingStr += 'export mongo_user=\n'
        settingStr += 'export mongo_pswd=\n'
        settingStr += '# windows\n'
        settingStr += 'set proxy_host=\n'
        settingStr += 'set proxy_port=\n'
        settingStr += 'set proxy_user=\n'
        settingStr += 'set proxy_pswd=\n'
        settingStr += 'set mongo_host=\n'
        settingStr += 'set mongo_port=\n'
        settingStr += 'set mongo_user=\n'
        settingStr += 'set mongo_pswd=\n'
        fileU.write_str("./command_lines.txt",settingStr)
    # init crawl.py
    settingss = fileU.read_str("./crawl.py")
    if len(settingss) == 0:
        settingStr = fileU.read_str(f'{pyutsPath}/py_crawl/scrapyCrawlDemo.py')
        fileU.write_str("./crawl.py", settingStr)
    # move project
    if copyName != projectName:
        fileU.move(projectName,copyName)

def printHelp():
    print('example: python -m pyuts.py_crawl scrapy_init projectName')
    print('example: python -m pyuts.py_crawl scrapy_init_spider projectName spiderName')
    print('example: python -m pyuts.py_crawl scrapy_init_command projectName spiderCommand')

if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 2:
        printHelp()
        exit()
    else:
        action = sys.argv[1]
        if action == 'scrapy_init':
            projectName = sys.argv[2]
            initScrapyProject(projectName)
        elif action == 'scrapy_init_spider':
            projectName = sys.argv[2]
            spiderName = sys.argv[3]
            initScrapySpider(projectName,spiderName)
        elif action == 'scrapy_init_command':
            projectName = sys.argv[2]
            commandName = sys.argv[3]
            initScrapyCommand(projectName,commandName)
        else:
            printHelp()
# okay decompiling __main__.cpython-37.pyc
