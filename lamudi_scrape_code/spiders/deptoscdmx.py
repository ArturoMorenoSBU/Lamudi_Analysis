import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DeptoscdmxSpider(CrawlSpider):
    name = 'deptoscdmx'
    allowed_domains = ['www.lamudi.com.mx']

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url='https://www.lamudi.com.mx/distrito-federal/departamento/for-rent/?currency=mxn', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='ListingCell-AllInfo ListingUnit']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='next ']/a"))
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
       yield{
           'title': response.xpath("//div[@class='Header-title-block small-12 columns']/h1/text()").get(),
           'price': response.xpath("//span[@class='Overview-main FirstPrice']/text()").get(),
           'address': response.xpath("normalize-space(//span[@class='Header-title-address-text']/text())").get(),
           'car_boxes': response.xpath("normalize-space((//div[@class='columns-2']/div[@data-attr-name='car_spaces']/following-sibling::node())[2]/text())").get(),
           'rooms': response.xpath("normalize-space((//div[@class='columns-2']/div[@data-attr-name='bedrooms']/following-sibling::node())[2]/text())").get(),
           'bathroms': response.xpath("normalize-space((//div[@class='columns-2']/div[@data-attr-name='bathrooms']/following-sibling::node())[2]/text())").get(),
           'squareM': response.xpath("normalize-space((//div[@class='columns-2']/div[@data-attr-name='building_size']/following-sibling::node())[2]/text())").get(),
           'levels': response.xpath("normalize-space((//div[@class='columns-2']/div[@data-attr-name='floor']/following-sibling::node())[2]/text())").get(),
           'date_post': response.xpath("normalize-space((//div[@class='columns-2']/div[@data-attr-name='empty']/following-sibling::node())[2]/text())").get(),
           'description': response.xpath("//div[@class='ViewMore-text-description']/descendant-or-self::node()/text()").getall(),
           'url': response.url
       }