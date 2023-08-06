from .element import Element, FieldElement
from .prop import ValidProp
from flask import request, flash
from flask_wtf.csrf import generate_csrf
class Form(Element):
    method = ValidProp(str)
    action = ValidProp(str)
    has_file = ValidProp(bool)
    
    def __init__(self, method='POST', action=None, has_file=None, css_class=None):
        super().__init__('form', hide_id=False)
        self.method = method
        self.append_inner(self.create_csrf_field())
        self.has_file = has_file
        
        self.attrs = []
        if self.method and self.method.upper() in ('GET', 'POST', 'PUT', 'DELETE'):
            self.attrs.append(('method', self.method))
        
        if self.attrs:
            self.attrs.append(('action', action))
            
        if self.has_file:
            self.attrs.append(('enctype', 'multipart/form-data'))
        
        self.css_class = css_class or f'ui form'
        self.errors = []
        
    @staticmethod
    def create_csrf_field():
        return Element('', inner_text=f'<input type="hidden" name="csrf_token" value="{generate_csrf()}"/>')
    
    def validate_on_submit(self):
        if request.method in ('PUT', 'POST', 'DELETE'):
            errors = []
            for _, f in self.__dict__.items():
                if isinstance(f, FieldElement) and f.validate():
                    errors.append(f.validate())
            self.errors = errors
            return len([e for e in self.errors if e.status]) == 0
        
    def render(self):
        raise NotImplementedError()
    
    @staticmethod
    def flash_success(message='Success', category='success'):
        flash(message, category)
    
    @staticmethod
    def flash_error(message='Fail', category='error'):
        flash(message, category)