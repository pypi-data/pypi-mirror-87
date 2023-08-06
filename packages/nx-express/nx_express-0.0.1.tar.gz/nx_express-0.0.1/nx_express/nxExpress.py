# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class nxExpress(Component):
    """A nxExpress component.
nxExpress is the Component.
It renders a graph based on the data given.
On click, it gives the data correspondent to the node.
Built with Data Driven Documents.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- data (dict; required): The cytoscape data for rendering the graph.
- edge_props (dict; default {
  e_width: null,
  e_color: null,
}): Aesthetics properties for the edges.
- node_props (dict; default {
  n_radius: null,
  n_size_range: [1, 9],
  n_color: null,
}): Aesthetics properties for the nodes.
- node_label (dict; default {
  fontSize: 12,
  fontFamily: "Arial",
  fontWeight: "none",
}): Aesthetics properties for the labels.
- dims (dict; default {width: 758, height: 458})
- tapNode (dict; optional): Node clicked."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.REQUIRED, edge_props=Component.UNDEFINED, node_props=Component.UNDEFINED, node_label=Component.UNDEFINED, dims=Component.UNDEFINED, tapNode=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'edge_props', 'node_props', 'node_label', 'dims', 'tapNode']
        self._type = 'nxExpress'
        self._namespace = 'nx_express'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'edge_props', 'node_props', 'node_label', 'dims', 'tapNode']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(nxExpress, self).__init__(**args)
