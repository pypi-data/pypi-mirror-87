from .element import Element
from .prop import ValidProp
from .icon import Icon

class Menu(Element):
    opt_css_class = ValidProp(str)
    css_class = ValidProp(str)
    
    def __init__(self, *elements, opt_css_class=None, css_class=None, hide_id=True):
        super().__init__('div', hide_id=hide_id)
        self.opt_css_class = ' ' + opt_css_class if opt_css_class else ''
        self.css_class = css_class or f'ui{self.opt_css_class} menu'
        self.append_inner(*elements)
        
class RightMenu(Menu):
    def __init__(self, *elements):
        super().__init__(*elements, css_class='right menu')
        
class MenuItem(Element):
    url = ValidProp(str)
    icon = ValidProp(Icon)
    
    def __init__(self, name, url=None, icon=None, css_class=None, hide_id=True):
        super().__init__('div', hide_id=hide_id)
        self.url = url
        if self.url is not None:
            self.tag_name = 'a'
        self.icon = icon
        if self.icon:
            self.append_inner(icon)
        self.css_class = css_class or 'item'
        if self.url is not None and len(str(self.url).strip()) > 0:
            self.attrs = [('href', self.url)]
        self.inner_text = name
        
class MenuHeaderItem(MenuItem):
    def __init__(self, title, url=None, icon=None):
        super().__init__(title, url, icon, 'header item')
        
class MenuActiveItem(MenuItem):
    def __init__(self, title, url=None, icon=None):
        super().__init__(title, url, icon, 'active item')
        
class MenuDisableItem(MenuItem):
    def __init__(self, title, url=None, icon=None):
        super().__init__(title, url, icon, 'disabled item')
        