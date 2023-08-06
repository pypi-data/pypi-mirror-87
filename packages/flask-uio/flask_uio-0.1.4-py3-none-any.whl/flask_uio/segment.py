from .element import Element, CoreElement
from .prop import ValidProp

class Segment(Element):
    opt_css_class = ValidProp(str)
    css_class = ValidProp(str)
    
    def __init__(self, *elements, opt_css_class=None, css_class=None):
        super().__init__('div')
        for e in elements:
            if not isinstance(e, CoreElement):
                raise ValueError('Element must be an instance of CoreElement.')
            self.append_inner(e)
        self.opt_css_class = opt_css_class
        self.css_class = css_class if css_class else f'ui {opt_css_class} segment'
        
class Segments(Element):
    opt_css_class = ValidProp(str)
    css_class = ValidProp(str)
    
    def __init__(self, *segments, opt_css_class=None, css_class=None):
        super().__init__('div')
        for e in segments:
            if not isinstance(e, Segment):
                raise ValueError('The object must be an instance of Segment.')
            self.append_inner(e)
        self.opt_css_class = opt_css_class
        self.css_class = css_class if css_class else f'ui {opt_css_class} segments'
        