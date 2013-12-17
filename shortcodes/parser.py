import re
import shortcodes.parsers
from django.core.cache import cache

supported_shortcodes = ["caption","gallery","vimeo"]

def import_parser(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def shortcode_to_html(code, shortcode_text):
    module = import_parser('shortcodes.parsers.' + code)
    method = getattr(module, 'parse')

    regex_string = r"\[%s(.*?)\]" % code

    shortcode_first_tag = re.findall(regex_string, shortcode_text )[0]

    shortcode_name, space, shortcode_args = shortcode_first_tag.partition(' ')
    shortcode_args = __parse_args__(shortcode_args)

    html = method(shortcode_args, shortcode_text)

    return html

def parse(value):
    original_html = value

    replacements = []

    for code in supported_shortcodes:

        # Caption shortcodes have a beginning and ending tag
        if code in ['caption']:
            regex_search_string = r"\[%s .*?\].*?\[/%s\]" % (code,code)
        # Gallery and Vimeo shortcodes are just opening tags with arguments.
        elif code in ['gallery','vimeo']:
            regex_search_string = r"\[%s (.*?)\]" % code
        else:
            continue

        ex = re.compile(regex_search_string)
        match_groups = re.finditer(ex, original_html)

        for group in match_groups:
            shortcode_text = original_html[group.start():group.end()]
            converted_shortcode_html = shortcode_to_html(code, shortcode_text)

            replacements.append({
                'old' : shortcode_text,
                'new' : converted_shortcode_html
            })

    for replacement in replacements:
        print replacement
        original_html = original_html.replace(replacement['old'], replacement['new'], 1)

    return original_html


def __parse_args__(value):
    ex = re.compile(r'[ ]*(\w+)=([^" ]+|"[^"]*")[ ]*(?: |$)')
    groups = ex.findall(value)
    kwargs = {}

    for group in groups:
        if group.__len__() == 2:
            item_key = group[0]
            item_value = group[1]

            if item_value.startswith('"'):
                if item_value.endswith('"'):
                    item_value = item_value[1:]
                    item_value = item_value[:item_value.__len__() - 1]

            kwargs[item_key] = item_value

    return kwargs
