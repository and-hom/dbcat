import re

camel_pat = re.compile(r'(?<!^)([A-Z])')


def camel_to_underscore(text):
    return camel_pat.sub(lambda x: '_' + x.group(1), text).lower()
