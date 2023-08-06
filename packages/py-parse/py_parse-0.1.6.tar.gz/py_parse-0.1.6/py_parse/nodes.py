from typing import List, Callable, Any

from .helpers import get_filter_body
from .exceptions import NoSuchElementError


class Nodes:
    """
    Representation of container for html-elements. Used only with Node objects.
    """

    def __init__(self, *args):
        self.container: List = []
        self.container.extend(args)

    def append(self, node):
        self.container.append(node)

    def is_empty(self):
        return len(self.container) == 0

    def extend(self, iterable):
        self.container.extend(iterable)

    def __getitem__(self, item):
        return self.container[item]

    def __contains__(self, item):
        return item in self.container

    def __bool__(self):
        return len(self.container) > 0

    def __repr__(self):
        return f'Nodes<length={len(self.container)}>'

    def __len__(self):
        return len(self.container)

    def __iter__(self):
        return iter(self.container)

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Nodes):
            return False
        return self.container == other.container

    def first(self):
        if self.is_empty():
            raise NoSuchElementError('Cant find element with current filter')
        return self.container[0]

    def last(self):
        if self.is_empty():
            raise NoSuchElementError('Cant find element with current filter')
        return self.container[-1]

    def _flatten(self, filter_: Callable[[Any], bool] = None):
        """
        Method to get each element and all it descendants in this container.
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Nodes object
        """
        result = Nodes()
        for node in self.container:
            result.extend(node._flatten(filter_))
        return result

    def html(self, spaces: int = 0):
        sp = '\n' if not spaces else f'\n' + (" " * spaces)
        result = ''
        for child in self.container:
            result += f'{sp}' + child.html(spaces)
        if sp == '\n':
            result = result.replace('\n', '', 1)
        return result

    def find_all(self, filter_: Callable[[Any], bool] = None):
        """
        Returns Nodes - all objects in current container for those filter_ callable returns True. If no filter
        specified then all objects will be return
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Nodes object
        """
        return self._flatten(filter_)

    def find(self, filter_: Callable[[Any], bool]):
        """
        Returns Node - first element of all objects in current container for those filter_ callable returns True.
        If no filter specified then first Node object from this container will be return
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Node object
        """
        result = self._flatten(filter_)
        if result.is_empty():
            raise NoSuchElementError(f'No elements with current filter ({get_filter_body(filter_)})')
        return result[0]

    def find_tag(self, tag: str, filter_: Callable[[Any], bool] = None):
        """
        Returns Node - first element of all objects with current tag and for those filter_ callable returns True.
        If no filter specified then first Node object  with current tag will be return
        :param tag: name of the element's tag to look for
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Node object
        """
        result = self.find_tags(tag, filter_)
        if result.is_empty():
            filter_body = get_filter_body(filter_)
            if filter_body:
                filter_body = f' and {filter_body}'
            raise NoSuchElementError(f"No elements with current filter (tag == '{tag}'{filter_body})")
        return result[0]

    def find_tags(self, tag: str, filter_: Callable[[Any], bool] = None):
        """
        Returns Nodes - all objects with current tag and for those filter_ callable returns True. If no filter
        specified then all objects with current tag will be return
        :param tag: name of the element's tag to look for
        :param filter_ lambda function or callable predicate to check each element, must returns True/False and take
        exactly one arg - node object
        :return Nodes object
        """
        result = self._flatten(lambda e: e.tag == tag)
        if filter_:
            result = result._flatten(filter_)
        return result
