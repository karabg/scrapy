from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import argparse
from utils.tools import get_domain_from_url


def main(start_urls=None, allowed_domains=None):
    # Determine the output file name
    if allowed_domains is None:
        allowed_domains = []
    if start_urls is None:
        start_urls = []

    domain = get_domain_from_url(start_urls[0]).split('.')[0]
    output_filename = f'crawlings/output_{domain}.json'

    # Set up the Scrapy settings
    settings = get_project_settings()
    settings.set('FEEDS', {output_filename: {'format': 'json', 'overwrite': True}})
    settings.set('LOG_LEVEL', 'INFO')  # Set log level to INFO

    # Create and configure the CrawlerProcess
    process = CrawlerProcess(settings)
    process.crawl('universal', start_urls=start_urls, allowed_domains=allowed_domains)
    process.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Scrapy spider with custom start URLs and allowed domains.")
    parser.add_argument('--start_urls', nargs='+', help="List of start URLs", required=True)
    parser.add_argument('--allowed_domains', nargs='+', help="List of allowed domains", required=True)

    args = parser.parse_args()

    # Convert the lists to the expected format
    start_urls = args.start_urls
    allowed_domains = args.allowed_domains

    main(start_urls, allowed_domains)
