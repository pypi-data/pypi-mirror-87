from flask import url_for
from .prop import ValidProp

class Route:
    bp_func_name = ValidProp(str)
    
    def __init__(self, bp_func_name, **kwargs):
        self.bp_func_name = bp_func_name
        self.kwargs = kwargs
    
    def get_url(self, **kwargs):
        return url_for(self.bp_func_name, **self.kwargs, **kwargs)
    
    def __repr__(self):
        return f'Route(bp_func_name="{self.bp_func_name}", kwargs={self.kwargs})'