from .element import Element
from .mixin import ReqInjectScriptMixin
from .menu import Menu, MenuItem
from .icon import Icon

class SideBar(Element, ReqInjectScriptMixin):
    def __init__(self):
        super().__init__('')
        self.sidebar_menu = Menu(css_class='ui sidebar inverted vertical menu', hide_id=False)
        self.content = Element('div', css_class='pusher')
        self.nav_menu = Menu(css_class='ui primary inverted large stackable menu custom')
        self.toggle = MenuItem('', '', icon=Icon('bars icon'), hide_id=False)
        self.nav_menu.append_inner(self.toggle)
        # combined
        self.content.append_inner(self.nav_menu)
        self.sidebar_menu.append_next(self.content)
        self.append_inner(self.sidebar_menu)
        self.inject_script = f'$("#{self.toggle.id}").click(function () {{$("#{self.sidebar_menu.id}").sidebar("toggle");}})'