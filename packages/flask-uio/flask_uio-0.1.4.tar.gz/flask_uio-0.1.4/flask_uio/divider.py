from .element import Element
from .prop import ValidProp

class Divider(Element):
    '''Divider Widget (default: Fomantic-UI)
    
    Args:

        * opt_css_class (str): set divider's option style. 
            - options: inverted, fitted, clearing, hidden, section, vertical, horizontal
            - alignments: left aligned, center aligned, right aligned        
        * css_class (str): set icon css class.
        * label (str): divider with text label.
    '''
    
    opt_css_class = ValidProp(str)
    css_class = ValidProp(str)
    label = ValidProp(str)
    
    def __init__(self, opt_css_class=None, css_class=None, label=None):
        super().__init__('div')
        self.opt_css_class = opt_css_class
        self.label = label
        self.css_class = css_class or f'ui {self.opt_css_class} divider'
        self.inner_text = self.label
        