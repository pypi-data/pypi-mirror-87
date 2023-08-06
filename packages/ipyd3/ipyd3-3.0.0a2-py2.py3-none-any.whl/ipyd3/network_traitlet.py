from traitlets import TraitType as _TraitType, Any
import copy

class Graph(Any):
    """
        A trait for a graph dictionary
    """

    default_value = {"nodes":[], "links":[]}
    info_text = 'an networkx.classes.graph.Graph object or dict in format of { nodes:[...], links:[...] }'

    def validate(self, obj, value):
        if "'networkx.classes" in str(type(value)):
            nodes = dict(value.nodes.data())
            format_nodes = []
            for k,v in dict(nodes).items():
                temp = v.copy()
                temp["id"]=k
                temp["layer"]="default"
                format_nodes.append(temp)

            edges = list(value.edges.data())

            format_edges = []
            for e1,e2,v in edges:
                temp = v.copy()
                temp["source"] = e1
                temp["target"] = e2
                temp["edge"] = str(e1) +"-"+str(e2)
                temp["layer"]="default - default"
                format_edges.append(temp)

            graph = {
                "nodes":format_nodes,
                "links":format_edges
            }
            return graph

        # Checking for dictionary containing nodes and edges as keys.
        if type(value) == dict and "nodes" in value.keys() and "links" in value.keys():

            return copy.deepcopy(value)

        self.error(obj, value)
