from collections import abc

class ValidProp:
    def __init__(self, prop_type, nullable=True, default=None):
        self._prop_type = prop_type
        self._nullable = nullable
        self._default = default
        
    def __set_name__(self, owner_clasds, prop_name):
        self.prop_name = prop_name
        
    def __set__(self, instance, value):
        if not self._nullable or value is not None:
            if not isinstance(value, self._prop_type):
                if isinstance(self._prop_type, abc.Sequence):
                    type_name = ''
                    for type_ in self._prop_type:
                        type_name += type_.__name__ if type_name == '' else f' or {type_.__name__}'
                    raise ValueError(f'{self.prop_name} must be {type_name}.')
                else:
                    raise ValueError(f'{self.prop_name} must be of type {self._prop_type.__name__}.')
        instance.__dict__[self.prop_name] = value
        
    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        else:
            prop_value = instance.__dict__.get(self.prop_name)
            if prop_value is None:
                return self._default
            return prop_value

class IntProp:
    def __init__(self, min_value=None, max_value=None, nullable=True):
        self.min_value = min_value
        self.max_value = max_value
        self.nullable = nullable
        
    def __set_name__(self, owner_class, name):
        self.name = name
        
    def __set__(self, instance, value):
        if not self.nullable or value is not None:
            if not isinstance(value, int):
                raise ValueError(f'{self.name} must be an int.')
            if self.min_value is not None and value < self.min_value:
                raise ValueError(f'{self.name} must be at least {self.min_value}')
            if self.max_value is not None and value > self.max_value:
                raise ValueError(f'{self.name} cannot exceed {self.max_value}')
        instance.__dict__[self.name] = value
        
    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self.name, None)
        
class ValidSequenceProp:
    def __init__(self, prop_type, nullable=True, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length
        self._prop_type = prop_type
        self._nullable = nullable
        
    def __set_name__(self, owner_class, prop_name):
        self.prop_name = prop_name
        
    def __set__(self, instance, value):
        if not isinstance(value, abc.Sequence):
            if self._nullable and value is None:
                pass
            else:
                raise ValueError(f'{self.prop_name} must be a sequence type.')
            
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(f'{self.prop_name} must contain at least {self.min_length} elements')
            
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f'{self.prop_name} cannot contain more than {self.max_length} elements')
        
        if value is not None:
            for index, item in enumerate(value):
                if not isinstance(item, self._prop_type):
                    raise ValueError(f'Item at index {index} is not an instance of {self._prop_type.__name__}.')
        
        instance.__dict__[self.prop_name] = list(value) if value else []
        
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            if self.prop_name not in instance.__dict__:
                instance.__dict__[self.prop_name] = []
            return instance.__dict__.get(self.prop_name)