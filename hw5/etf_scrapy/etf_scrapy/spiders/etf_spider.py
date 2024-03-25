import scrapy


class EtfSpiderSpider(scrapy.Spider):
    name = "etf-spider"
    allowed_domains = ["finance.yahoo.com"]
    start_urls = ["https://finance.yahoo.com/etfs"]

    def parse(self, response):
        rows = response.xpath('//table/tbody/tr')
        for row in rows:
            symbol = row.xpath('.//td[1]/a/text()').get().strip()
            name = row.xpath('.//td[2]/text()').get().strip()
            price = float(row.xpath('.//td[3]/fin-streamer/text()').get())
            change = float(row.xpath('.//td[4]/fin-streamer/span/text()').get())
            change_rate = float(row.xpath('.//td[5]/fin-streamer/span/text()').get()[:-1])
            volume = row.xpath('.//td[6]/fin-streamer/text()').get()
            fifty_day_average = float(row.xpath('.//td[7]/text()').get())
            hundred_day_average = float(row.xpath('.//td[8]/text()').get())
            link = row.xpath(".//@href").get()
            yield response.follow(url=link, callback = self.parse_ticker, meta={
                'symbol': symbol,
                'name': name,
                'price': price,
                'change': change,
                'change_rate': change_rate,
                'volume': volume,
                'fifty_day_average': fifty_day_average,
                'hundred_day_average': hundred_day_average
            })


    def parse_ticker(self, response):
        symbol = response.request.meta['symbol']
        name = response.request.meta['name']
        price = response.request.meta['price']
        change = response.request.meta['change']
        change_rate = response.request.meta['change_rate']
        volume = response.request.meta['volume']
        fifty_day_average = response.request.meta['fifty_day_average']
        hundred_day_average = response.request.meta['hundred_day_average']

        rows = response.xpath('//table[@class="W(100%)"]/tbody')

        for row in rows:
            previous_close = float(row.xpath(".//tr[1]/td[2]/text()").get())
            open = float(row.xpath(".//tr[2]/td[2]/text()").get())

            yield {
                'symbol': symbol,
                'name': name,
                'price': price,
                'change': change,
                'change_rate': change_rate,
                'volume': volume,
                'fifty_day_average': fifty_day_average,
                'hundred_day_average': hundred_day_average,
                'previous_close': previous_close,
                'open': open
            }


            # yield{
            #     'symbol': symbol,
            #     'name': name,
            #     'price': price,
            #     'change': change,
            #     'change_rate': change_rate,
            #     'volume': volume,
            #     'fifty_day_average': fifty_day_average,
            #     'hundred_day_average': hundred_day_average,
            #     'link': link
            # }
