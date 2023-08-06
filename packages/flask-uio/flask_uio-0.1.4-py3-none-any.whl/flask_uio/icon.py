from .element import Element
from .prop import ValidProp

class Icon(Element):
    """Icon widget (default: Fomantic-UI)
    
    Args:
        
        * css_class (str): set icon css class.
    """
    def __init__(self, css_class):
        super().__init__('i', css_class)
        
class LinkIcon(Element):
    """LinkIcon widget (default: Fomantic-UI)
    
    Args:
        
        * css_class (str): set icon css class.
        * url (str): url.
        * target (str): '_self', '_blank', '_parent', '_top'
    """
    
    url = ValidProp(str)
    target = ValidProp(str)
    def __init__(self, css_class, url, target=None):
        super().__init__('a', css_class)
        self.url = url
        self.target = target
        self.attrs = [('href', self.url)]
        if self.target:
            self.attrs.append(('target', self.target))
        self.append_inner(Icon(css_class))