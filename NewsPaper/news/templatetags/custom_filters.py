from django import template
import re

register = template.Library()

TABOO_WORDS = ['собак', 'редиск', 'черт', 'чёрт', 'скотин']


@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise ValueError('Подвергать цензуре можно только строки!')

    matches = []
    for taboo in TABOO_WORDS:
        matches.extend(re.findall(taboo, text, flags=re.IGNORECASE))

    for match in set(matches):
        text = re.sub(match, f'{match[0] + len(match[1:]) * "*"}', text)

    return text
