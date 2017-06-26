import scrapy
import datetime
from scrapy.spiders import CrawlSpider
from techfinder.items import EmailItem
from scrapy.selector import HtmlXPathSelector


class DetectSpider(scrapy.Spider):
    name = "test"

    alloweddomainfile = open("emaildomains.txt")
    allowed_domains = [domain.strip() for domain in alloweddomainfile.readlines()]
    alloweddomainfile.close()

    starturlfile = open("emailurls.txt")
    start_urls = [url.strip() for url in starturlfile.readlines()]
    starturlfile.close()


    def parse(self, response):




        hxs = HtmlXPathSelector(response)
        emails = hxs.xpath('//body').re('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')


       # emails = hxs.xpath('//[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+').extract()             
        #[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+
        #<a\s+href=\"mailto:([a-zA-Z0-9._@]*)\
        #/^(|(([A-Za-z0-9]+_+)|([A-Za-z0-9]+\-+)|([A-Za-z0-9]+\.+)|([A-Za-z0-9]+\++))*[A-Za-z0-9]+@((\w+\-+)|(\w+\.))*\w{1,63}\.[a-zA-Z]{2,6})$/i



        emailitems = []
        for email in zip(emails):
            emailitem = EmailItem()
            emailitem["email"] = emails
            emailitem["source"] = response.url
            emailitem["datetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            emailitems.append(emailitem)
        return emailitems
