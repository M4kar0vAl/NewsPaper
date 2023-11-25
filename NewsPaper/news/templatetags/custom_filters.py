from django import template

register = template.Library()

TABOO_WORDS = ['собак', 'редиск', 'черт', 'чёрт', 'скотин']


@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise ValueError('Подвергать цензуре можно только строки!')

    for taboo in TABOO_WORDS:
        if taboo in text:
            text = text.replace(taboo, f'{taboo[0] + "*" * len(taboo[1:])}')

        if taboo.capitalize() in text:
            taboo = taboo.capitalize()
            text = text.replace(taboo, f'{taboo[0] + "*" * len(taboo[1:])}')

    return text
