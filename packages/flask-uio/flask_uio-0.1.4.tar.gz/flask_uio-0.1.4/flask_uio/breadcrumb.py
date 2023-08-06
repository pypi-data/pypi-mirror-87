from .element import Element
from .divider import Divider
from .prop import ValidProp

class Breadcrumb(Element):
    opt_css_class = ValidProp(str)
    is_dividing = ValidProp(bool)
    
    def __init__(self, opt_css_class=None, is_dividing=True):
        super().__init__('div')
        self.opt_css_class = ' ' + opt_css_class if opt_css_class else ''
        self.css_class = f'ui{self.opt_css_class} breadcrumb'
        self.is_dividing = is_dividing
        if self.is_dividing:
            self.append_next(Divider())

class BreadcrumbSection(Element):
    def __init__(self, title, url=None, is_active=False):
        super().__init__('div')
        self.url = url
        if self.url:
            self.tag_name = 'a'
            self.attrs = [('href', self.url)]
        self.inner_text = title
        opt = ''
        self.is_active = is_active
        if self.is_active:
            opt = 'active '
        self.css_class = f'{opt}section'
        
class BreadcrumbDividerIcon(Element):
    def __init__(self, icon_css_class=None):
        super().__init__('i')
        self.css_class = icon_css_class + ' divider' if icon_css_class else 'right chevron icon divider'
        
        