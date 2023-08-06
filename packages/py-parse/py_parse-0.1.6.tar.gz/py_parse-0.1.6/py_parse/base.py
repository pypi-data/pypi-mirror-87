from typing import List
from html.parser import HTMLParser

from .node import Node, Nodes
from .exceptions import WrongHTMLFormatError


def parse(html: str, show_unclosed_tags: bool = False, strict_parsing: bool = True,
          auto_close: List[str] = None) -> Nodes:
    """
    Main functions to parse html source. Gets Nodes object back to use it with queries
    :param html: string html-content
    :param show_unclosed_tags: flag to show all unclosed tags on parsing error. If strict_parsing is False, then will
    be ignored
    :param strict_parsing: flag to check markup (closing tag must be for same opened tag etc.) if False then nothing
    checks and all relative-style query will return None or Error
    :param auto_close: list of tags for auto-closing when parse, can be used to fix markup issues
    :return: Nodes object
    :raises WrongHTMLFormatError if wrong format and strict_parsing is True
    """
    parser = MyHTMLParser(auto_close) if strict_parsing else RelaxedHTMLParser()
    parser.feed(html)
    if strict_parsing and parser.opened_tags_count != parser.closed_tags_count:
        message = ''
        if show_unclosed_tags:
            message = "\nUNCLOSED TAGS:\n" + "\n".join(
                e.__repr__() for e in parser.all_nodes._flatten() if not e.closed)
        raise WrongHTMLFormatError(f'Count of the open tags({parser.opened_tags_count}) is not match with count of '
                                   f'closed tags({parser.closed_tags_count})!{message}')
    return parser.all_nodes


class MyHTMLParser(HTMLParser):
    VOID = ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
            'meta', 'param', 'source', 'track', 'wbr')

    def __init__(self, auto_close: List = None):
        super().__init__()
        if auto_close:
            MyHTMLParser.VOID += tuple(auto_close)
        self.actual_node = None
        self.all_nodes = Nodes()
        self.opened_tags_count = 0
        self.closed_tags_count = 0

    def handle_starttag(self, tag, attrs):
        self.opened_tags_count += 1
        attrs = None if not attrs else attrs
        if self.actual_node is None:
            self.actual_node = Node(tag=tag, attrs=attrs)
            self.all_nodes.append(self.actual_node)
        else:
            node = Node(tag, attrs=attrs)
            node._parent = self.actual_node
            if self.actual_node.children:
                self.actual_node.children[-1]._next_node = node
                node._prev_node = self.actual_node.children[-1]
            self.actual_node.children.append(node)
            self.actual_node = node
        if tag in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        self.closed_tags_count += 1
        if self.actual_node is None:
            raise WrongHTMLFormatError(f'Closed tag ({tag}) without opening!')
        self.actual_node.closed = True
        if self.actual_node._parent is not None:
            self.actual_node = self.actual_node._parent
        else:
            self.actual_node = None

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self.actual_node is not None:
            self.actual_node._set_text(data)

    def handle_comment(self, data):
        Node.comments.append(data)

    def handle_entityref(self, name):
        pass
        # c = chr(name2codepoint[name])
        # print("Named ent:", c)

    def handle_charref(self, name):
        pass
        # if name.startswith('x'):
        #     c = chr(int(name[1:], 16))
        # else:
        #     c = chr(int(name))
        # print("Num ent  :", c)

    def handle_decl(self, data):
        pass
        # print("Decl     :", data)

    def error(self, message):
        raise WrongHTMLFormatError('Parser error!\n' + message)


class RelaxedHTMLParser(HTMLParser):
    """
    Parser realisation which ignores markup failures, just collects all html-elements
    WARNING! You cant use any relative-type queries with current parser! All next, previous, children, parent for all
    nodes is None
    """

    def __init__(self):
        super().__init__()
        self.actual_node = None
        self.all_nodes = Nodes()
        self.opened_tags_count = 0
        self.closed_tags_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = None if not attrs else attrs
        self.actual_node = Node(tag=tag, attrs=attrs)
        self.all_nodes.append(self.actual_node)

    def handle_endtag(self, tag):
        pass

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if self.actual_node is not None:
            self.actual_node._set_text(data)

    def handle_comment(self, data):
        Node.comments.append(data)

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

    def handle_decl(self, data):
        pass

    def error(self, message):
        pass
