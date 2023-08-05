import uuid

import ipywidgets as widgets
import traitlets
from ipyvue import VueTemplate
from traitlets import Unicode

from ._version import __version__


# See js/lib/kodexa.js for the frontend counterpart to this file.

@widgets.register
class KodexaNodeWidget(VueTemplate):
    """Kodexa Widget for Rendering Content Nodes"""

    # Name of the widget view class in front-end
    _view_name = Unicode('KodexaView').tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = Unicode('KodexaModel').tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = Unicode('kodexa-widget').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('kodexa-widget').tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = Unicode(__version__).tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode(__version__).tag(sync=True)

    nodes = traitlets.List().tag(sync=True)
    options = traitlets.Dict().tag(sync=True)

    template = traitlets.Unicode('''
        <div>
           <kodexa-content-node 
                :nodes="nodes" :options="options">
            </kodexa-content-node>
        </div>
    ''').tag(sync=True)

    def __init__(self, nodes, options=None):
        widgets.DOMWidget.__init__(self)
        if options is None:
            options = {'showFeatures':True}

        if isinstance(nodes, list):
            new_nodes = []
            for a_node in nodes:
                new_nodes.append(a_node.to_dict())
        else:
            new_nodes = [nodes.to_dict()]

        self.nodes = new_nodes
        self.options = options

        self.css = ".kodexa-vue-base { background: white }; background: white;"


@widgets.register
class KodexaDocumentWidget(VueTemplate):
    """Kodexa Widget for Rendering Documents"""

    # Name of the widget view class in front-end
    _view_name = Unicode('KodexaView').tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = Unicode('KodexaModel').tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = Unicode('kodexa-widget').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('kodexa-widget').tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = Unicode(__version__).tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode(__version__).tag(sync=True)

    document_bytes = traitlets.Bytes().tag(sync=True)
    width = traitlets.Integer(None, allow_none=True).tag(sync=True)
    height = traitlets.Integer(None, allow_none=True).tag(sync=True)
    tags = traitlets.List(None, allow_none=True).tag(sync=True)
    mixin = traitlets.Unicode(None, allow_none=True).tag(sync=True)
    options = traitlets.Dict({}).tag(sync=True)
    ref_id = traitlets.Unicode().tag(sync=True)

    def vue_update_tag(self, tag_update):
        for tag in tag_update:
            for uuid in tag_update[tag]:
                for node in self.document.select('//*[uuid()="' + uuid + '"]'):
                    node.tag(tag)

    template = traitlets.Unicode('''
        <div>
           <kodexa-document 
                :refId="ref_id"
                :data-view="document_bytes" 
                :width="width" 
                :height="height" 
                :tags="tags"
                :options="options"
                @update="(tag_update) => update_tag(tag_update)"
                :mixin=mixin>
            </kodexa-document>
        </div>
    ''').tag(sync=True)

    def __init__(self, document, width=None, height=None, mixin=None, options=None,
                 tags=None):

        widgets.DOMWidget.__init__(self)

        if options is None:
            options = {'menubar': True, 'spatial': {'showPageSelector': True}}
        self.ref_id = 'kdxa' + str(uuid.uuid4()).replace('-', '')
        self.document = document
        self.document_bytes = document.to_msgpack()
        self.width = width
        self.height = height
        self.mixin = mixin
        self.options = options
        self.tags = tags

        self.css = ".kodexa-vue-base { background: white }; background: white;"


@widgets.register
class KodexaStoreWidget(VueTemplate):
    """Kodexa Widget for Rendering Document Stores"""

    # Name of the widget view class in front-end
    _view_name = Unicode('KodexaView').tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = Unicode('KodexaModel').tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = Unicode('kodexa-widget').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('kodexa-widget').tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = Unicode(__version__).tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode(__version__).tag(sync=True)

    document_bytes = traitlets.Bytes(None, allow_none=True).tag(sync=True)
    width = traitlets.Integer(None, allow_none=True).tag(sync=True)
    height = traitlets.Integer(None, allow_none=True).tag(sync=True)
    tags = traitlets.List(None, allow_none=True).tag(sync=True)
    store_documents = traitlets.List(None, allow_none=True).tag(sync=True)
    mixin = traitlets.Unicode(None, allow_none=True).tag(sync=True)
    options = traitlets.Dict({}).tag(sync=True)
    ref_id = traitlets.Unicode().tag(sync=True)

    def vue_update_tag(self, tag_update):
        for tag in tag_update:
            for uuid in tag_update[tag]:
                for node in self.document.select('//*[uuid()="' + uuid + '"]'):
                    node.tag(tag)

    template = traitlets.Unicode('''
        <div>
           {{store_documents}}
        </div>
    ''').tag(sync=True)

    def __init__(self, store, width=None, height=None, mixin=None, options=None,
                 tags=None):

        widgets.DOMWidget.__init__(self)

        if options is None:
            options = {'menubar': True, 'spatial': {'showPageSelector': True}}

        self.ref_id = 'kdxa' + str(uuid.uuid4()).replace('-', '')
        self.store = store
        self.store_documents = store.list()
        self.document_bytes = None #document.to_msgpack()
        self.width = width
        self.height = height
        self.mixin = mixin
        self.options = options
        self.tags = tags

        self.css = ".kodexa-vue-base { background: white }; background: white;"
