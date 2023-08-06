import pytest
from flask_uio import CoreElement

tag_names = [
    ('div', 'div'),
    ('Div', 'div'),
    ('DIV', 'div'),
]

def setup_module(module):
    print('-----setup-----')

def teardown_module(module):
    print('-----teardown-----')

@pytest.mark.parametrize('tag_name, result', tag_names)
def test_tag_name_is_lower_case(tag_name, result):
    e = CoreElement(tag_name)
    assert e.tag_name == result
    
def test_append_element_has_element():
    e1 = CoreElement('div')
    e1._inner_elements = []
    e1._prev_elements = []
    e1._next_elements = []
    e2 = CoreElement('span')
    CoreElement._append_element(e1, '_inner_elements', e2)
    CoreElement._append_element(e1, '_prev_elements', e2)
    CoreElement._append_element(e1, '_next_elements', e2)
    e1_inner_elements = getattr(e1, '_inner_elements')
    e1_prev_elements = getattr(e1, '_prev_elements')
    e1_next_elements = getattr(e1, '_next_elements')
    assert len(e1_inner_elements) == 1
    assert len(e1_prev_elements) == 1
    assert len(e1_next_elements) == 1
    assert e2 in e1_inner_elements
    assert e2 in e1_prev_elements
    assert e2 in e1_next_elements
    
def test_set_tag_name_with_bad_value():
    with pytest.raises(ValueError):
        e = CoreElement(100)
        
    with pytest.raises(ValueError):
        e = CoreElement(True)
        
    with pytest.raises(ValueError):
        e = CoreElement(None)
    
        
        
        