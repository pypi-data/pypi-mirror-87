from .element import Element, CoreElement
from .prop import ValidProp

class Container(Element):
    fluid = ValidProp(bool)
    text = ValidProp(bool)
    css_class = ValidProp(str)
    
    def __init__(self, *elements, fluid=None, text=None, css_class=None):
        super().__init__('div')
        for e in elements:
            if not isinstance(e, CoreElement):
                raise ValueError('Element must be an instance of CoreElement.')
            self.append_inner(e)
        self.fluid = fluid
        self.text = text
        opt = ''
        if self.fluid:
            opt = ' fluid'
        elif self.text:
            opt = ' text'
        self.css_class = css_class if css_class else f'ui{opt} container'
        