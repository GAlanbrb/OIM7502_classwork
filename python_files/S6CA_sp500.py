import scrapy


class S6caSp500Spider(scrapy.Spider):
    name = "S6CA_sp500"
    allowed_domains = ["slickcharts.com"]
    start_urls = ["https://slickcharts.com/sp500/performance"]

    def parse(self, response):
        rows = response.xpath('//table/tbody/tr') # cannot find the ID within table
        for row in rows:
            number = row.xpath('td[1]/text()').get()
            company = row.xpath('td[2]/text()').get()
            symbol = row.xpath('td[3]/text()').get()
            ytd = row.xpath('td[4]/text()').get()
        yield{
            'number': number,
            'company': company,
            'symbol': symbol,
            'ytd': ytd
        }
