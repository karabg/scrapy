from urllib.parse import urlparse


def get_domain_from_url(url):
    netloc = urlparse(url).netloc
    index = 4 * ("www" in netloc)  # =0 if no www and =1 if www in netloc
    domain = netloc[index:]
    return domain


def get_company_name(domain):
    return domain.split(".")[0]