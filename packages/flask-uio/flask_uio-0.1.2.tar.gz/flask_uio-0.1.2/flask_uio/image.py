from .prop import ValidProp
from .element import Element

class Image(Element):
    src = ValidProp(str)
    opt_css_class = ValidProp(str)
    
    def __init__(self, src, opt_css_class=None, css_class=None):
        super().__init__('img')
        self.src = src
        self.attrs = [('src', self.src)]
        self.opt_css_class = ' ' + opt_css_class if opt_css_class else ''
        self.css_class = css_class or f'ui{self.opt_css_class} image'
        
class ImageLink(Element):
    src = ValidProp(str)
    url = ValidProp(str)
    opt_css_class = ValidProp(str)
    
    def __init__(self, src, url, opt_css_class=None, css_class=None):
        super().__init__('a')
        self.src = src
        self.url = url
        self.attrs = [('href', self.url)]
        self.append_inner(Image(self.src, css_class=''))
        self.opt_css_class = ' ' + opt_css_class if opt_css_class else ''
        self.css_class = css_class or f'ui{self.opt_css_class} image'