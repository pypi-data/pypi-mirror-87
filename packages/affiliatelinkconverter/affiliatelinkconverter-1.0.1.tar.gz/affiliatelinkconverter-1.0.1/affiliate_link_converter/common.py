import re
import urllib.parse
import http.client

import furl
import requests
from unshortenit import UnshortenIt


def expand_short_url(url):
    is_amazon_short_url = url.startswith('https://amzn.to')
    is_flipkart_short_url = url.startswith('http://fkrt.it')
    if is_amazon_short_url or is_flipkart_short_url:
        full_url = get_full_url_from_header_location(url)
        is_amazon_url = full_url.startswith("https://www.amazon.in") or full_url.startswith("http://www.amazon.in/")
        if is_amazon_url:
            full_url = get_clean_amazon_url(full_url)
    else:
        unshortener = UnshortenIt()
        full_url = unshortener.unshorten(url)
    return full_url


def get_full_url_from_header_location(url):
    parsed = urllib.parse.urlsplit(url)
    h = http.client.HTTPConnection(parsed.netloc)
    resource = parsed.path
    if parsed.query != "":
        resource += "?" + parsed.query
    h.request('HEAD', resource)
    response = h.getresponse()
    return response.getheader('Location')


def get_clean_amazon_url(full_url):
    if full_url.startswith('https://www.amazon.in/') or full_url.startswith("http://www.amazon.in/"):
        asin_number = get_amazon_asin_number(full_url=full_url)
        if asin_number is not None:
            full_url = "http://www.amazon.in/dp/" + asin_number
    return full_url


def get_amazon_asin_number(full_url):
    asin = None
    try:
        if '/dp' in full_url:
            asin = full_url.split("/dp/")[1]
            if '/' in asin:
                asin = asin.split("/")[0]
            elif '?' in asin:
                asin = asin.split("?")[0]
            elif '&' in asin:
                asin = asin.split("&")[0]
        elif '/d' in full_url:
            asin = full_url.split("/d/")[1]
            if '/' in asin:
                asin = asin.split("/")[0]
            elif '?' in asin:
                asin = asin.split("?")[0]
            elif '&' in asin:
                asin = asin.split("&")[0]
        elif '/product' in full_url:
            asin = full_url.split("/product/")[1]
            if '/' in asin:
                asin = asin.split("/")[0]
            elif '?' in asin:
                asin = asin.split("?")[0]
            elif '&' in asin:
                asin = asin.split("&")[0]
        elif '/offer-listing' in full_url:
            asin = full_url.split("/offer-listing/")[1]
            if '/' in asin:
                asin = asin.split("/")[0]
            elif '?' in asin:
                asin = asin.split("?")[0]
            elif '&' in asin:
                asin = asin.split("&")[0]
        return asin
    except Exception as ex:
        return asin


def convert_amazon_link_with_default(url, affiliate_id):
    result = furl.furl(url)
    return result.add({'tag': affiliate_id}).url


def encode_url(full_url):
    full_url = full_url.replace("%", "%25")
    full_url = full_url.replace("!", "%21")
    full_url = full_url.replace("*", "%2A")
    full_url = full_url.replace("'", "%27")
    full_url = full_url.replace("(", "%28")
    full_url = full_url.replace(")", "%29")
    full_url = full_url.replace(";", "%3B")
    full_url = full_url.replace(":", "%3A")
    full_url = full_url.replace("@", "%40")
    full_url = full_url.replace("&", "%26")
    full_url = full_url.replace("=", "%3D")
    full_url = full_url.replace("+", "%2B")
    full_url = full_url.replace("$", "%24")
    full_url = full_url.replace(",", "%2C")
    full_url = full_url.replace("/", "%2F")
    full_url = full_url.replace("?", "%3F")
    full_url = full_url.replace("#", "%23")
    full_url = full_url.replace("[", "%5B")
    full_url = full_url.replace("]", "%5D")
    result = requests.get('https://helloacm.com/api/urlencode/?cached&s=' + full_url)
    return result.json()


def replacer(match, new_value, is_third_group_exist):
    prefix = match.group(1)
    infix = new_value
    if is_third_group_exist:
        suffix = match.group(3)
        result = f'{prefix}{infix}{suffix}'.format(prefix, infix, suffix)
        return result
    result = f'{prefix}{infix}'.format(prefix, infix)
    return result


def add_affiliate_id_in_flipkart(url, affiliate_id):
    pattern = r'(.*[?&]affid=)(\w+)(&.*)'
    is_match = re.search(pattern, url)
    if not is_match:
        pattern = r'(.*[?&]affid=)(\w+)'
        is_match = re.search(pattern, url)
        if is_match:
            return re.sub(pattern, lambda m: replacer(m,affiliate_id, False), url)
        return url
    return re.sub(pattern, lambda m: replacer(m,affiliate_id, True), url)