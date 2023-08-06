from .core import CoreElement
from .prop import ValidProp, ValidSequenceProp
from .validator import Validator, Error, RequiredValidator
from flask import request

class Element(CoreElement):
    tag_name = ValidProp(str)
    css_class = ValidProp(str)
    attrs = ValidSequenceProp(tuple)
    inner_text = ValidProp(str)
    _inner_elements = ValidSequenceProp(CoreElement)
    _prev_elements = ValidSequenceProp(CoreElement)
    _next_elements = ValidSequenceProp(CoreElement)
    is_self_closing_tag = ValidProp(bool)
    hide_id = ValidProp(bool)
    
    def __init__(self, tag_name, css_class=None, inner_text=None, inner_elements=None, prev_elements=None, next_elements=None, attrs=None, is_self_closing_tag=False, hide_id=True):
        super().__init__(tag_name)
        self.tag_name = tag_name
        self.css_class = css_class
        self.attrs = attrs
        self.inner_text = inner_text
        self._inner_elements = inner_elements
        self._prev_elements = prev_elements
        self._next_elements = next_elements
        self.is_self_closing_tag = is_self_closing_tag
        self.hide_id = hide_id
    
    def get_html(self):
        # inner text
        inner_text = self.inner_text if self.inner_text else ''
        
        # attributes
        attrs = ''
        if self.attrs:
            for k, v in self.attrs:
                if k and v is not None:
                    attrs += f' {k}="{v}"'
                elif k and v is None:
                    attrs += f' {k}'
            
        # inner_elements
        inner_element_html = ''
        if self._inner_elements:
            for obj in self._inner_elements:
                inner_element_html += obj.get_html()
                
        # prev_elements
        prev_element_html = ''
        if self._prev_elements:
            for obj in self._prev_elements:
                prev_element_html += obj.get_html()
                
        # next_elements
        next_element_html = ''
        if self._next_elements:
            for obj in self._next_elements:
                next_element_html += obj.get_html()     
                
        # css class
        css_class = ''
        if self.css_class:
            css_class = f' class="{self.css_class}"'
                
        # tag id
        tag_id = '' if self.hide_id else f' id="{self.id}"'
        
        if self.tag_name == '':
            html = f'{inner_text}{inner_element_html}'
        else:
            if self.is_self_closing_tag:
                html = f'<{self.tag_name}{tag_id}{css_class}{attrs} />'
            else:
                html = f'<{self.tag_name}{tag_id}{css_class}{attrs}>{inner_element_html}{inner_text}</{self.tag_name}>'
        
        return prev_element_html + html + next_element_html
        
    def append_inner(self, *elements):
        for element in elements:
            self._append_element(self, '_inner_elements', element)
        return self
        
    def append_prev(self, *elements):
        for element in elements:
            self._append_element(self, '_prev_elements', element)
        return self
        
    def append_next(self, *elements):
        for element in elements:
            self._append_element(self, '_next_elements', element)   
        return self     
    
    def find_element(self, *type_):
        result = []
        if self._inner_elements:
            for obj in self._inner_elements:
                if isinstance(obj, type_):
                    result += [obj]
                else:
                    if hasattr(obj, 'find_element'):
                        finding = obj.find_element(type_)
                        if len(finding) > 0:
                            result += finding
        if self._prev_elements:
            for obj in self._prev_elements:
                if isinstance(obj, type_):
                    result += [obj]
                else:
                    if hasattr(obj, 'find_element'):
                        finding = obj.find_element(type_)
                        if len(finding) > 0:
                            result += finding
        if self._next_elements:
            for obj in self._next_elements:
                if isinstance(obj, type_):
                    result += [obj]
                else:
                    if hasattr(obj, 'find_element'):
                        finding = obj.find_element(type_)
                        if len(finding) > 0:
                            result += finding
        return result
    
class Link(Element):
    href = ValidProp(str)
    
    def __init__(self, href='index.css'):
        self.href = href
        super().__init__('link', attrs=[('rel', 'stylesheet'), ('type', 'text/css'), ('href', self.href)], is_self_closing_tag=True)
        
class Script(Element):
    src = ValidProp(str)
    
    def __init__(self, src='index.js'):
        self.src = src
        super().__init__('script', attrs=[('src', self.src)])
        
class BaseHead(CoreElement):
    title = ValidProp(str, nullable=False)
    element = ValidSequenceProp(CoreElement)
    link = ValidSequenceProp(CoreElement)
    script = ValidSequenceProp(CoreElement)
    
    def __init__(self, title, element=None, link=None, script=None):
        super().__init__('head')
        self.title = title
        self.element = element
        self.link = link
        self.script = script
        self.element.append(Element('title', inner_text=title))
    
    def append(self, *elements):
        for element in elements:
            self._append_element(self, 'element', element)
        
    def append_link(self, *href_args):
        for href in href_args:
            if not isinstance(href, str):
                raise ValueError('Each href must be a string.')
            link = Link(href)
            self._append_element(self, 'link', link)
        
    def append_script(self, *src_args):
        for src in src_args:
            if not isinstance(src, str):
                raise ValueError('Each src must be a string.')
            self._append_element(self, 'script', Script(src))

    def get_html(self):
        html = ''
        fields = ['element', 'link', 'script']
        for field in fields:
            elements = getattr(self, field)
            for obj in elements:
                html += obj.get_html()
        
        return f'<{self.tag_name}>{html}</{self.tag_name}>'
    
class BaseBody(CoreElement):
    element = ValidSequenceProp(CoreElement)
    script = ValidSequenceProp(CoreElement)
    _injected_script = ValidSequenceProp(CoreElement)
    
    def __init__(self, element=None, script=None, injected_script=None):
        super().__init__('body')
        self.element = element
        self.script = script
        self._injected_script = injected_script
    
    def append(self, *elements):
        for element in elements:
            self._append_element(self, 'element', element)
        
    def append_script(self, *src_args):
        for src in src_args:
            if not isinstance(src, str):
                raise ValueError('Each src must be a string.')
            self._append_element(self, 'script', Script(src))
            
    def append_injected_script(self, *elements):
        for element in elements:
            self._append_element(self, '_injected_script', element)

    def get_html(self):
        html = ''
        injected_script = ''
        fields = ['element', 'script']
        for field in fields:
            for obj in getattr(self, field):
                html += obj.get_html()
        
        # Check for injected script
        if len(self._injected_script) > 0:
            for script in self._injected_script:
                injected_script += script.get_html()
        
        return f'<{self.tag_name}>{html}{injected_script}</{self.tag_name}>'
    
class FieldElement(Element):
    name = ValidProp(str)
    placeholder = ValidProp(str)
    disabled = ValidProp(bool)
    required = ValidProp(bool)
    readonly = ValidProp(bool)
    error = ValidProp(Error)
    validators = ValidSequenceProp(Validator)
    
    def __init__(
        self, 
        tag_name, 
        id=None, 
        name=None, 
        placeholder=None, 
        disabled=False, 
        required=False, 
        readonly=False, 
        css_class=None, 
        attrs=None,
        validators=None,
        ):
        
        super().__init__(tag_name, hide_id=False, css_class=css_class, attrs=attrs)
        
        self.id = id if id else self.id
        self.name = name.replace('_', ' ').title()
        self.placeholder = placeholder if placeholder else self.name
        self.disabled = disabled
        self.required = required
        self.validators = []
        if self.required:
            self.validators.append(RequiredValidator())
        if validators:
            self.validators = self.validators + validators
        self.readonly = readonly
        self.error = Error(False)
        
        main_attrs = []
        
        if self.name:
            main_attrs.append(('name', self.name))
        if self.placeholder:
            main_attrs.append(('placeholder', self.placeholder))
        # turn on if use html5 validator
        # if self.required:
        #     main_attrs.append(('required', None))
        if self.readonly:
            main_attrs.append(('readonly', None))
        if self.disabled:
            main_attrs.append(('disabled', None))
        
        if len(list(self.attrs)) == 0:
            self.attrs = []
            
        self.attrs = main_attrs + self.attrs
            
        if len(self.attrs) == 0:
            self.attrs = None
            
    @property
    def form_data(self):
        is_multiple = getattr(self, 'is_multiple', None)
        if is_multiple:
            return request.form.getlist(self.name)
        return request.form.get(self.name, None)
    
    @property
    def data(self):
        pass
    
    @data.setter
    def data(self, value):
        pass
    
    def validate(self):
        if request.method in ('PUT', 'POST', 'DELETE'):
            for v in self.validators:
                if not isinstance(v, Validator):
                    raise Exception('validator must be an instance of Validator.')
                self.error = v.validate(self.name, self.form_data)
                if self.error.status:
                    break
            return self.error