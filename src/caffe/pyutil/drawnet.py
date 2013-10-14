"""Functions to draw a caffe NetParameter protobuffer.
"""

import pydot

# Internal layer and blob styles.
LAYER_STYLE = {'shape': 'record', 'fillcolor': '#6495ED',
         'style': 'filled,bold'}
NEURON_LAYER_STYLE = {'shape': 'record', 'fillcolor': '#90EE90',
         'style': 'filled,bold'}
BLOB_STYLE = {'shape': 'octagon', 'fillcolor': '#F0E68C',
        'style': 'filled'}

def draw_net(caffe_net, ext='png'):
  """Draws a caffe net and returns the image string encoded using the given
  extension.

  Input:
    caffe_net: a caffe.proto.caffe_pb2.NetParameter protocol buffer.
    ext: the image extension. Default 'png'.
  """
  pydot_graph = pydot.Dot(caffe_net.name, graph_type='digraph')
  pydot_nodes = {}
  pydot_edges = []
  for layer in caffe_net.layers:
    name = layer.layer.name
    layertype = layer.layer.type
    if (len(layer.bottom) == 1 and len(layer.top) == 1 and
        layer.bottom[0] == layer.top[0]):
      # We have an in-place neuron layer.
      pydot_nodes[name + '_' + layertype] = pydot.Node(
          '%s (%s)' % (name, layertype), **NEURON_LAYER_STYLE)
    else:
      pydot_nodes[name + '_' + layertype] = pydot.Node(
          '%s (%s)' % (name, layertype), **LAYER_STYLE)
    for bottom_blob in layer.bottom:
      pydot_nodes[bottom_blob + '_blob'] = pydot.Node(
        '%s' % (bottom_blob), **BLOB_STYLE)
      pydot_edges.append((bottom_blob + '_blob', name + '_' + layertype))
    for top_blob in layer.top:
      pydot_nodes[top_blob + '_blob'] = pydot.Node(
        '%s' % (top_blob))
      pydot_edges.append((name + '_' + layertype, top_blob + '_blob'))
  # Now, add the nodes and edges to the graph.
  for node in pydot_nodes.values():
    pydot_graph.add_node(node)
  for edge in pydot_edges:
    pydot_graph.add_edge(
        pydot.Edge(pydot_nodes[edge[0]], pydot_nodes[edge[1]]))
  return pydot_graph.create(format=ext)

def draw_net_to_file(caffe_net, filename):
  """Draws a caffe net, and saves it to file using the format given as the
  file extension.
  """
  ext = filename[filename.rfind('.')+1:]
  with open(filename, 'w') as fid:
    fid.write(draw_net(caffe_net, ext))

