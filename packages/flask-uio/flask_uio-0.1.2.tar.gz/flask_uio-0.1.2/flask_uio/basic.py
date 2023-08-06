from .element import Element, BaseBody, BaseHead
from .mixin import ReqInjectScriptMixin

class Head(BaseHead):
    def __init__(self, title, element=None, link=None, script=None):
        super().__init__(title, element, link, script)
        self.element.append(Element('meta', attrs=[('charset', 'UTF-8')]))
        self.element.append(Element('meta', attrs=[('name', 'viewport'), ('content', 'width=device-width, initial-scale=1.0')]))
        
class Body(BaseBody):
    def __init__(self, element=None, script=None):
        super().__init__(element, script)
        
    def get_html(self):
        html = ''
        
        for obj in getattr(self, 'element'):
            html += obj.get_html()
            
        for obj in getattr(self, 'script'):
            html += obj.get_html()
        
        result = []
        for obj in getattr(self, 'element'):
            if isinstance(obj, ReqInjectScriptMixin):
                script = Element('script', inner_text=obj.inject_script)
                self.append_injected_script(script)
            
            if isinstance(obj, Element):
                result += obj.find_element(ReqInjectScriptMixin)
                for field in result:
                    script = Element('script', inner_text=field.inject_script)
                    self.append_injected_script(script)
                    
        if len(self._injected_script) > 0:
            for script in self._injected_script:
                html += script.get_html()
        
        return f'<{self.tag_name}>{html}</{self.tag_name}>'
    
class Document():
    def __init__(self, title):
        self.head = Head(title)
        self.body = Body()
    
    def get_html(self):
        doctype = '<!DOCTYPE html>'
        html = Element('html', attrs=[('lang', 'en')])
        head_html = self.head.get_html()
        body_html = self.body.get_html()
        html.inner_text = head_html + body_html
        return doctype + html.get_html()