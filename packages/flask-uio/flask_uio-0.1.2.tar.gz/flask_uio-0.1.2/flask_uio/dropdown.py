from .element import Element
from .prop import ValidProp
from .mixin import ReqInjectScriptMixin
from .icon import Icon

class Dropdown(Element, ReqInjectScriptMixin):
    title = ValidProp(str)
    opt_css_class = ValidProp(str)
    css_class = ValidProp(str)
    
    def __init__(self, title, *elements, opt_css_class=None, css_class=None):
        super().__init__('div', hide_id=False)
        self.title = title
        self.opt_css_class = opt_css_class or ''
        self.css_class = css_class or f'ui{self.opt_css_class} dropdown'
        self.append_inner(Element('div', css_class='text', inner_text=title))
        self.append_inner(Icon('dropdown icon'))
        self.append_inner(*elements)
        self.inject_script = f'load_dropdown("{self.id}", {{on: "hover"}});'
        
class DropdownMenu(Element):
    def __init__(self, *elements):
        super().__init__('div')
        for e in elements:
            self.append_inner(e)
        self.css_class = 'menu'
        
class DropdownMenuItem(Element):
    name = ValidProp(str)
    url = ValidProp(str)
    icon = ValidProp(Icon)
    desc = ValidProp(str)
    
    def __init__(self, name, url=None, icon=None, desc=None, css_class=None):
        super().__init__('div')
        self.inner_text = name
        self.url = url
        if self.url:
            self.tag_name = 'a'
            self.attrs = [('href', self.url)]
        self.desc = desc
        self.icon = icon
        if self.icon:
            self.append_inner(icon)
        if self.desc:
            self.append_inner(Element('span', css_class='description', inner_text=self.desc))
        self.css_class = css_class or f'item'
        