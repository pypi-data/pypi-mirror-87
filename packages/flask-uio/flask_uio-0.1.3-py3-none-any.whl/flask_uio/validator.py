from flask import current_app
from werkzeug.utils import secure_filename
from datetime import date, datetime
from .prop import ValidProp
import os
import re

class Error:
    status = ValidProp(bool)
    message = ValidProp(str)
    
    def __init__(self, status, message=None):
        self.status = status
        self.message = message

class Validator:
    custom_error_message = ValidProp(str)
    
    def __init__(self, custom_error_message=None):
        self.error = Error(False)
        self.custom_error_message = custom_error_message
    
    def _update_error(self, status=False, message=None):
        self.error.status = status
        self.error.message = message
    
    def validate(self, field_name, value):
        pass

class RegexValidator(Validator):
    pattern_name = ValidProp(str)
    
    def __init__(self, pattern_raw_string, pattern_name):
        super().__init__()
        self.pattern = re.compile(pattern_raw_string)
        self.pattern_name = pattern_name
        
    def validate(self, field_name, value):
        if value:
            match = self.pattern.fullmatch(value)
            if match is None:
                self._update_error(True, self.custom_error_message or f'{field_name} is an invalid {self.pattern_name}.')
        return self.error
    
class EmailValidator(RegexValidator):
    def __init__(self):
        super().__init__(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', 'email address')
        
class PhoneValidator(RegexValidator):
    def __init__(self):
        super().__init__(r'[0][\d]{8,9}', 'phone number')

class DateValidator(Validator):
    _min = ValidProp(date)
    _max = ValidProp(date)
    
    def __init__(self, min=None, max=None, custom_error_message=None):
        super().__init__(custom_error_message)
        self.py_format = current_app.config['FLASK_UIO_DATE_DISPLAY_FORMAT']
        self._min = min
        self._max = max
        
    def validate(self, field_name, value):
        if value:
            try:
                value = datetime.strptime(value, self.py_format).date()
                if self._min:
                    if value < self._min:
                        fm_min = datetime.strftime(self._min, self.py_format)
                        self._update_error(True, self.custom_error_message or f'{field_name} cannot be earlier than {fm_min}.')
                    
                if not self.error.status and self._max:
                    if value > self._max:
                        fm_max = datetime.strftime(self._max, self.py_format)
                        self._update_error(True, self.custom_error_message or f'{field_name} cannot be later than {fm_max}.')
            except Exception:
                self._update_error(True, self.custom_error_message or f'{field_name} is invalid!')
        return self.error
    
class DateTimeValidator(Validator):
    _min = ValidProp(datetime)
    _max = ValidProp(datetime)
    
    def __init__(self, min=None, max=None, custom_error_message=None):
        super().__init__(custom_error_message)
        self.py_format = current_app.config['FLASK_UIO_DATETIME_DISPLAY_FORMAT']
        self._min = min
        self._max = max
        
    def validate(self, field_name, value):
        if value:
            try:
                value = datetime.strptime(value, self.py_format)
                if self._min:
                    if value < self._min:
                        fm_min = datetime.strftime(self._min, self.py_format)
                        self._update_error(True, self.custom_error_message or f'{field_name} cannot be earlier than {fm_min}.')
                    
                if not self.error.status and self._max:
                    if value > self._max:
                        fm_max = datetime.strftime(self._max, self.py_format)
                        self._update_error(True, self.custom_error_message or f'{field_name} cannot be later than {fm_max}.')
            except Exception:
                self._update_error(True, self.custom_error_message or f'{field_name} is invalid!')
        return self.error
    
class RequiredValidator(Validator):    
    def __init__(self, custom_error_message=None):
        super().__init__(custom_error_message)
    
    def validate(self, field_name, value):
        if value is None or (value is not None and str(value).strip() == ''):
            self.error.status = True
            self.error.message = self.custom_error_message or f'{field_name} is required.'
        else:
            self.error.status = False
            self.error.message = None
        return self.error
    
class StringValidator(Validator):
    _min = ValidProp(int)
    _max = ValidProp(int)
    
    def __init__(self, min=None, max=None, custom_error_message=None):
        super().__init__(custom_error_message)
        self._min = min
        self._max = max
        
    def validate(self, field_name, value):
        if value:
            if type(value) != str:
                self._update_error(True, self.custom_error_message or f'{field_name} is invalid.')
            
            if not self.error.status and self._min:
                if len(str(value)) < self._min:
                    self._update_error(True, self.custom_error_message or f'{field_name}\'s length must be at least {self._min}.')
                    
            if not self.error.status and self._max:
                if len(str(value)) > self._max:
                    self._update_error(True, self.custom_error_message or f'{field_name}\'s length cannot be greater than {self._max}.')
            
        return self.error
    
class UploadValidator(Validator):
    def __init__(self, custom_error_message=None):
        super().__init__(custom_error_message)

    def validate(self, field_name, data):
        if data:
            filename = secure_filename(data.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext.lower() not in current_app.config['UPLOAD_EXTENSIONS']:
                    self._update_error(True, f'The file is allowed.')
            else:
                self._update_error(True, f'The file has no content.')
            
        return self.error