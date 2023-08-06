from .element import Element
from .prop import ValidProp, IntProp
from .func import get_word

class Grid(Element):
    nb_col = IntProp(1,16)
    opt_css_class = ValidProp(str)
    css_class = ValidProp(str)
    
    def __init__(self, *elements, nb_col=None, opt_css_class=None, css_class=None):
        super().__init__('div')
        self.nb_col = nb_col
        self.opt_css_class = opt_css_class
        opt = ''
        if self.nb_col:
            opt = ' ' + get_word(self.nb_col) + ' column'
        if self.opt_css_class:
            opt += ' ' + self.opt_css_class    
        self.css_class = css_class or f'ui{opt} grid'
        self.append_inner(*elements)
        
class GridColumn(Element):
    nb_wide = IntProp(1,16)
    css_class = ValidProp(str)
    
    def __init__(self, *elements, nb_wide=None, css_class=None):
        super().__init__('div')
        self.nb_wide = nb_wide
        opt = ''
        if self.nb_wide:
            opt = get_word(nb_wide) + ' wide '
        self.css_class = css_class or f'{opt}column'
        self.append_inner(*elements)
        
class GridRow(Element):
    nb_col = IntProp(1,16)
    css_class = ValidProp(str)
    
    def __init__(self, *elements, nb_col=None, css_class=None):
        super().__init__('div')
        self.nb_col = nb_col
        opt = ''
        if self.nb_col:
            opt = get_word(nb_col) + ' column '
        self.css_class = css_class or f'{opt}row'
        self.append_inner(*elements)