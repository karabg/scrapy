from scrapy_splash import SplashRequest
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class UniversalCrawler(CrawlSpider):
    name = 'universal'

    def __init__(self, start_urls=None, allowed_domains=None, *args, **kwargs):
        super(UniversalCrawler, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.allowed_domains = allowed_domains

    rules = (
        Rule(
            LinkExtractor(allow=(), deny=()),  # Extract all links
            callback='parse_item',
            follow=True
        ),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_start_url, args={'wait': 2})

    def parse_start_url(self, response, **kwargs):
        return self._parse_response(response, self.parse_item, cb_kwargs={}, follow=True)

    def parse_item(self, response):
        # Extract visible text content from the page, ignoring 'Skip to content'
        page_text = ' '.join(response.xpath(
            '//body//text()[not(ancestor::script) and not(ancestor::style) and not(ancestor::noscript) and not('
            'ancestor::head) and not(ancestor::title) and normalize-space()]').getall())
        content = page_text.strip()[16:]  # Ignore "Skip to content" part in the page text

        # Save the scraped content to a dictionary with the URL as the key
        yield {
            response.url: content
        }