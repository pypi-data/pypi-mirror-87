import sys

def printHelp():
    print('py_crawl')
    from .py_crawl.__main__ import printHelp as printHelp1
    printHelp1()

if __name__ == "__main__":
    option = '--help'
    if len(sys.argv) > 1:
        option = sys.argv[1]
    if option in ['-h','--help']:
        printHelp()
        