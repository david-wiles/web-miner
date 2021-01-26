from scrapy import Item, Field


class WebItem(Item):
    url = Field()
    response = Field()
    timestamp = Field()
    server = Field()
    file = Field()  # The location of the response body file. Could be a file path or url
