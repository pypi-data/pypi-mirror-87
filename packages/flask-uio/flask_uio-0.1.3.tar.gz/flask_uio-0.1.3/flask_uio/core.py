import secrets

class CoreElement:
    def __init__(self, tag_name):
        self.id = secrets.token_hex(4)
        self.tag_name = tag_name
        
    @property
    def tag_name(self):
        return self._tag_name.lower()
    
    @tag_name.setter
    def tag_name(self, value):
        if not isinstance(value, str):
            raise ValueError('tag_name must be string.')
        self._tag_name = value.lower()
    
    def get_html(self):
        raise NotImplementedError
        
    @staticmethod
    def _append_element(instance, prop_name, element):
        if not isinstance(element, CoreElement):
            raise ValueError(f'Can only append Element in {type(instance).__name__}\'s {prop_name}.')

        attr = instance.__dict__[prop_name]
        if getattr(attr, 'max_length', None):
            max_length = attr.max_length
            if max_length is not None and len(instance.__dict__[prop_name]) >= max_length:
                raise ValueError(f'Elements length of {prop_name} is at max ({max_length})')
            
        instance.__dict__[prop_name].append(element)
        
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
