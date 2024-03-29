from scrapy.crawler import CrawlerProcess
from quotes.quotes.spiders.spider import SpiderSpider

def main():
    process = CrawlerProcess()
    process.crawl(SpiderSpider)
    process.start()

if __name__ == "__main__":
    main()
