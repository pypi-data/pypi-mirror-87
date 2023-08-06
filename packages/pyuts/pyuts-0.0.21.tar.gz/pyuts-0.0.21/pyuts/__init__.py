# -*- coding: UTF-8 -*-
try:
    from pyuts.py_phone.adbU import AdbU

    def adbU(key=None) -> AdbU:
        '''
        
        adb相关工具
        
        '''
        return AdbU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.chromeU import ChromeU

    def chromeU(key=None) -> ChromeU:
        '''
        
        网页浏览器模拟工具
        
        '''
        return ChromeU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.scrapyU import ScrapyU

    def scrapyU(key=None) -> ScrapyU:
        '''
        
        scrapy相关封装工具
        
        '''
        return ScrapyU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.webU import WebU

    def webU(key=None) -> WebU:
        '''
        
        网页浏览器模拟工具
        
        '''
        return WebU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.scrapySpiderU import ScrapySpiderU

    def scrapySpiderU(key=None) -> ScrapySpiderU:
        '''
        
        scrapy相关封装工具的各个爬虫器
        
        '''
        return ScrapySpiderU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.threadU import ThreadU

    def threadU(key=None) -> ThreadU:
        '''
        
        线程相关工具
        
        '''
        return ThreadU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.envU import EnvU

    def envU(key=None) -> EnvU:
        '''
        
        环境变量相关工具
        
        '''
        return EnvU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_db.mongoDBU import MongoDBU

    def mongoDBU(key=None) -> MongoDBU:
        '''
        
        Mongo数据库工具
        
        '''
        return MongoDBU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.scrapyCommandU import ScrapyCommandU

    def scrapyCommandU(key=None) -> ScrapyCommandU:
        '''
        
        scrapy相关命令行操作
        
        '''
        return ScrapyCommandU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.datetimeU import DatetimeU

    def datetimeU(key=None) -> DatetimeU:
        '''
        
        时间日期相关工具 
        
        
        时间格式类型: 
        
        %y 两位数的年份表示（00-99）
        
        %Y 四位数的年份表示（000-9999）
        
        %m 月份（01-12）
        
        %d 月内中的一天（0-31）
        
        %H 24小时制小时数（0-23）
        
        %I 12小时制小时数（01-12）
        
        %M 分钟数（00=59）
        
        %S 秒（00-59）
        
        %a 本地简化星期名称
        
        %A 本地完整星期名称
        
        %b 本地简化的月份名称
        
        %B 本地完整的月份名称
        
        %c 本地相应的日期表示和时间表示
        
        %j 年内的一天（001-366）
        
        %p 本地A.M.或P.M.的等价符
        
        %U 一年中的星期数（00-53）星期天为星期的开始
        
        %w 星期（0-6），星期天为星期的开始
        
        %W 一年中的星期数（00-53）星期一为星期的开始
        
        %x 本地相应的日期表示
        
        %X 本地相应的时间表示
        
        %Z 当前时区的名称
        
        %% %号本身
        
        
        '''
        return DatetimeU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.scrapyRunU import ScrapyRunU

    def scrapyRunU(key=None) -> ScrapyRunU:
        '''
        
        ScrapyRun相关封装工具
        
        '''
        return ScrapyRunU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.recordU import RecordU

    def recordU(key=None) -> RecordU:
        '''
        
        ???
        
        '''
        return RecordU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.scrapyItemU import ScrapyItemU

    def scrapyItemU(key=None) -> ScrapyItemU:
        '''
        
        scrapy相关封装工具的数据存储项基类
        
        '''
        return ScrapyItemU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.scrapySpiderDemo import Scrapyspidername

    def scrapyspidername(key=None) -> Scrapyspidername:
        '''
        
        '''
        return Scrapyspidername.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.httpU import HttpU

    def httpU(key=None) -> HttpU:
        '''
        
        接口请求
        
        '''
        return HttpU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_crawl.scrapyCommandDemo import Scrapycommandname

    def scrapycommandname(key=None) -> Scrapycommandname:
        '''
        
        '''
        return Scrapycommandname.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_server.httpHandlerU import HttpHandlerU

    def httpHandlerU(key=None) -> HttpHandlerU:
        '''
        
        HTTP服务器端接口基类
        
        '''
        return HttpHandlerU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_server.httpServerU import HttpServerU

    def httpServerU(key=None) -> HttpServerU:
        '''
        
        HTTP服务器端相关工具
        
        '''
        return HttpServerU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_server.serverU import ServerU

    def serverU(key=None) -> ServerU:
        '''
        
        服务器端相关工具
        
        '''
        return ServerU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_proxy.proxyCrawlerU import ProxyCrawlerU

    def proxyCrawlerU(key=None) -> ProxyCrawlerU:
        '''
        
        代理相关工具
        
        '''
        return ProxyCrawlerU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.ctrlCU import CtrlCU

    def ctrlCU(key=None) -> CtrlCU:
        '''
        
        信号相关工具
        
        '''
        return CtrlCU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.asyncU import AsyncU

    def asyncU(key=None) -> AsyncU:
        '''
        
        异步相关工具
        
        '''
        return AsyncU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_file.fileU import FileU

    def fileU(key=None) -> FileU:
        '''
        
        文件相关工具
        
        '''
        return FileU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_db.redisDBU import RedisDBU

    def redisDBU(key=None) -> RedisDBU:
        '''
        
        Redis数据库工具
        
        '''
        return RedisDBU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_proxy.proxyU import ProxyU

    def proxyU(key=None) -> ProxyU:
        '''
        
        代理相关工具
        
        '''
        return ProxyU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_proxy.proxyInfoU import ProxyInfoU

    def proxyInfoU(key=None) -> ProxyInfoU:
        '''
        
        代理信息相关工具
        
        '''
        return ProxyInfoU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_file.videoU import VideoU

    def videoU(key=None) -> VideoU:
        '''
        
        视频文件格式相关工具
        
        '''
        return VideoU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.moduleU import ModuleU

    def moduleU(key=None) -> ModuleU:
        '''
        
        模块相关工具
        
        '''
        return ModuleU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.mathU import MathU

    def mathU(key=None) -> MathU:
        '''
        
        数学相关工具
        
        '''
        return MathU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.sortU import SortU

    def sortU(key=None) -> SortU:
        '''
        
        排序相关工具
        
        '''
        return SortU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.algorithmU import AlgorithmU

    def algorithmU(key=None) -> AlgorithmU:
        '''
        
        算法相关工具
        
        '''
        return AlgorithmU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.cmdU import CmdU

    def cmdU(key=None) -> CmdU:
        '''
        
        命令行相关工具
        
        '''
        return CmdU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.speechU import SpeechU

    def speechU(key=None) -> SpeechU:
        '''
        
        语言转化相关工具，文本转语音
        
        '''
        return SpeechU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.speechBaiduU import SpeechU

    def speechU(key=None) -> SpeechU:
        '''
        
        语言转化相关工具，文本转语音
        
        '''
        return SpeechU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.jsonU import JsonU

    def jsonU(key=None) -> JsonU:
        '''
        
        json
        
        '''
        return JsonU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.objU import ObjU

    def objU(key=None) -> ObjU:
        '''
        
        obj相关操作工具
        
        '''
        return ObjU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.xmlU import XmlU

    def xmlU(key=None) -> XmlU:
        '''
        
        XML
        pip install xmltodict
        
        '''
        return XmlU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_mix.jsU import JsU

    def jsU(key=None) -> JsU:
        '''
        
        js工具， pip install PyExecJS
        
        '''
        return JsU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_pfm.modelU import ModelU

    def modelU(key=None) -> ModelU:
        '''
        
        模型相关工具
        
        '''
        return ModelU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_pfm.pfmU import PfmU

    def pfmU(key=None) -> PfmU:
        '''
        
        预测模型相关工具
        
        '''
        return PfmU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_app.windowU import WindowU

    def windowU(key=None) -> WindowU:
        '''
        
        PC界面相关工具
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5-tools
        
        '''
        return WindowU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_app.appU import AppU

    def appU(key=None) -> AppU:
        '''
        
        PC界面相关工具
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5-tools
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ quamash
        
        '''
        return AppU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_app.ui2pyU import Ui2pyU

    def ui2pyU(key=None) -> Ui2pyU:
        '''
        
        PC界面相关工具
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5-tools
        
        '''
        return Ui2pyU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_db.mysqlDBU import MysqlDBU

    def mysqlDBU(key=None) -> MysqlDBU:
        '''
        
        mysql数据库操作工具
        
        '''
        return MysqlDBU.produce(key)
except ImportError as e:
    print(e)

try:
    from pyuts.py_db.mysqlU import MysqlU

    def mysqlU(key=None) -> MysqlU:
        '''
        
        mysql数据库工具
        
        '''
        return MysqlU.produce(key)
except ImportError as e:
    print(e)

