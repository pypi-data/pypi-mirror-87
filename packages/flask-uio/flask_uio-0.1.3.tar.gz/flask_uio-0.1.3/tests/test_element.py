from flask_uio import Element
import pytest

def test_create_element_has_attributes():
    div = Element('div')
    assert hasattr(div, 'tag_name')
    assert hasattr(div, 'css_class')
    assert hasattr(div, 'attrs')
    assert hasattr(div, 'inner_text')
    assert hasattr(div, '_inner_elements')
    assert hasattr(div, '_prev_elements')
    assert hasattr(div, '_next_elements')
    assert hasattr(div, 'is_self_closing_tag')
    assert hasattr(div, 'hide_id')

testelement = Element('span', inner_text='Element for testing')
testcase1 = [
    (
        Element('div'), 
        {
            'tag_name': 'div',
            'css_class': None,
            'attrs': [],
            'inner_text': None,
            '_inner_elements': [],
            '_prev_elements': [],
            '_next_elements': [],
            'is_self_closing_tag': False,
            'hide_id': True,
        }
    ),
    (
        Element('div', 
            css_class='ui container', 
            inner_text='Test UI container', 
            inner_elements=[testelement],
            prev_elements=[testelement],
            next_elements=[testelement],
            attrs=[('style', 'margin: 40px;')],
            hide_id=False,
        ), 
        {
            'tag_name': 'div',
            'css_class': 'ui container',
            'attrs': [('style', 'margin: 40px;')],
            'inner_text': 'Test UI container',
            '_inner_elements': [testelement],
            '_prev_elements': [testelement],
            '_next_elements': [testelement],
            'is_self_closing_tag': False,
            'hide_id': False,
        }
    )
]
@pytest.mark.parametrize('test, expect', testcase1)
def test_default_value(test, expect):
    assert getattr(test, 'tag_name') == expect['tag_name']
    assert getattr(test, 'css_class') is expect['css_class']
    assert getattr(test, 'attrs') == expect['attrs']
    assert getattr(test, 'inner_text') is expect['inner_text']
    assert getattr(test, '_inner_elements') == expect['_inner_elements']
    assert getattr(test, '_prev_elements') == expect['_prev_elements']
    assert getattr(test, '_next_elements') == expect['_next_elements']
    assert getattr(test, 'is_self_closing_tag') == expect['is_self_closing_tag']
    assert getattr(test, 'hide_id') == expect['hide_id']
    inner_elements = getattr(test, '_inner_elements')
    if len(inner_elements) > 0:
        assert getattr(test, '_inner_elements')[0] == expect['_inner_elements'][0]
    prev_elements = getattr(test, '_prev_elements')
    if len(prev_elements) > 0:
        assert getattr(test, '_prev_elements')[0] == expect['_prev_elements'][0]
    next_elements = getattr(test, '_next_elements')
    if len(next_elements) > 0:
        assert getattr(test, '_next_elements')[0] == expect['_next_elements'][0]
        
def test_append_inner():
    e = Element('div')
    e.append_inner(testelement)
    assert testelement in e._inner_elements
    
def test_append_prev():
    e = Element('div')
    e.append_prev(testelement)
    assert testelement in e._prev_elements
    
def test_append_next():
    e = Element('div')
    e.append_next(testelement)
    assert testelement in e._next_elements
    
def test_find_element():
    
    class Div(Element):
        def __init__(self):
            super().__init__('div')
    
    class Span(Element):
        def __init__(self):
            super().__init__('span')
            
    e2 = Element('div')
    e2.append_inner(Div())
    e2.append_next(Span())
    
    e1 = Element('div')
    e1.append_prev(e2)
    
    e = Element('div')
    e.append_inner(e1)
    
    result = e.find_element(Div, Span)
    assert len(result) == 2
    
testcase2 = [
    (
        Element('div',
            css_class='ui segment',
            inner_text='hello world',
        ),
        '<div class="ui segment">hello world</div>'
    ),
    (
        Element('input',
            css_class='ui input',
            attrs=[('type', 'email'), ('name', 'email_address'), ('required', None)],
            hide_id=False,
        ),
        '<input id="replaced_id" class="ui input" type="email" name="email_address" required></input>'
    ),
    (
        Element('div',
            css_class='ui basic segment',
            inner_elements=[
                Element('h1', inner_text='FlaskUIO'),
                Element('p', inner_text='Testing flask_uio', css_class='custom'),
            ]
        ),
        '<div class="ui basic segment"><h1>FlaskUIO</h1><p class="custom">Testing flask_uio</p></div>'
    ),
    (
        Element('div',
            css_class='ui basic segment',
            inner_elements=[Element('h1', inner_text='FlaskUIO')],
            prev_elements=[Element('p', inner_text='Testing flask_uio', css_class='custom')]
        ),
        '<p class="custom">Testing flask_uio</p><div class="ui basic segment"><h1>FlaskUIO</h1></div>'
    ),
    (
        Element('div',
            css_class='ui basic segment',
            inner_elements=[Element('h1', inner_text='FlaskUIO')],
            next_elements=[Element('p', inner_text='Testing flask_uio', css_class='custom')]
        ),
        '<div class="ui basic segment"><h1>FlaskUIO</h1></div><p class="custom">Testing flask_uio</p>'
    ),
    (
        Element('br', is_self_closing_tag=True),
        '<br />'
    ),
    (
        Element('input', attrs=[('type', 'text'), ('value', 'some value'), ('name', 'txt1')], hide_id=False, is_self_closing_tag=True),
        '<input id="replaced_id" type="text" value="some value" name="txt1" />'
    )
]
@pytest.mark.parametrize('test, expect', testcase2)
def test_get_html(test, expect):
    assert test.get_html() == expect.replace("replaced_id", test.id)
    
    
    
    
