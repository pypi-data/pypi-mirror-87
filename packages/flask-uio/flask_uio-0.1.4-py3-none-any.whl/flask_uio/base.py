from flask import url_for, current_app
from .basic import Body, Head, Document
from .element import Element
from .prop import ValidProp
class FomanticHead(Head):
    summernote = ValidProp(bool)
    
    def __init__(self, title, element=None, link=None, script=None, summernote=False):
        super().__init__(title, element, link, script)
        
        static_folder = current_app.config.get('FLASK_UIO_FOMANTIC_STATIC_FOLDER')
        if static_folder is None:
            static_folder = 'flaskuio.static'
            
        filename = current_app.config.get('FLASK_UIO_FOMANTIC_CSS_FILENAME')
        if filename is None:
            filename = 'style/semantic.min.css'
        self.summernote = summernote
        self.element.append(Element('meta', attrs=[('charset', 'UTF-8')]))
        self.element.append(Element('meta', attrs=[('name', 'viewport'), ('content', 'width=device-width, initial-scale=1.0')]))
        self.append_link(url_for(static_folder, filename=filename))
        if self.summernote:
            self.append_link(url_for('flaskuio.static', filename='vendor/summernote-0.8.18-dist/summernote-lite.min.css'))
        self.append_link(url_for('flaskuio.static', filename='style/main.css'))

class FomanticBody(Body):
    summernote = ValidProp(bool)
    
    def __init__(self, element=None, script=None, summernote=False):
        super().__init__(element, script)
        
        static_folder = current_app.config.get('FLASK_UIO_FOMANTIC_STATIC_FOLDER')
        if static_folder is None:
            static_folder = 'flaskuio.static'
            
        filename = current_app.config.get('FLASK_UIO_FOMANTIC_JS_FILENAME')
        if filename is None:
            filename = 'script/semantic.min.js'
        self.summernote = summernote
        self.append_script(url_for('flaskuio.static', filename='script/jquery-3.5.1.min.js'))
        self.append_script(url_for('flaskuio.static', filename='script/jquery-dateformat.js'))
        self.append_script(url_for(static_folder, filename=filename))
        self.append_script(url_for('flaskuio.static', filename='script/custom-semantic.js'))
        if self.summernote:
            self.append_script(url_for('flaskuio.static', filename='vendor/summernote-0.8.18-dist/summernote-lite.min.js'))
            self.append_script(url_for('flaskuio.static', filename='script/summernote.js'))
        
class Document(Document):
    head = None
    body = None
    def __init__(self, title, summernote=False):
        css = current_app.config.get('FLASK_UIO_CSS_FRAMEWORK') or 'fomanticui'
        if css == 'fomanticui':
            self.head = FomanticHead(title, summernote=summernote)
            self.body = FomanticBody(summernote=summernote)
        