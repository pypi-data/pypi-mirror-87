from .element import Element
from .prop import ValidProp
        
class A(Element):
    """A widget (default: Fomantic-UI)
    
    Args:
        
        * url (str): url.
        * target (str): '_self', '_blank', '_parent', '_top'.
        * text (str); link's text.
    """
    
    url = ValidProp(str, False)
    target = ValidProp(str)
    
    def __init__(self, *elements, url=None, text=None, target=None):
        super().__init__('a')
        self.url = url
        self.target = target
        self.inner_text = text
        self.attrs = [('href', self.url)]
        if self.target:
            self.attrs.append(('target', self.target))
        self.append_inner(*elements)