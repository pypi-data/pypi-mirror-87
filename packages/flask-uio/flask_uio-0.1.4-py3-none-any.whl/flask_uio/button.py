from .element import Element
from .prop import ValidProp

class Button(Element):
    """Button widget (default: Fomantic-UI)
    
    Args:
    
        * title (str): set button's name. 
        * btn_type (str): 'button', 'submit', 'reset'.
        * url (str): provide url if the behavior of button is a link.
        * basic (bool): enable basic style, if no css_class.
        * fluid (bool): enable fluid style, if no css_class.
        * tertiary (bool): enable tertiary style, if no css_class.
        * color (str): change button's color.
        * css_class (str): override default css class.
    """
    title = ValidProp(str)
    url = ValidProp(str)
    btn_type = ValidProp(str)
    css_class = ValidProp(str)
    basic = ValidProp(bool)
    fluid = ValidProp(bool)
    color = ValidProp(str)
    tertiary = ValidProp(bool)
    form_id = ValidProp(str)
    
    def __init__(self, title, btn_type=None, url=None, form_id=None, basic=None, fluid=None, tertiary=None, color='primary', css_class=None):
        super().__init__('a' if url else 'input', hide_id=False)
        self.title = title
        self.url = url
        self.btn_type = btn_type
        self.basic = basic
        self.fluid = fluid
        self.tertiary = tertiary
        self.color = color
        self.form_id = form_id
        if self.url:
            self.inner_text = self.title
            self.attrs = [('href', self.url)]
        else:
            self.attrs = self.attrs + [('value', title.title()), ('type', btn_type)]
        if self.form_id:
            self.attrs.append(('form', self.form_id))
        self.css_class = css_class or f'ui{self._get_opt_css_class()} button'
        
    def _get_opt_css_class(self):
        opt_css_class = ''    
        if self.basic:
            opt_css_class += ' basic'
        if self.fluid:
            opt_css_class += ' fluid'
        if self.tertiary:
            opt_css_class += ' tertiary'
        if self.color:
            opt_css_class += f' {self.color}'
        return opt_css_class
            
        