from .element import Element, CoreElement
from .mixin import ReqInjectScriptMixin
from .prop import ValidProp, ValidSequenceProp
from .icon import Icon
from .button import Button
from .form import Form

class MessageModal(Element, ReqInjectScriptMixin):
    title = ValidProp(str)
    content_elements = ValidSequenceProp(CoreElement)
    action_elements = ValidSequenceProp(CoreElement)
    scroll_content = ValidProp(bool)
    icon = ValidProp(Icon)
    calling_id = ValidProp(str)
    
    def __init__(self, title, content_elements=None, action_elements=None, icon=None, scroll_content=False, calling_id=None):
        super().__init__('div')
        self.css_class = 'ui top aligned small modal'
        self.hide_id = False
        self.title = title.title()
        self.content_elements = content_elements
        self.action_elements = action_elements
        self.scroll_content = scroll_content
        self.icon = icon
        self.calling_id = calling_id
            
        header = Element('div', css_class='header', inner_text=f'{self.title}')
        if self.icon:
            header.append_inner(self.icon)
        self.append_inner(header)
        
        if self.content_elements:
            css_class = 'scrolling content' if self.scroll_content else 'content'
            content = Element('div', css_class=css_class, inner_elements=self.content_elements)
            self.append_inner(content)
            
        if self.action_elements:
            actions = Element('div', css_class='actions', inner_elements=self.action_elements)
            self.append_inner(actions)
            
        self.inject_script = f'load_modal("{self.calling_id}", "{self.id}");'
        
class ConfirmModal(MessageModal):
    def __init__(self, title, message, more_message=None, submit_url=None, yes='yes', yes_color='red', no='no', no_color='cancel', icon=None, calling_id=None, form_id=None):
        self.message = message
        self.more_message = more_message
        self.submit_url = submit_url
        self.yes_color = yes_color
        self.no_color = no_color
        self.form_id = form_id
        content = Element('p', inner_text=message)
        more_content = Element('', inner_text=more_message)
        yes = Button(yes, btn_type='submit', color=self.yes_color, form_id=self.form_id)
        no = Button(no, btn_type='button', color=self.no_color)
        form = []
        if self.submit_url:
            form.append(Form(action=submit_url).append_inner(yes, no))
        else:
            form.append(Element('div', css_class='ui form', inner_elements=[yes, no]))
        super().__init__(title, content_elements=[content, more_content], action_elements=form, icon=icon, calling_id=calling_id)