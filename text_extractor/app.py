import streamlit as st
import os
import json
import subprocess
from utils.tools import get_domain_from_url, get_company_name


def run_crawler(start_urls, allowed_domains):
    # Run the Scrapy crawler script
    command = [
        'py', 'crawl.py',
        '--start_urls', start_urls,
        '--allowed_domains', allowed_domains
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    print(result)
    return result.stdout


def read_json_output(company_name):
    output_file = f'crawlings/output_{company_name}.json'
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    else:
        return {}


# Streamlit app
st.title('Web Crawler')

url_input = st.text_input("Enter URL to crawl:", value="https://careaware.eu")

if st.button('Start Crawling'):
    if url_input:
        domain = get_domain_from_url(url_input)
        # Run the crawler
        run_crawler(url_input, domain)

        # Read and display the output
        company_name = get_company_name(domain)

        data = read_json_output(company_name)
        if data:
            st.json(data)
        else:
            st.error("No data found. Ensure the URL is correct and try again.")
    else:
        st.error("Please enter a URL.")
