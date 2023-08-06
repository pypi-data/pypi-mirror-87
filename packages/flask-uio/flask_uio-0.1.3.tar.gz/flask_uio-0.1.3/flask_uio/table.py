from datetime import datetime
from operator import itemgetter
from flask import request, url_for, current_app
from flask_sqlalchemy.model import DefaultMeta
from flask_sqlalchemy import Pagination
from .element import CoreElement
from .mixin import ReqInjectScriptMixin
from .prop import IntProp, ValidProp, ValidSequenceProp
from .route import Route
from .a import A
from .element import Element
from .modal import ConfirmModal
from .form import Form
from .button import Button
from sqlalchemy.orm.attributes import InstrumentedAttribute

class TableColItem:
    name = ValidProp(str)
    allow_search = ValidProp(bool)
    is_key=ValidProp(bool)
    is_hidden=ValidProp(bool)
    default_sort=ValidProp(bool)
    default_sort_asc=ValidProp(bool)
    
    def __init__(self, name, column=None, allow_search=True, is_key=False, is_hidden=False, default_sort=False, default_sort_asc=False):
        self.name = name
        self.column = column
        self.allow_search = allow_search
        self.is_key = is_key
        self.is_hidden = is_hidden
        self.default_sort = default_sort
        self.default_sort_asc = default_sort_asc
        
    @property
    def column(self):
        return getattr(self, '_column', None)
    
    @column.setter
    def column(self, value):
        if value is not None:
            if type(value) is not InstrumentedAttribute:
                raise ValueError('sort column must be a type of InstrumentedAttribute.')
        setattr(self, '_column', value)
    
    @property
    def friendly_name(self):
        return self.name.replace('_', ' ').title()
    
    def __repr__(self):
        return f"ColItem(name='{self.name}', column={self.column}, allow_search={self.allow_search})"

class TableDateItem(TableColItem):
    format = ValidProp(str)
    display_format = ValidProp(str)
    
    def __init__(self, name, db_column=None, is_hidden=False, format=None, display_format=None, default_sort=False, default_sort_asc=False):
        super().__init__(name, db_column, allow_search=False, is_hidden=is_hidden, default_sort=default_sort, default_sort_asc=default_sort_asc)
        self.format = format or current_app.config['FLASK_UIO_DATE_FORMAT']
        self.display_format = display_format or current_app.config['FLASK_UIO_DATE_DISPLAY_FORMAT']
        
    def get_value(self, date_string):
        if not isinstance(date_string, str):
            raise ValueError(f'date string must be a string type.')
        return datetime.strptime(date_string, self.format).date()
    
    def get_text(self, date):
        if type(date) not in (datetime.date, datetime):
            raise ValueError(f'date string must be a date type.')
        return datetime.strftime(date, self.display_format)
    
class TableDateTimeItem(TableColItem):
    format = ValidProp(str)
    display_format = ValidProp(str)
    
    def __init__(self, name, db_column=None, is_hidden=False, format=None, display_format=None, default_sort=False, default_sort_asc=False):
        super().__init__(name, db_column, allow_search=False, is_hidden=is_hidden, default_sort=default_sort, default_sort_asc=default_sort_asc)
        self.format = format or current_app.config['FLASK_UIO_DATETIME_FORMAT']
        self.display_format = display_format or current_app.config['FLASK_UIO_DATETIME_DISPLAY_FORMAT']
        
    def get_value(self, datetime_string):
        if not isinstance(datetime_string, str):
            raise ValueError(f'date string must be a string type.')
        return datetime.strptime(datetime_string, self.format).date()
    
    def get_text(self, datetime_):
        if not isinstance(datetime_, datetime):
            raise ValueError(f'date string must be a datetime type.')
        return datetime.strftime(datetime_, self.display_format)
    
class TableStaticLinkItem(TableColItem):
    fp_col_name = ValidProp(str)
    
    def __init__(self, name, db_column=None, is_hidden=False, default_sort=False, default_sort_asc=False, fp_col_name=None):
        super().__init__(name, db_column, allow_search=False, is_hidden=is_hidden, default_sort=default_sort, default_sort_asc=default_sort_asc)
        self.fp_col_name = fp_col_name
    
class Table(CoreElement, ReqInjectScriptMixin):
    per_page = IntProp(min_value=1)
    pages = IntProp(min_value=0)
    total = IntProp(min_value=0)
    prev_num = IntProp(min_value=1)
    next_num = IntProp(min_value=1)
    css_class = ValidProp(str)
    inject_script = ValidProp(str)
    reload_route = ValidProp(Route)
    detail_route = ValidProp(Route)
    new_route = ValidProp(Route)
    edit_route = ValidProp(Route)
    delete_route = ValidProp(Route)
    excludes = ValidSequenceProp(str)
    allow_sort = ValidProp(bool)
    allow_search = ValidProp(bool)
    allow_paginate = ValidProp(bool)
    search_text = ValidProp(str)
    search_option = ValidProp(str)
    inject_script = ValidProp(str)
    
    def __init__(
            self, 
            title, 
            items=None, 
            colitems=None, 
            css_class=None, 
            reload_route=None, 
            new_route=None, 
            detail_route=None, 
            edit_route=None, 
            delete_route=None, 
            excludes=None,
            per_page=None, 
            page=None, 
            pages=None, 
            total=None, 
            prev_num=None, 
            next_num=None, 
            allow_sort=False, 
            allow_search=False, 
            allow_paginate=False,
        ):
        
        super().__init__('table')
        self.title = title
        self._ref_title = title.replace(' ', '-').lower()
        self._ref_form_paginate_id = f'form-paginate-table-{self._ref_title}'
        self._ref_form_paginate_text_id = f'form-paginate-text-table-{self._ref_title}'
        self._ref_form_search_id = f'form-search-table-{self._ref_title}'
        self._ref_form_search_text_id = f'form-search-text-table-{self._ref_title}'
        self._ref_form_search_option_id = f'form-search-option-table-{self._ref_title}'
        
        self.items = items or []
        self.colitems = colitems or []
        self.per_page = per_page
        self.pages = pages 
        self.total = total
        
        # page
        if request.method == 'POST':
            page = request.form.get(self._ref_form_paginate_text_id, None)
            if page is None:
                page = request.args.get('_page', None)
        elif request.method == 'GET':
            page = request.args.get('_page', None) or page
        self.page = page
        
        # search
        if request.method == 'POST':
            search_text = request.form.get(self._ref_form_search_text_id, None)
            search_option = request.form.get(self._ref_form_search_option_id, None)
            if search_text and search_option:
                self.page = 1
            if search_text is None:
                search_text = request.args.get('_search_text', None)
            if search_option is None:
                search_option = request.args.get('_search_option', None)
            self.search_text = search_text
            self.search_option = search_option
        elif request.method == 'GET':
            self.search_text = request.args.get('_search_text', None)
            self.search_option = request.args.get('_search_option', None)
        
        # prev page
        self.prev_num = prev_num
        if self.prev_num is None and self.page and self.page > 1:
            self.prev_num = self.page - 1
            
        # next page
        self.next_num = next_num
        if self.next_num is None and self.page:
            self.next_num = self.page + 1
            
        self.reload_route = reload_route
        self.detail_route = detail_route
        self.new_route = new_route
        self.edit_route = edit_route
        self.delete_route = delete_route
        self.excludes = excludes    
        self.allow_sort = allow_sort
        self.allow_search = allow_search
        self.allow_paginate = allow_paginate
        
        default_css = 'ui compact celled table'
        if self.detail_route:
            default_css = 'ui selectable compact celled table'
        self.css_class = css_class or default_css
        self.inject_script = ''
        
    def refresh(self, paginate):
        if not isinstance(paginate, Pagination):
            raise ValueError('paginate must be an instance of Pagination.')
        self.items = paginate.items
        self.page = paginate.page
        self.total = paginate.total
        self.per_page = paginate.per_page
        self.pages = paginate.pages
    
    @property
    def paginate(self):
        return {'page': self.page, 'per_page': self.per_page, 'error_out': False}
        
    @property
    def items(self):
        current_args_dicts = self.current_args_dicts.copy()
        items = getattr(self, '_items', [])
        for key in current_args_dicts.keys():
            header = key[5:]
            if header in self.headers:
                direction = current_args_dicts.get(key)
                if direction == 'asc':
                    items.sort(key=itemgetter(header))
                else:
                    items.sort(key=itemgetter(header), reverse=True)
        return items
    
    @items.setter
    def items(self, data):
        if not isinstance(data, list):
            raise ValueError('data must be a list of dict.')
        
        list_dict = []
        for index, item in enumerate(data):
            data_dict = {}
            try:
                if isinstance(item, dict):
                    data_dict = item
                elif hasattr(type(item), '__class__') and type(item).__class__ == DefaultMeta:
                    data_dict = item.__dict__
                    del data_dict['_sa_instance_state']
                else:
                    data_dict = item._asdict()
            except Exception as ex:
                raise Exception(f'item not supported.(index: {index}, {item})')
            list_dict.append(data_dict)
            
        setattr(self, '_items', list_dict)
    
    @property
    def headers(self):
        return [item.name for item in self.colitems]
    
    @property 
    def colitems(self):
        colitems = getattr(self, '_colitems', None)
        if colitems:
            return colitems
        if len(self._items) > 0:
            return [TableColItem(name) for name in list(self._items[0].keys())]
        return []
    
    @colitems.setter
    def colitems(self, value):
        if not isinstance(value, list):
            raise ValueError('colitems must be a list of ColItem.')
        
        for v in value:
            if not isinstance(v, TableColItem):
                raise ValueError('item must be an instance of ColItem.')
        
        setattr(self, '_colitems', value)
    
    @property
    def current_args_dicts(self):
        item = {}
        for h in self.headers:
            if h.lower() not in self.excludes and self.reload_route:
                sort_key = f'sort_{h}'
                sort_value = request.args.get(sort_key, None)
                if sort_value:
                    item.update({sort_key: sort_value})
        if self.search_text:
            item.update({'_search_text': self.search_text})
        if self.search_option:
            item.update({'_search_option': self.search_option})
        if self.page:
            item.update({'_page': self.page})
        
        return item
    
    @property
    def order_by(self):
        current_args_dicts = self.current_args_dicts
        output = []
        for col in self.colitems:
            sort_key = f'sort_{col.name}'
            sort_value = current_args_dicts.get(sort_key, None)
            if sort_value:
                if sort_value == 'asc':
                    output.append(col.column.asc())
                elif sort_value == 'desc':
                    output.append(col.column.desc())
        if len(output) == 0:
            for col in self.colitems:
                if col.default_sort:
                    if col.default_sort_asc:
                        output.append(col.column.asc())
                    else:
                        output.append(col.column.desc())
        return tuple(output)
    
    @property
    def filter(self):
        output = []
        if self.search_text and self.search_option:
            for item in self.colitems:
                if item.name == self.search_option:
                    output.append(item.column.ilike(f'%{self.search_text}%'))
        return tuple(output)

    @property
    def next_sort_dicts(self):
        item = {}
        for h in self.headers:
            if h.lower() not in self.excludes and self.reload_route:
                sort_key = f'sort_{h}'
                sort_value = request.args.get(sort_key, None)
                if sort_value:
                    if sort_value == 'asc':
                        item.update({sort_key: 'desc'})
                else:
                    item.update({sort_key: 'asc'})
        return item
    
    @property
    def column_sort_dicts(self):
        item = {}
        current_args_dicts = self.current_args_dicts.copy()
        for h in self.headers:
            temp_dict = dict(current_args_dicts)
            
            if h.lower() not in self.excludes and self.reload_route:
                sort_key = f'sort_{h}'
                if current_args_dicts.get(sort_key, None):
                    del temp_dict[sort_key]
                
                d = {}
                d.update(temp_dict)
                if self.next_sort_dicts.get(sort_key):
                    d.update({sort_key: self.next_sort_dicts.get(sort_key)})
                sort_dict = {sort_key: d}
                item.update(sort_dict)
        return item

    @property
    def page(self):
        return getattr(self, '_page', 1)
            
    @page.setter
    def page(self, value):
        if value:
            setattr(self, '_page', int(value))
        else:
            setattr(self, '_page', 1)

    def _get_colspans(self):
        colspans = len(self.headers)
        
        if self.edit_route or self.delete_route:
            colspans += 1
            
        for h in self.headers:
            if h.lower() in self.excludes:
                colspans -= 1
                
        return colspans

    def _get_header_html(self):
        current_args_dict = self.current_args_dicts.copy()
        tb_header = ''
        if (self.edit_route or self.delete_route) and len(self.items) > 0:
            tb_header = '<th class="collapsing"></th>'
            
        for col in self.colitems:
            header_name = col.name.replace('_', ' ').title()
            if not col.is_hidden and col.name.lower() not in self.excludes:
                if self.reload_route and self.allow_sort:
                    sort_key = f'sort_{col.name}'
                    sort_value = current_args_dict.get(sort_key, None)
                    url = self.reload_route.get_url(**self.column_sort_dicts.get(sort_key))
                    if sort_value:
                        icon = ''
                        if sort_value == 'asc':
                            icon = '<i class="sort amount down alternate grey icon"></i>'
                        elif sort_value == 'desc':
                            icon = '<i class="sort amount down grey icon"></i>'
                        tb_header += f'<th><a href="{url}">{icon}{header_name}</a></th>'
                    else:
                        tb_header += f'<th><a href="{url}">{header_name}</a></th>'
                else:
                    tb_header += f'<th>{header_name}</th>'
        return f'<thead><tr>{tb_header}</tr></thead>'
        
    def _format_col_data(self, colitem, data, item):
        output = data
        if isinstance(colitem, TableDateItem):
            if isinstance(data, str):
                output = colitem.get_text(colitem.get_value(data))
            elif type(data) in (datetime.date, datetime):
                output = colitem.get_text(data)
        elif isinstance(colitem, TableDateTimeItem):
            if isinstance(data, str):
                output = colitem.get_text(colitem.get_value(data))
            elif isinstance(data, datetime):
                output = colitem.get_text(data)
        elif isinstance(colitem, TableStaticLinkItem):
            fp = item.get(colitem.fp_col_name)
            if fp:
                url = url_for('static', filename=fp.replace('static/', ''))
                output = A(text=data, url=url).get_html()
            else:
                output = str(data)
        return output
        
    def _get_body_html(self):    
        tb_rows = ''
        for item in self.items:
            tb_row = ''
                    
            detail_kwarg = {}
            for col in self.colitems:
                data = item.get(col.name)
                if col.is_key:
                    detail_kwarg.update(**{col.name: data})
                    
                if not col.is_hidden and col.name.lower() not in self.excludes:
                    detail_url = ''
                    if self.detail_route and bool(detail_kwarg):
                        detail_url = f'onclick="window.location=\'{self.detail_route.get_url(**detail_kwarg)}\';"'
                    data = self._format_col_data(col, data, item)    
                    tb_row += f'<td {detail_url}>{data if data is not None else "N/A"}</td>'
                
            # actions
            tb_action = ''
            if (self.edit_route or self.delete_route) and bool(detail_kwarg):
                actions = Element('div', css_class="ui small basic icon buttons")
                if self.edit_route:
                    actions.append_inner(
                        Element('a', 
                            css_class='ui button', 
                            inner_text='<i class="pen icon"></i>', 
                            attrs=[('href', self.edit_route.get_url(**detail_kwarg))]
                        )
                    )
                if self.delete_route:
                    delete_info = ''
                    for col in self.colitems:
                        if not col.is_hidden or col.name.lower() not in self.excludes:
                            delete_info += f'<li>{col.friendly_name}: {self._format_col_data(col, item.get(col.name), item)}</li>'
                    delete_info = f'<ul>{delete_info}</ul>'
                    delete_button = Element('div', css_class='ui button', inner_text='<i class="trash alternate red icon"></i>', hide_id=False)
                    confirm = ConfirmModal(
                        title=self.title,
                        submit_url=self.delete_route.get_url(**detail_kwarg),
                        message='Are you sure to delete the following record?',
                        more_message=delete_info,
                        no='Cancel',
                        yes='Yes, Delete',
                        calling_id=delete_button.id,
                    )
                    actions.append_inner(delete_button)
                    actions.append_inner(confirm)
                    self.inject_script += f'load_modal("{delete_button.id}", "{confirm.id}");'
                tb_action += '<td>' + actions.get_html() + '</td>'
            
            tb_row = f'<tr>{tb_action}{tb_row}</tr>'    
            tb_rows += tb_row
            
        if len(self.items) == 0:
            tb_rows = f'<tbody><tr><td colspans="{self._get_colspans()}">No record!</td></tr></tbody>'    
        else:
            tb_rows = f'<tbody>{tb_rows}</tbody>'
            
        return tb_rows

    def _get_footer_html(self):
        if self.reload_route and len(self.items) > 0:
            pagination = Element('div', css_class='ui pagination stackable fluid secondary menu', attrs=[('style', 'padding-top:5px; padding-bottom:5px;')])
            
            current_args_dict = self.current_args_dicts.copy()
            
            if self.total or self.pages:
                text = f'Total: {self.total}'
                text += f', Pages: {self.pages}'
                pagination.append_inner(Element('div', css_class='item', inner_text=text))
            
            if self.page > 1:
                current_args_dict.update({'_page': 1})
                url = self.reload_route.get_url(**current_args_dict)
                pagination.append_inner(Element('a', css_class='item', inner_text='First', attrs=[('href', url)]))
                
            if self.prev_num and self.page and self.page > 2:
                current_args_dict.update({'_page': self.prev_num})
                url = self.reload_route.get_url(**current_args_dict)
                pagination.append_inner(Element('a', css_class='icon item', inner_text='<i class="angle left icon"></i>', attrs=[('href', url)]))
                
            if self.page:
                pagination.append_inner(Element('div', css_class='active item', inner_text=f'{self.page}'))
                
            if self.next_num:
                if self.pages is None or (self.pages and self.next_num < self.pages): 
                    current_args_dict.update({'_page': self.next_num})
                    url = self.reload_route.get_url(**current_args_dict)
                    pagination.append_inner(Element('a', css_class='icon item', inner_text='<i class="angle right icon"></i>', attrs=[('href', url)]))
                
            if self.pages:
                current_args_dict.update({'_page': self.pages})
                url = self.reload_route.get_url(**current_args_dict)
                pagination.append_inner(Element('a', css_class='item', inner_text='Last', attrs=[('href', url)]))
            
            current_args_dict = self.current_args_dicts.copy()
            if current_args_dict.get('_page'):
                del current_args_dict['_page']
            url = self.reload_route.get_url(**current_args_dict)
            form = Element('form', css_class='item', attrs=[('id', self._ref_form_paginate_id), ('method', 'POST'), ('action', url)],)
            form.append_inner(
                Element('div', 
                    css_class='ui action input', 
                    inner_elements=[
                        Form.create_csrf_field(),
                        Element('', inner_text=f'<input name="{self._ref_form_paginate_text_id}" type="text" placeholder="Page" value="{self.page}" />'),
                        Element('', inner_text=f'<button form="{self._ref_form_paginate_id}" class="ui button" type="submit">Go</button>')
                    ]
                )
            )
            pagination.append_inner(form)
            return pagination.get_html()
        else:
            return Element('div', attrs=[('style', 'padding: 0.8rem;')], inner_text='0 Page').get_html()

    def _get_search_html(self):
        current_args_dict = self.current_args_dicts.copy()
        if current_args_dict.get('_search_text'):
            del current_args_dict['_search_text']
        if current_args_dict.get('_search_option'):
            del current_args_dict['_search_option']
        url = self.reload_route.get_url(**current_args_dict)
        
        textbox = Element('input', attrs=[('type', 'text'), ('placeholder', 'Search...'), ('name', self._ref_form_search_text_id), ('value', self.search_text)])
        select = Element('select', css_class='ui compact selection dropdown', hide_id=False, attrs=[('name', self._ref_form_search_option_id)])
        options = f'<option value="">Select Option</option>'
        for col in self.colitems:
            if col.allow_search and not col.is_hidden:
                col_value = col.name
                col_text = col.name.replace('_', ' ').title()
                if col_value == self.search_option:
                    options += f'<option value="{col_value}" selected>{col_text}</option>'
                else:
                    options += f'<option value="{col_value}">{col_text}</option>'
        select.inner_text = options
        btn = Element('button', css_class='ui button', attrs=[('type', 'submit'), ('form', self._ref_form_search_id)], inner_text='Search')
        form = Element('form', css_class='ui action input', attrs=[('method', 'POST'), ('id', self._ref_form_search_id), ('action', url)])
        csrf_field = Form.create_csrf_field()
        form.append_inner(csrf_field ,textbox, select, btn)
        self.inject_script += f'load_dropdown_field("{select.id}");'
        return form.get_html()

    def _get_table_html(self):
        header_html = self._get_header_html()
        body_html = self._get_body_html()
        
        # css class
        css_class = ''
        if self.css_class:
            css_class = f' class="{self.css_class}"'
            
        return f'<table id="{self.id}"{css_class}>{header_html}{body_html}</table>'

    def get_html(self):
        items = []
        if self.new_route:
            btn = Button('New Record', url=self.new_route.get_url())
            items.append(f'<div class="item">{btn.get_html()}</div>')
        
        if self.allow_search:
            items.append(f'<div class="right item">{self._get_search_html()}</div>')
        
        title_html, table_html, paginate_html, action_html = '', '', '', ''
        
        if len(items) > 0:
            menu = Element('div', css_class='ui stackable secondary menu', attrs=[('style', 'padding-top:5px; padding-bottom:5px;')])
            for item in items:
                menu.append_inner(Element('', inner_text=item))
            action_html = f'<div class="ui fitted attached segment">{menu.get_html()}</div>'

        footer_html = self._get_footer_html()
        if self.allow_paginate and footer_html:
            paginate_html = f'<div class="ui bottom attached vertically fitted segment">{footer_html}</div>' 
        
        if action_html != '' or paginate_html != '':
            title_html = f'<h4 class="ui top attached primary header segment">{self.title}</h4>'
            table_html = f'<div class="ui attached segment" style="overflow-x: auto;">{self._get_table_html()}</div>'
        else:
            title_html = Element('h4', css_class='ui dividing primary header', inner_text=self.title).get_html()
            table_html = f'<div style="overflow-x: auto;">{self._get_table_html()}</div>'
        
        return title_html + action_html + table_html + paginate_html