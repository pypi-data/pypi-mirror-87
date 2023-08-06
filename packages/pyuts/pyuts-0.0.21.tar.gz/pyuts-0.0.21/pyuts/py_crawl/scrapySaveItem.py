import scrapy


class ScrapySaveItem(scrapy.Item):
    """"""
    type = scrapy.Field()
    """"""
    saveSign = scrapy.Field()
    """"""
    optionType = scrapy.Field()
