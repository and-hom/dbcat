import re

camel_to_underscore_pat = re.compile(r'(?<!^)([A-Z])')
underscore_to_camel_pat = re.compile(r'(^|_)([a-z])')


def camel_to_underscore(text):
    return camel_to_underscore_pat.sub(lambda x: '_' + x.group(1), text).lower()


def underscore_to_camel(text):
    return underscore_to_camel_pat.sub(lambda x: x.group(2).upper(), text)

def filter_type(s):
    l = re.findall('\'.*?/(.*?)_edit\.html\'', str(s))
    if l:
        return l[0]
    return None

