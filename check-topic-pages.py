import sys
import requests

from urlparse import urljoin
from bs4 import BeautifulSoup

askcfpb_home = 'http://www.consumerfinance.gov/askcfpb/'
home_response = requests.get(askcfpb_home)

assert(home_response.status_code == 200)

home_soup = BeautifulSoup(home_response.content, "html.parser")

request_headers= dict(pragma="akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-nonces, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no")


def check_topic_page(url, topic):
    print "testing {topic} at {url}".format(topic=topic, url=url)
    response = requests.get(url, headers=request_headers)
    assert (response.status_code == 200)

    soup = BeautifulSoup(response.content, 'html.parser')
    h1 = soup.find('h1')
    try:
        assert(h1.text.strip() == topic)
    except AssertionError:
        exit_code = 1
        print "----"
        print "expected '{expected}', got '{recieved}'".format(expected=topic,
                                                               recieved=h1.text.strip())
        for key, value in response.headers.items():
            print "{key}: {value}".format(key=key, value=value)

        sys.exit(2)

for topic_link in home_soup.select('.category_summary h2 a'):
    url = urljoin(askcfpb_home, topic_link.attrs['href'])
    topic = topic_link.text.strip()
    check_topic_page(url, topic)
