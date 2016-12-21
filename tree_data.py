"""Assignment 2: Trees for Treemap
=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto
=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
import os
from random import randint
import math


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.
    This is an abstract class that should not be instantiated directly.
    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.
    === Public Attributes ===
    @type data_size: int
        The total size of all leaves of this tree.
    @type colour: (int, int, int)
        The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.
    === Private Attributes ===
    @type _root: obj | None
        The root value of this tree, or None if this tree is empty.
    @type _subtrees: list[AbstractTree]
        The subtrees of this tree.
    @type _parent_tree: AbstractTree | None
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.
    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).
    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    def __init__(self, root, subtrees, data_size=0):
        """Initialize a new AbstractTree.
        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored,
        and this tree's data_size is computed from the data_sizes of the
        subtrees.
        If <subtrees> is not empty, <data_size> should not be specified.
        This method sets the _parent_tree attribute for each subtree to self.
        A random colour is chosen for this tree.
        Precondition: if <root> is None, then <subtrees> is empty.
        @type self: AbstractTree
        @type root: object
        @type subtrees: list[AbstractTree]
        @type data_size: int
        @rtype: None
        """
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None
        self.data_size = data_size
        first_color_int = randint(0, 255)
        second_color_int = randint(0, 255)
        third_color_int = randint(0, 255)
        self.colour = (first_color_int, second_color_int, third_color_int)
        for i in self._subtrees:
            if i.get_subtrees():
                i._parent_tree = self
                self.data_size += i.data_size
            else:
                i._parent_tree = self
                self.data_size += i.data_size

    def is_empty(self):
        """Return True if this tree is empty.
        @type self: AbstractTree
        @rtype: bool
        """
        return self._root is None

    def generate_treemap(self, rect):
        """Run the treemap algorithm on this tree and return the rectangles.
        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).
        One tuple should be returned per non-empty leaf in this tree.
        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        x, y, width, height = rect
        width += x
        result = []
        if self.is_empty() or self.data_size == 0:
            return []
        elif len(self._subtrees) == 0:
            return [(rect, self.colour)]
        else:
            # is width is greater than height
            if rect[2] > rect[3]:
                for subtree in self._subtrees:
                    if not self._subtrees[-1] == subtree:
                        ratio_prop = (subtree.data_size /
                                      self.data_size) * 100
                        width_rect = int((ratio_prop * rect[2]) // 100)
                        result += subtree.generate_treemap(
                            (x, y, width_rect, rect[3]))
                        x += width_rect
                    else:
                        result += subtree.generate_treemap(
                            (x, y, width - x, rect[3]))
            else:  # if height is greater than the width
                for subtree in self._subtrees:
                    if not self._subtrees[-1] == subtree:
                        ratio_prop = (subtree.data_size /
                                      self.data_size) * 100
                        height_rect = int((ratio_prop * rect[3]) // 100)
                        result += subtree.generate_treemap(
                            (x, y, rect[2], height_rect))
                        y += height_rect
                    else:
                        result += subtree.generate_treemap(
                            (x, y, rect[2], height - y))
            return result

    def get_root(self):
        """Provides acccess to protected member of
        AbstractTree class
        @type self: AbstractTree
        @rtype: str
        """
        return self._root

    def ceiling_(self, node):
        """Returns the ceiling of 1 percent of node's data size
        @type self: AbstractTree
        @type node: AbstractTree
        @rtype: int
        """
        a = math.ceil(node.data_size/100)
        return a

    def get_leaf(self):
        """
        Returns the list of leafs of the tree objects in the tree.
        @type self: AbstractTree
        @rtype: list[AbstractTree]
        """
        lst = []
        if self.is_empty() or self.data_size == 0:
            return []
        else:
            if self._subtrees:
                for i in self._subtrees:
                    if i.data_size != 0:
                        lst += i.get_leaf()
            else:
                lst.append(self)
        return lst

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.
        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.
        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.
        @type self: AbstractTree
        @rtype: str
        """
        raise NotImplementedError

    def __repr__(self):
        """String representation of nodes
        @type self: AbstractTreetype
        @rtype: str
        """
        result = ""
        return result + "Root: " + str(self.get_root()) + " size: "\
            + str(self.data_size)

    def get_parent(self):
        """
        Provides access to protected member parent_tree of AbstractTree

        @type self: AbstractTree
        @rtype: AbstractTree
        """
        return self._parent_tree

    def get_subtrees(self):
        """
        Provides access to protected member subtrees of AbstractTree
        @type self: AbstractTreetype
        @rtype: list
        """
        return self._subtrees

    def remove_node(self, node):
        """
        Removes node from the tree and updates the tree
        @type self: AbstractTree
        @type node: AbstractTree
        @rtype: None
        """
        node.get_parent().get_subtrees().remove(node)
        self.size_change(node)
        node._parent_tree = None

    def size_up(self, node, number):
        """Raises the size of the node by given number and updates the tree
        @type self: AbstractTree
        @type node: AbstractTree
        @type number: int
        @rtype: None
        """
        node.data_size += number
        curr = node
        while curr.get_parent() is not None:
            curr = curr.get_parent()
            curr.data_size += number

    def size_down(self, node, number):
        """Decreases the size of the node by given number and updates the tree
        @type self: AbstractTree
        @type node: AbstractTree
        @type number: int
        @rtype: None
        """
        if node.data_size - number >= 1:
            node.data_size -= number
            curr = node
            while curr.get_parent() is not None:
                curr = curr.get_parent()
                curr.data_size -= number

    def size_change(self, node):
        """Helper for remove_node function. Subtracts the
        size of node from its parent nodes
        @type self: AbstractTree
        @type node: AbstractTree
        @rtype: None
        """
        a = node.data_size
        curr = node
        while curr.get_parent() is not None:
            curr = curr.get_parent()
            curr.data_size -= a

    def cordinate(self, x, y, lst):
        """Gets the node which cursor points
        @type self: AbstractTree
        @type x: int
        @type y: int
        @type lst: list[tuple]
        @rtype: AbstractTree
        """
        a = self.get_leaf()
        if a != []:
            for i in lst:
                if i[0][0] + i[0][2] > x > i[0][0]:
                    if i[0][1] + i[0][3] > y > i[0][1]:
                        return a[lst.index(i)]
            return None
        else:
            return None

    def get_path(self, separator, node):
        """ Returns the path from root to the node
        @type self: FileSystemTree
        @type separator: str
        @type node: FileSystemTree
        @rtype: str
        """
        result_str = ""
        curr = node
        while curr.get_parent() is not None:
            result_str = separator + str(curr.get_root()) + result_str
            curr = curr.get_parent()
        result_str = str(curr.get_root()) + result_str
        return result_str


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.
    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).
    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'
    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """
    def __init__(self, path):
        """Store the file tree structure contained in the given file or folder.
        Precondition: <path> is a valid path for this computer.
        @type self: FileSystemTree
        @type path: str
        @rtype: None
        """
        self._subtrees = []
        self.path = path
        get_name = self.separate(path)  # getname[-1]  is main root
        if os.path.isfile(path):
            AbstractTree.__init__(self, get_name[-1], [], os.path.getsize(path))
        else:
            lst = os.listdir(path)
            for filename in lst:
                subitem = os.path.join(path, filename)
                self._subtrees.append(FileSystemTree(subitem))
            AbstractTree.__init__(self, get_name[-1], self._subtrees, 0)

    def separate(self, path):
        """
        Helper function to split given path into parts.
        @type self: FileSystemTree
        @type path: str
        @rtype: list
        """
        parts = []
        while True:
            newpath, tail = os.path.split(path)
            if newpath == path:
                assert not tail
                if path:
                    parts.append(path)
                break
            parts.append(tail)
            path = newpath
        parts.reverse()
        return parts

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.
        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.
        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.
        @type self: AbstractTree
        @rtype: str
        """
        return "/"

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='pylintrc.txt')
