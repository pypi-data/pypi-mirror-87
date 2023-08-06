from typing import List, Tuple, Callable, Any
import sys

from .nodes import Nodes
from .helpers import get_filter_body
from .exceptions import NoRelativeError


class Node:
    """
    Representation of one html element, node in DOM
    """
    comments: List[str] = []

    def __init__(self, tag: str, parent=None, prev_node=None, next_node=None, attrs: List[Tuple] = None,
                 text: str = None, children=None):
        """
        Init for creating analog of html DOM element. All pairs from attrs list will become object attributes, so
        if attrs= [('id','1')] then node.id = '1'
        :param tag: required field, tag of the html element
        :param parent: link to Node object - parent of the current element in DOM
        :param prev_node: link to Node object - previous sibling of the current element in DOM
        :param next_node: link to Node object - next sibling of the current element in DOM
        :param attrs: list of tuples - pairs of the element attributes in html, all of them became object's attributes
        :param text: text of the element
        :param children: Nodes object, containing all children (inner elements) of current element
        """
        self.tag = tag
        self._parent = parent
        self._prev_node = prev_node
        self._next_node = next_node
        self._attrs = attrs
        self.text = ''
        if attrs:
            for pair in attrs:
                key = pair[0] if pair[0] != 'class' else 'class_'
                setattr(self, key, pair[1])
        self._set_text(text)
        self.children = Nodes() if children is None else children
        # is closed tag for this Node was found
        self.closed = False

    def __contains__(self, item):
        """
        For using "'attr' in node" syntax  with filter
        """
        return item in self.__dict__

    def __getattr__(self, item):
        if item not in self.__dict__:
            frame = sys._getframe(0)
            while frame.f_back is not None:
                frame = frame.f_back
                if frame.f_code.co_filename.endswith('node.py') and frame.f_code.co_name == '_flatten':
                    del frame
                    return Node('')
            del frame
            raise AttributeError(f"'Node' object has no attribute '{item}'")
        return self.__dict__[item]

    def _set_text(self, text):
        if text is None or len(text.rstrip()) == 0:
            return
        else:
            self.text = text if not self.text else self.text + '\n' + text

    def cleared_text(self) -> str:
        """
        Return text of the element without leading/following spaces, tabs (\t), new line characters(\n).
        :return: text after replacing
        """
        if not self.text:
            return ''
        return self.text.replace('\n', '').replace('\t', '').strip()

    def __repr__(self):
        text = '' if not self.text else f' text={self.text},'
        return f'Node<tag={self.tag}, previous={self._prev_node}, next={self._next_node}, attributes={self._attrs},' \
               f'{text} children={self.children}, parent={self._parent}>'

    def __str__(self):
        attributes = '' if not self._attrs else ' ' + ' '.join([f'{e[0]}="{e[1]}"' for e in self._attrs])
        data = '' if not self.text else self.text
        return f'<{self.tag}{attributes}>{data}</{self.tag}>'

    def html(self, spaces: int = 0):
        start = self.__repr__()
        sp = spaces + 4
        if self.children:
            start = start + f'{self.children.html(sp)}'
        return start

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Node):
            return False
        return self.tag == other.tag and self.text == other.text and self._attrs == other._attrs

    def _flatten(self, filter_: Callable[[Any], bool] = None):
        """
        Method to get this element and all descendants in Nodes object.
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Nodes object
        """
        result = Nodes()
        if (filter_ and filter_(self)) or filter_ is None:
            result.append(self)
        if not self.children.is_empty():
            result.extend(self.children._flatten(filter_))
        return result

    def has_parent(self) -> bool:
        return self._parent is not None

    @property
    def parent(self):
        """
        Returns parent (Node object) of current object
        :return Node object
        :raises NoRelativeError if no parent presents
        """
        if self._parent is None:
            raise NoRelativeError(f'Element {self} has no parent')
        return self._parent

    def has_child(self) -> bool:
        return not self.children.is_empty()

    def child(self, filter_: Callable[[Any], bool] = None):
        """
        Returns one of the children (inner elements) of the current element. If no  filter_ specified then
        returns first child.
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - Node object
        :return Node object
        :raises NoRelativeError if no children at all, or with that filter
        """
        if not self.children:
            raise NoRelativeError(f'Element {self} has no children')
        for child in self.children:
            if filter_ is None or filter_(child):
                return child
        raise NoRelativeError(f'Element {self} has no children with current filter {_body(filter_)}')

    def descendant(self, filter_: Callable[[Any], bool] = None):
        """
        Returns first of the descendants (inner elements and their inners) of the current element.
        If no  filter_ specified then returns first child.
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Node object
        :raises NoRelativeError if no descendants at all, or with that filter
        """
        nodes = self.descendants(filter_)
        if nodes.is_empty():
            raise NoRelativeError(f'Element {self} has no descendants with current filter {_body(filter_)}')
        return nodes[0]

    def descendants(self, filter_: Callable[[Any], bool] = None):
        """
        Returns all descendants (inner elements and their inners) of the current element.
        If no  filter_ specified then returns first child.
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Nodes object
        :raises NoRelativeError if no descendants at all, or with that filter
        """
        if not self.children:
            raise NoRelativeError(f'Element {self} has no children')
        if filter_ is None:
            return Nodes(self.child())
        nodes = self.children._flatten(filter_)
        return nodes

    def has_next_node(self):
        return self._next_node is not None

    def has_prev_node(self):
        return self._prev_node is not None

    def next_sibling(self, filter_: Callable[[Any], bool] = None):
        """
        Returns next (following in DOM) element.
        If no  filter_ specified then returns current next node.
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Node object
        :raises NoRelativeError if no following siblings at all, or with that filter
        """
        if self._next_node is None:
            raise NoRelativeError(f'Element {self} has no following siblings')
        if filter_ is None:
            return self._next_node
        current = self
        while current._next_node is not None:
            if filter_(current._next_node):
                return current._next_node
            current = current._next_node
        raise NoRelativeError(f'Element {self} has no following siblings with current filter {_body(filter_)}')

    def prev_sibling(self, filter_: Callable[[Any], bool] = None):
        """
        Returns previous (preceding in DOM) element.
        If no  filter_ specified then returns current next node.
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Node object
        :raises NoRelativeError if no preceding siblings at all, or with that filter
        """
        if self._prev_node is None:
            raise NoRelativeError(f'Element {self} has no preceding siblings')
        if filter_ is None:
            return self._prev_node
        current = self
        while current._prev_node is not None:
            if filter_(current._prev_node):
                return current._prev_node
            current = current._prev_node
        raise NoRelativeError(f'Element {self} has no preceding siblings with current filter {_body(filter_)}')

    def ancestor(self, filter_: Callable[[Any], bool] = None):
        """
        Returns ancestor (parent in hierarchy) of the current element.
        If no  filter_ specified then returns current parent.
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Node object
        :raises NoRelativeError if no descendants at all, or with that filter
        """
        if self._parent is None:
            raise NoRelativeError(f'Element {self} has no parent')
        if filter_ is None:
            return self._parent
        current = self
        while current._parent is not None:
            if filter_(current._parent):
                return current._parent
            current = current._parent
        raise NoRelativeError(f'Element {self} has no ancestor with current filter {_body(filter_)}')

    def inner_text(self) -> List[str]:
        """
        Returns list of element text and text of all element descendants
        :return: list of strings
        """
        return [n.text for n in self._flatten() if n.text]


def _body(filter_):
    body = get_filter_body(filter_)
    return f'({body})' if body else ''
