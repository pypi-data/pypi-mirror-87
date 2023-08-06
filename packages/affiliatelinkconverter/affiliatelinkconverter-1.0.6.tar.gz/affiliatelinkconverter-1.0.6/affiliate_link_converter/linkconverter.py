import furl

from affiliate_link_converter import constants
from affiliate_link_converter.common import expand_short_url, convert_amazon_link_with_default, encode_url, \
    add_affiliate_id_in_flipkart

LIST_OF_QUERY_PARAMETERS_TO_REMOVE = ['tag', 'affExtParam1', 'affExtParam2']


def remove_old_affiliate_id_from_urls(short_urls: list):
    """
        :param short_urls: list of short URLs
        :return: list of full url of product page
    """
    expanded_urls = []
    for url in short_urls:
        expanded_url = expand_short_url(url)
        result = furl.furl(expanded_url)
        expanded_urls.append(result.remove(LIST_OF_QUERY_PARAMETERS_TO_REMOVE).url)
    return expanded_urls


def convert_link_with_third_party_vendor(full_url: str, convert_with: str, affiliate_id: str):
    """
        :param full_url: full url of product page
        :param convert_with: cuelinks, inrdeals, zingoy
        :param affiliate_id: affiliate id value
        :return: full url of product page with affiliate id
        """
    if convert_with.lower() == constants.CUELINLKS_CONVETER:
        return 'https://linksredirect.com/?cid=' + affiliate_id + '&source=linkkit&url=' + encode_url(full_url=full_url)
    if convert_with.lower() == constants.INR_DEALS_CONVETER:
        return 'https://inr.deals/track?id=' + affiliate_id + '&src=backend&url=' + encode_url(full_url=full_url)
    if convert_with.lower() == constants.ZIGNOY_CONVERTER:
        return 'http://links.zingoy.com?ref=' + affiliate_id + '&url=' + encode_url(full_url=full_url)


def convert_amazon_link_using_default(full_url: str, convert_with: str, affiliate_id: str):
    """
          :param full_url: full url of product page
          :param affiliate_id: affiliate id of Amazon (e.g bestlootdea-21)
          :return: full url of product page with affiliate id
          """
    if convert_with.lower() == constants.DEFAULT_CONVERTER:
        return convert_amazon_link_with_default(url=full_url, affiliate_id=affiliate_id)


def convert_flipkart_link_using_default(full_url: str, affiliate_id: str):
    """
             :param full_url: full url of product page
             :param affiliate_id: affiliate id of Flipkart
             :return: full url of product page with affiliate id
             """
    if "affid=" in full_url:
        return add_affiliate_id_in_flipkart(full_url, affiliate_id)
    else:
        return full_url + "?affid=" + affiliate_id
