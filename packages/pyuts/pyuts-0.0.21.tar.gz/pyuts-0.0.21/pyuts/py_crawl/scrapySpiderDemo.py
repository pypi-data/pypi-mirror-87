# -*- coding:UTF-8 -*-
from pyuts import ScrapySpiderU, ScrapyItemU


class ScrapyspidernameItem(ScrapyItemU):
    saveDbName = 'scrapyprojectname'
    saveTableName = 'scrapyspidername'
    id = ScrapyItemU.normal()
    """ ID """
    name = ScrapyItemU.normal()
    """ name """
    
class Scrapyspidername(ScrapySpiderU):
    name = "Scrapyspidername"
    # crawlType = "chrome"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get_url(self):
        return "https://www.baidu.com"
    
    def start_requests(self):
        yield self.get(self.get_url(), callback=self.onParse, meta={'need_proxy':False})
        
    def onParse(self, response):
        print(response.text)
        # yield self.saveItem(scrapyspidernameObj, ScrapyspidernameItem)