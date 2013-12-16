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


def parse(value):

    for code in supported_shortcodes:

        module = import_parser('shortcodes.parsers.' + code)
        function = getattr(module, 'parse')


        # With arguments in opening tag
        ex = re.compile(r"\[%s .*?\].*?\[/%s\]" % (code,code))
        match_groups = re.finditer(ex, value)

        for group in match_groups:
          value = value[:group.start()] + function(value) + value[group.end():]

        # Without arguments in tag
        ex = re.compile(r"\[%s\].*?\[/%s\]" % (code,code))
        match_groups = re.finditer(ex, value)

        for group in match_groups:
          value = value[:group.start()] + function(value) + value[group.end():]

        ex = re.compile(r"\[%s (.*?)\]" % code)
        match_groups = re.finditer(ex, value)

        for group in match_groups:
          value =  value[:group.start()] + function(value) + value[group.end():]
        

    """
    ex = re.compile(r'\[(.*?)\]')
    groups = ex.findall(value)
    pieces = {}
    parsed = value

    for item in groups:
        if ' ' in item:
            name, space, args = item.partition(' ')
            args = __parse_args__(args)
        # If shortcode does not use spaces as a separator, it might use equals
        # signs.
        elif '=' in item:
            name, space, args = item.partition('=')
            args = __parse_args__(args)
        else:
            name = item
            args = {}

        item = re.escape(item)
        try:
            #if cache.get(item):
            #    parsed = re.sub(r'\[' + item + r'\]', cache.get(item), parsed)
            #else:
                # Case when you have a shortcode like []
                if name == '':
                    continue


                #cache.set(item, result, 3600)

                if result is None:
                  result = ''
                parsed = re.sub(r'\[' + item + r'\]', result, parsed)
        except ImportError:
            pass
        except ValueError:
            pass

    return parsed
    """

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
