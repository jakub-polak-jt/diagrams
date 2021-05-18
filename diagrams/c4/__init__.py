"""
A set of nodes and edges to visualize software architecture using the C4 model.
"""
import html
import textwrap
from diagrams import Cluster, Node, Edge


def _format_node_label(name, key, description):
    """Create a graphviz label string for a C4 node"""
    title = f'<font point-size="12"><b>{html.escape(name)}</b></font><br/>'
    subtitle = f'<font point-size="9">[{html.escape(key)}]<br/></font>' if key else ""
    text = f'<br/><font point-size="10">{_format_description(description)}</font>' if description else ""
    return f"<{title}{subtitle}{text}>"


def _format_description(description):
    """
    Formats the description string so it fits into the C4 nodes.

    It line-breaks the description so it fits onto exactly three lines. If there are more
    than three lines, all further lines are discarded and "..." inserted on the last line to
    indicate that it was shortened. This will also html-escape the description so it can
    safely be included in a HTML label.
    """
    wrapper = textwrap.TextWrapper(width=40, max_lines=3)
    lines = [html.escape(line) for line in wrapper.wrap(description)]
    lines += [""] * (3 - len(lines))  # fill up with empty lines so it is always three
    return "<br/>".join(lines)


def _format_edge_label(description):
    """Create a graphviz label string for a C4 edge"""
    wrapper = textwrap.TextWrapper(width=24, max_lines=3)
    lines = [html.escape(line) for line in wrapper.wrap(description)]
    text = "<br/>".join(lines)
    return f'<<font point-size="10">{text}</font>>'


def Container(name, technology="", description="", **kwargs):
    key = f"Container: {technology}" if technology else "Container"
    node_attributes = {
        "label": _format_node_label(name, key, description),
        "labelloc": "c",
        "shape": "rect",
        "width": "2.6",
        "height": "1.6",
        "fixedsize": "true",
        "style": "filled",
        "fillcolor": "dodgerblue3",
        "fontcolor": "white",
    }
    node_attributes.update(kwargs)
    return Node(**node_attributes)


def Database(name, technology="", description="", **kwargs):
    key = f"Database: {technology}" if technology else "Database"
    node_attributes = {
        "label": _format_node_label(name, key, description),
        "shape": "cylinder",
        "width": "2.6",
        "height": "1.6",
        "fixedsize": "true",
        "style": "filled",
        "fillcolor": "dodgerblue3",
        "fontcolor": "white",
    }
    node_attributes.update(kwargs)
    return Node(**node_attributes)


def System(name, description="", external=False, **kwargs):
    key = "External System" if external else "System"
    node_attributes = {
        "label": _format_node_label(name, key, description),
        "labelloc": "c",
        "shape": "rect",
        "width": "2.6",
        "height": "1.6",
        "fixedsize": "true",
        "style": "filled",
        "fillcolor": "gray60" if external else "dodgerblue4",
        "fontcolor": "white",
    }
    # collapse system boxes to a smaller form if they don't have a description
    if not description:
        node_attributes.update({"width": "2", "height": "1"})
    node_attributes.update(kwargs)
    return Node(**node_attributes)


def Person(name, description="", external=False, **kwargs):
    key = "External Person" if external else "Person"
    node_attributes = {
        "label": _format_node_label(name, key, description),
        "labelloc": "c",
        "shape": "rect",
        "width": "2.6",
        "height": "1.6",
        "fixedsize": "true",
        "style": "rounded,filled",
        "fillcolor": "gray60" if external else "dodgerblue4",
        "fontcolor": "white",
    }
    # collapse person boxes to a smaller form if they don't have a description
    if not description:
        node_attributes.update({"width": "2", "height": "1"})
    node_attributes.update(kwargs)
    return Node(**node_attributes)


def SystemBoundary(name, **kwargs):
    graph_attributes = {
        "label": html.escape(name),
        "bgcolor": "white",
        "margin": "16",
        "style": "dashed",
    }
    graph_attributes.update(kwargs)
    return Cluster(name, graph_attr=graph_attributes)


def Relationship(label="", **kwargs):
    edge_attribtues = {"style": "dashed", "color": "gray60"}
    if label:
        edge_attribtues.update({"label": _format_edge_label(label)})
    edge_attribtues.update(kwargs)
    return Edge(**edge_attribtues)
