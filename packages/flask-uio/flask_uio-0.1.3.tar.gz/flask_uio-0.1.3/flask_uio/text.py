from .element import Element
from .prop import ValidProp

class Text(Element):
    """LinkIcon widget (default: Fomantic-UI)
    
    Args:
        
        * text (str): text to be displayed.
        * opt_css_class (str): set option css class.
            - color: primary, secondary, redred, orange, yellow, olive, green, teal, blue, violet, purple, pink, brown, grey, black
            - size: mini, tiny, small, medium, large, big, huge, massive
        * css_class (str): set text css class.
        
    """
    opt_css_class = ValidProp(str)
    css_class = ValidProp(str)
    
    def __init__(self, text, opt_css_class=None, css_class=None):
        super().__init__('span')
        self.opt_css_class = opt_css_class
        self.css_class = css_class if css_class else f'ui {self.opt_css_class} text'
        self.inner_text = text