from flask_uio.func import get_word
from .element import Element
from .prop import IntProp, ValidProp

class Card(Element):
    opt_css_class = ValidProp(str)
    css_class = ValidProp(str)
    url = ValidProp(str)
    
    def __init__(self, *elements, url=None, opt_css_class=None, css_class=None):
        super().__init__('div')
        self.url = url
        if self.url:
            self.tag_name = 'a'
            self.attrs = [('href', self.url)]
        self.opt_css_class = opt_css_class
        opt = ''
        if self.opt_css_class:
            opt += ' ' + self.opt_css_class    
        self.css_class = css_class or f'ui{opt} card'
        self.append_inner(*elements)
        
class CardImage(Element):
    src = ValidProp(str)
    def __init__(self, src):
        super().__init__('div')
        self.css_class = 'image'
        self.append_inner(Element('img', attrs=[('src', src)]))
        
class Cards(Element):
    opt_css_class = ValidProp(str)
    css_class = ValidProp(str)
    nb_card = IntProp()
    
    def __init__(self, *elements, nb_card=None, opt_css_class=None, css_class=None):
        super().__init__('div')
        self.opt_css_class = opt_css_class
        self.nb_card = nb_card
        opt = ''
        if self.nb_card:
            opt += ' ' + get_word(self.nb_card)
        if self.opt_css_class:
            opt += ' ' + self.opt_css_class    
        self.css_class = css_class or f'ui{opt} cards'
        for e in elements:
            if not isinstance(e, Card):
                raise Exception('Element must be a Card Object.')
            e.css_class.replace('ui ', '')
            self.append_inner(e)
        
class CardContent(Element):
    def __init__(self, *elements):
        super().__init__('div')
        self.css_class = 'content'
        self.append_inner(*elements)
        
class CardExtraContent(Element):
    def __init__(self, *elements):
        super().__init__('div')
        self.css_class = 'extra content'
        self.append_inner(*elements)
        
class CardContentHeader(Element):
    def __init__(self, title):
        super().__init__('div')
        self.css_class = 'header'
        self.inner_text = title
        
class CardContentMeta(Element):
    def __init__(self, text):
        super().__init__('div')
        self.css_class = 'meta'
        self.inner_text = text
        
class CardContentDesc(Element):
    def __init__(self, text):
        super().__init__('div')
        self.css_class = 'description'
        self.inner_text = text
        