import scrapy
import json

class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def __init__(self, *args, **kwargs):
        super(SpiderSpider, self).__init__(*args, **kwargs)
        self.authors = []
        self.quotes = []

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            tags = quote.css("div.tags a.tag::text").getall()
            author = quote.css("small.author::text").get()
            self.quotes.append({
                "text": text,
                "author": author,
                "tags": tags
            })
            if author not in self.authors:
                self.authors.append(author)
                author_page_url = quote.css("span a::attr(href)").get()
                yield response.follow(author_page_url, self.parse_author)
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        fullname = response.css("h3.author-title::text").get()
        born_date = response.css("span.author-born-date::text").get()
        born_location = response.css("span.author-born-location::text").get()
        description = response.css("div.author-description::text").get()
        yield {
            "fullname" : fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description,
        }

    def closed(self, reason):
        with open("authors.json", "w") as f:
            json.dump(self.authors, f, indent=4)

        with open("quotes.json", "w") as f:
            json.dump(self.quotes, f, indent=4)
