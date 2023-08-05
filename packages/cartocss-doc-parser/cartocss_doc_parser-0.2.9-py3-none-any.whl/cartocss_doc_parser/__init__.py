import os
import re
import sys
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


__version__ = "0.2.9"
__version_info__ = tuple([int(i) for i in __version__.split(".")])
__title__ = "cartocss-doc-parser"
__description__ = "CartoCSS documentation parser."
__module__ = sys.modules[__name__]

CARTOCSS_DOC_URL = "https://carto.com/developers/styling/cartocss/"

DEFAULT_USER_AGENT = "%s v%s" % (__title__, __version__)

PROP_DETAILS_ATTR_MAP = {
    "Description": "description",
    "Sample CartoCSS Code": "sample",
    "Default Value": "default",
}

UNDOCUMENTED_VALUES = ["keyword", "unsigned", "tags"]

PARSERS = [
    ("symbolizers", "cartocss-symbolizer", False),
    ("values", "cartocss-values", False),
    ("other_parameters", "other-cartocss-parameters", False),
    ("torque_properties", "cartocss---torque-maps", True),
    ("common_elements", "common-elements", True),
    ("map_background_and_string_elements",
     "map-background-and-string-elements", True),
    ("polygon", "polygon", True),
    ("line", "line", True),
    ("markers", "markers", True),
    ("shield", "shield", True),
    ("line_pattern", "line-pattern", True),
    ("polygon_pattern", "polygon-pattern", True),
    ("raster", "raster", True),
    ("point", "point", True),
    ("text", "text", True),
    ("building", "building", True),
]


def get_cartocss_doc_html(url=CARTOCSS_DOC_URL, user_agent=DEFAULT_USER_AGENT):
    if os.path.isfile(url):
        with open(url, encoding="utf-8") as f:
            markup = f.read()
        return markup
    req = Request(url)
    req.add_header("User-Agent", user_agent)
    return urlopen(req).read().decode("utf-8")


def get_cartocss_doc_soup(url=CARTOCSS_DOC_URL, user_agent=DEFAULT_USER_AGENT):
    markup = get_cartocss_doc_html(url=url, user_agent=user_agent)
    return BeautifulSoup(markup, "lxml")


def _parse_table_links_after_h(soup,
                               h_id,
                               url=CARTOCSS_DOC_URL,
                               properties=False):
    h = soup.find(id=h_id)
    table = h.find_next()
    while table.name != "table":
        table = table.find_next()
    for td in table.find_all("td"):
        a = td.find("a", recursive=False)
        if a is None:
            break
        _id = a["href"].strip("#")
        prop = {
            # Split due to error in `opacity` property
            # https://carto.com/developers/styling/cartocss/#common-elements
            "name": str(a.string).split(" ")[0],
            "link": url + a["href"],
            "id": _id,
        }
        if properties:
            prop_h = soup.find(id=_id)
            data_type_container = prop_h.find_next()

            # Error in `property` title:
            # https://carto.com/developers/styling/cartocss/#point-comp-op-keyword
            if prop_h.string is not None and "`" in prop_h.string:
                prop["type"] = prop_h.string.split("`")[-1]
            else:
                prop["type"] = data_type_container.string
            if data_type_container.name == "table":
                prop_table = data_type_container
            else:
                prop_table = data_type_container.find_next()
            while prop_table.name != "table":
                prop_table = prop_table.find_next()

            _details_attr_map = PROP_DETAILS_ATTR_MAP
            if prop["type"] == "keyword":
                _details_attr_map["Available Values"] = "variants"
            prop_details = {}
            _current_prop_detail = None
            for prop_td in prop_table.find_all("td"):
                if _current_prop_detail is None:
                    _current_prop_detail = PROP_DETAILS_ATTR_MAP.get(
                        prop_td.string, None)
                else:
                    if _current_prop_detail == "default":
                        code_container = prop_td.find("code")

                        if code_container is None:
                            default = re.search(
                                r"^([^.,]+)", prop_td.get_text().lower()
                            ).group(1)
                            if " (" in default:
                                default = default.split(" (")[0]
                        else:
                            default = code_container.string.lower()
                        # The property `background-image` has next string as
                        # default value, but must be null instead
                        # carto.com/developers/styling/cartocss/#background-image-uri
                        _invalid_value = \
                            "this parameter is not applied by default"
                        if default == _invalid_value:
                            default = None
                        prop_details[_current_prop_detail] = default
                    elif _current_prop_detail == "variants":

                        code_containers = prop_td.find_all("code")
                        if len(code_containers) > 0:
                            prop_details[_current_prop_detail] = []

                            # Unconsistency in Available Values code:
                            # https://carto.com/developers/styling/cartocss/#
                            # -torque-aggregation-function-keyword
                            if len(code_containers) == 1:
                                variants = code_containers[0].string.split(",")
                                for variant in variants:
                                    prop_details[_current_prop_detail].append(
                                        variant.strip(" "))
                            else:
                                for code_container in code_containers:
                                    prop_details[_current_prop_detail].append(
                                        code_container.string)
                    else:
                        prop_details[_current_prop_detail] = prop_td.get_text()
                    _current_prop_detail = None
            prop.update(prop_details)
        yield prop


def cartocss_data_types(url=CARTOCSS_DOC_URL, user_agent=DEFAULT_USER_AGENT):
    soup = get_cartocss_doc_soup(url=url, user_agent=user_agent)
    for value in _parse_table_links_after_h(soup, "cartocss-values", url=url):
        data_type = value["name"].lower()
        yield data_type
        if data_type[-1] == "s":
            yield data_type[:-1]
    for value in UNDOCUMENTED_VALUES:
        yield value


def _create_parser(func_name, _id, properties):
    def _func(soup, url=CARTOCSS_DOC_URL):
        return _parse_table_links_after_h(
            soup, _id, url=url, properties=properties)
    _func.__name__ = func_name
    return _func


for _attrname, _id, properties in PARSERS:
    _func_name = "parse_%s" % _attrname
    setattr(
        __module__, _func_name, _create_parser(_func_name, _id, properties))


def cartocss_doc(url=CARTOCSS_DOC_URL, user_agent=DEFAULT_USER_AGENT):
    soup = get_cartocss_doc_soup(url=url, user_agent=user_agent)
    response = {}
    for _attrname, _id, _ in PARSERS:
        _func_name = "parse_%s" % _attrname
        response[_attrname] = getattr(__module__, _func_name)(soup, url=url)
    return response
