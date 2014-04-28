
from .exceptions import AISParseError, AISBehaviorError
from .components import component_classes

class Dialog:
    '''An opened AIS dialog.

    :param name: the identifier of this dialog instance.
    :param title: the user-visible dialog title.
    :param code: the identifier of the AIS dialog class (probably).
    :param parent_dialog_name: name of the dialog that opened us.
    :param modal: whether the dialog prevents access to others while opened.
    :param is_main_dialog: whether it's the top level body of the application.
    :param closeable: whether the dialog can be closed.
    :param hide_title_bar: whether AIS would show the title row.
    :param app: the :class:`aisikl.app.Application` this dialog belong to.
    '''

    def __init__(self, name, title, code, parent_dialog_name, modal,
                 is_main_dialog, closeable, hide_title_bar, app):
        self.name = name
        self.title = title
        self.code = code
        self.parent_dialog_name = parent_dialog_name
        self.modal = modal
        self.is_main_dialog = is_main_dialog
        self.closeable = closeable
        self.hide_title_bar = hide_title_bar
        self.app = app

        self.components = {}
        self.changed_components = set()

    def init(self, url):
        '''Load the dialog body.

        Called from :meth:`aisikl.app.Application.open_dialog`.

        :internal:
        '''
        dialog_soup = self.app.ctx.request_html(url)

        body = dialog_soup.body
        if body.get('jsct') != 'body' or body.get('id') != self.name:
            raise AISParseError("Unexpected dialog body response")

        for element in dialog_soup.find_all(jsct=True):
            if element.get('isTemporary') == 'true': continue
            id = element['id']
            jsct = element['jsct']

            if jsct not in component_classes:
                raise AISParseError("Unsupported component type: %r" % jsct)
            component = component_classes[jsct](dialog_soup, element, self)

            self.components[id] = component
            if hasattr(self, id):
                raise Exception(
                    'Component id conflicts with Dialog attribute: %r' % id)
                # If this ever becomes a problem, we can simply skip the
                # setattr. But for now, let's keep component access consistent.
            setattr(self, id, component)

        self.body = self.components[self.name]

    def changed_properties(self):
        '''Return the <changedProperties> string for this dialog.'''
        # We ignore width, height, x, y, focusedComponent and dtSelection.
        # So there are no <nameValue> pairs, only <embObjChProps>.
        if not self.changed_components: return ''
        result = (
            '<changedProperties><objName>' + dialogName + '</objName>\n' +
            '<embObjChProps>\n' +
            ''.join(self.components[id].changed_properties()
                    for id in self.changed_components) +
            '</embObjChProps>\n' +
            '</changedProperties>\n')
        self.changed_properties.clear()
        return result
