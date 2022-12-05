import json
import scrapy
import sys
import pandas as pd
from scrapy.crawler import CrawlerProcess

class TestSpider(scrapy.Spider):
    def __init__(self, url,short_url):
        self.url = url
        self.short_url = short_url
        self.name = 'test'
        self.start_urls = [self.url]
    all_reviews = list()

    def parse(self, response):
        section = response.xpath("/html/body/div[1]/div/div/div/main/div/div[4]/section")

        for div in section.css('div[class="styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ"]'):
            name = div.xpath('article/aside/div/a/span/text()').extract()[0]
            no_reviews = div.xpath('article/aside/div/a/div/span/text()').extract()[0]
            location = div.xpath('article/aside/div/a/div/div/span/text()').extract()[0]

            stars = div.xpath('article/section/div/div/img/@alt').extract()[0]
            stars = stars.split('out')[0].split('Rated')[1]
            date_of_review = div.xpath('article/section/div/div[2]/time/text()').extract()
            if len(date_of_review) > 0:
                date_of_review = date_of_review[0]
            header = div.xpath('article/section/div[2]/a/h2/text()').extract()[0]
            body = div.xpath('article/section/div[2]/p/text()').extract()[0]
            date_of_experience = div.xpath('article/section/div[2]/p[2]/text()').extract()

            if len(date_of_experience) > 0:
                date_of_experience = date_of_experience[1]

            review = {
                # "name": name,
                # "number of reviews": no_reviews,
                # "location": location,
                # "stars": stars,
                # "date of review": date_of_review,
                # "header": header,
                "body": body
                # "date of experience": date_of_experience
            }
            self.all_reviews.append(review)

        next_page = section.xpath('div[contains(@class, "styles_pagination__6VmQv")]/nav/a[5]/@href').extract()
        
        if next_page:
            full_next_page_url = f"{self.short_url}{next_page[0]}"
            print(full_next_page_url)
            yield scrapy.Request(
                url = full_next_page_url,
                callback=self.parse
            )
        else:
            with open('reviews.json', 'w') as f:
                json.dump(obj=self.all_reviews, fp=f)
                # json.dump(obj={"reviews": self.all_reviews}, fp=f)

        df = pd.read_json('reviews.json')
        df.to_csv('reviews1.csv', index=False)

        print("""
        
                        That is all for today

        """)



if __name__ == "__main__":
    url = sys.argv[1]
    short_url = url.split('/review')[0]
    process = CrawlerProcess()
    process.crawl(TestSpider,url,short_url)
    process.start()