from __future__ import annotations

import time

from typing import Optional, Any
from huffman import HuffmanTree
from utils import *


class EmptyStackError(Exception):
    """ An exception for the below OrderedStack classes. """

    def __str__(self) -> str:
        """Return a string representation of this error."""
        return 'You called pop on an empty stack.'


class _OrderedStack:
    """ An ordered list implementation of the stack ADT that stores
    items in a certain order. NOTE: This is an abstract class and should not
    be instantiated.
    """
    # Private Attributes:
    # _items: The list containing the contents of this OrderedStack

    _items: list
    _size: int

    def __init__(self) -> None:
        """ Initialize a new empty OrderedStack. """
        self._items = []
        self._size = 0

    def is_empty(self) -> bool:
        """ Returns whether this stack contains no items. """
        return self._size == 0

    def one_more(self) -> bool:
        """ Returns True if there is one more item left on the stack. """
        return self._size == 1

    def push(self, item: Any) -> None:
        """ Push <item> onto the top of the stack, following LIFO order. """
        self._items.append(item)
        self._size += 1

    def pop(self) -> Any:
        """ Pop the topmost item on the stack. Raises EmptyStackError if the
        stack is empty. """
        if self._size != 0:
            self._size -= 1
            return self._items.pop()
        else:
            raise EmptyStackError

    def ordered_insert(self, item: Any) -> None:
        """ Add <item> to this OrderedStack while maintaining its order. """
        raise NotImplementedError

    def __str__(self) -> str:
        """ Return a string representation of this OrderedStack. """
        return str(self._items)

    def __repr__(self) -> str:
        """ Return a representation of this OrderedStack for use in the console.
        """
        return str(self)


class _OrderedStackHuffmanTree(_OrderedStack):
    """ An ordered list implementation of the stack ADT that stores
    HuffmanTrees. HuffmanTrees with the least frequency (as defined by their
    numbers) are stored at the top of the stack.
    """
    # Private Attributes:
    # _items: The list containing the contents of this OrderedStack

    _items: list[HuffmanTree]
    _size: int

    def push(self, item: HuffmanTree) -> None:
        """ Push <item> onto the top of the stack, following LIFO order. """
        _OrderedStack.push(self, item)

    def pop(self) -> HuffmanTree:
        """ Pop the topmost item on the stack. Raises EmptyStackError if the
        stack is empty"""
        return _OrderedStack.pop(self)

    def ordered_insert(self, item: HuffmanTree) -> None:
        """ Add <item> to the stack while maintaining its order.
        >>> s = _OrderedStackHuffmanTree()
        >>> t1 = HuffmanTree()
        >>> t1.number = 10
        >>> t2 = HuffmanTree()
        >>> t2.number = 7
        >>> t3 = HuffmanTree()
        >>> t3.number = 11
        >>> t4 = HuffmanTree()
        >>> t4.number = 7
        >>> t5 = HuffmanTree()
        >>> t5.number = 0
        >>> s.ordered_insert(t1)
        >>> s.ordered_insert(t2)
        >>> s.ordered_insert(t3)
        >>> s.ordered_insert(t4)
        >>> s.ordered_insert(t5)
        >>> s._items == [t5, t2, t4, t1, t3]
        True
        """
        if self.is_empty():
            self.push(item)  # simply push the item to the stack if it is empty
            return
        # if the stack is not empty, the item needs to be inserted in order.
        # this is done by transferring all trees with number less than or equal
        # to the number of <item> to a separate stack, then pushing the <item>
        # onto self, and then transferring all the items on the separate stack
        # back onto self.
        side_stack = _OrderedStackHuffmanTree()
        while not self.is_empty():
            curr = self.pop()
            if curr.number <= item.number:
                side_stack.push(curr)
            else:
                self.push(curr)
                break
        self.push(item)
        while not side_stack.is_empty():
            self.push(side_stack.pop())


class _OrderedStackString(_OrderedStack):
    """ An ordered list implementation of the stack ADT that stores str objects.
    Strings with the least length are stored at the top of the stack.
    """
    # Private Attributes:
    # _items: The list containing the contents of this OrderedStack

    _items: list[str]
    _size: int

    def push(self, item: str) -> None:
        """ Push <item> onto the top of the stack, following LIFO order. """
        _OrderedStack.push(self, item)

    def pop(self) -> str:
        """ Pop the topmost item on the stack. Raises EmptyStackError if the
        stack is empty"""
        return _OrderedStack.pop(self)

    def ordered_insert(self, item: str) -> None:
        """ Add <item> to the stack while maintaining its order.
        >>> s = _OrderedStackString()
        >>> str1 =  '001'
        >>> str2 = '0'
        >>> str3 = '1'
        >>> str4 = '1234'
        >>> s.ordered_insert(str1)
        >>> s.ordered_insert(str2)
        >>> s.ordered_insert(str3)
        >>> s.ordered_insert(str4)
        >>> s._items == [str4, str1, str3, str2]
        True
        """
        if self.is_empty():
            self.push(item)  # simply push the item to the stack if it is empty
            return
        # if the stack is not empty, the item needs to be inserted in order.
        # this is done by transferring all elements with length less than or
        # equal to the number of <item> to a separate stack, then pushing the
        # <item> onto self, and then transferring all the items on the separate
        # stack back onto self.
        side_stack = _OrderedStackString()
        while not self.is_empty():
            curr = self.pop()
            if len(curr) <= len(item):
                side_stack.push(curr)
            else:
                self.push(curr)
                break
        self.push(item)
        while not side_stack.is_empty():
            self.push(side_stack.pop())


class _OrderedStackFrequency:
    """ An ordered list implementation of the stack ADT that stores int objects.
    Items with the greatest frequency are stored at the top of the stack.
    """
    # Private Attributes:
    # _items: The list containing the contents of this OrderedStack

    _items: list[Optional[int]]
    _size: int

    def __init__(self) -> None:
        """ Initialize a new empty OrderedStack. """
        self._items = []
        self._size = 0

    def is_empty(self) -> bool:
        """ Returns whether this stack contains no items. """
        return self._size == 0

    def one_more(self) -> bool:
        """ Returns True if there is one more item left on the stack. """
        return self._size == 1

    def push(self, item: int) -> None:
        """ Push <item> onto the top of the stack, following LIFO order. """
        self._items.append(item)
        self._size += 1

    def pop(self) -> int:
        """ Pop the topmost item on the stack. Raises EmptyStackError if the
        stack is empty"""
        if self._size != 0:
            self._size -= 1
            return self._items.pop()
        else:
            raise EmptyStackError

    def ordered_insert(self, item: int, freq_dict: dict[int, int]) -> None:
        """ Add item to the stack while maintaining its order.
        >>> s = _OrderedStackFrequency()
        >>> freq_dict = {1: 100, 2: 200, 3: 0, 4: 123, 5: 200}
        >>> s.ordered_insert(1, freq_dict)
        >>> s.ordered_insert(2, freq_dict)
        >>> s.ordered_insert(3, freq_dict)
        >>> s.ordered_insert(4, freq_dict)
        >>> s.ordered_insert(5, freq_dict)
        >>> s._items == [3, 1, 4, 5, 2]
        True
        """
        if self.is_empty():
            self.push(item)  # simply push the item to the stack if it is empty
            return
        # if the stack is not empty, the item needs to be inserted in order.
        # this is done by transferring all elements greater than or equal
        # <item> to a separate stack, then pushing <item> onto self, and then
        # transferring all the items on the separate stack back onto self.
        side_stack = _OrderedStackFrequency()
        while not self.is_empty():
            curr = self.pop()
            if freq_dict[curr] >= freq_dict[item]:
                side_stack.push(curr)
            else:
                self.push(curr)
                break
        self.push(item)
        while not side_stack.is_empty():
            self.push(side_stack.pop())

    def __str__(self) -> str:
        """ Return a string representation of this OrderedStack. """
        return str(self._items)

    def __repr__(self) -> str:
        """ Return a representation of this OrderedStack for use in the console.
        """
        return str(self)


class _Counter:
    """ An object that keeps track of a count.
    === Public Attributes ===
    count: the value of this Counter
    """
    count: int

    def __init__(self) -> None:
        """ Initialize this counter. Starts with initial value 0. """
        self.count = 0

    def __repr__(self) -> str:
        """ Return a representation of this Counter for use in the console."""
        return str(self.count)

# ====================
# Functions for compression


def build_frequency_dict(text: bytes) -> dict[int, int]:
    """ Return a dictionary which maps each of the bytes in <text> to its
    frequency.

    >>> d = build_frequency_dict(bytes([65, 66, 67, 66]))
    >>> d == {65: 1, 66: 2, 67: 1}
    True
    >>> build_frequency_dict(bytes([1]))
    {1: 1, 0: 0}
    >>> build_frequency_dict(bytes([]))
    {}
    """
    ans = {}
    for byte in text:
        if byte in ans:
            ans[byte] += 1
        else:
            ans[byte] = 1
    if len(ans) == 1:
        dummy = 0 if list(ans.keys())[0] != 0 else 1
        ans[dummy] = 0
    return ans


def build_huffman_tree(freq_dict: dict[int, int]) -> HuffmanTree:
    """ Return the Huffman tree corresponding to the frequency dictionary
    <freq_dict>.

    Precondition: freq_dict is not empty.

    >>> freq = {2: 6, 3: 4}
    >>> t = build_huffman_tree(freq)
    >>> result = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> t == result
    True
    >>> freq = {2: 6, 3: 4, 7: 5}
    >>> t = build_huffman_tree(freq)
    >>> result = HuffmanTree(None, HuffmanTree(2), \
                             HuffmanTree(None, HuffmanTree(3), HuffmanTree(7)))
    >>> t == result
    True
    >>> import random
    >>> symbol = random.randint(0,255)
    >>> freq = {symbol: 6}
    >>> t = build_huffman_tree(freq)
    >>> any_valid_byte_other_than_symbol = (symbol + 1) % 256
    >>> dummy_tree = HuffmanTree(any_valid_byte_other_than_symbol)
    >>> result = HuffmanTree(None, HuffmanTree(symbol), dummy_tree)
    >>> t.left == result.left or t.right == result.left
    True
    >>> build_huffman_tree({})
    HuffmanTree(None, None, None)
    """
    if len(freq_dict) == 0:
        return HuffmanTree()
    # if the length of freq_dict is 1, then we need to add a "dummy byte" to a
    # copy of it (so that we don't mutate it)
    elif len(freq_dict) == 1:
        copy = {}
        for byte in freq_dict:
            copy.setdefault(byte, freq_dict[byte])
            dummy = 0 if byte != 0 else 1
            copy[dummy] = 0
    else:
        copy = freq_dict

    # Now, take every element in the copy dictionary and push it (in order!)
    # into an OrderedStack. The items at the top of the stack will have the
    # least frequency, and the items at the bottom will have greater frequency.
    stack = _OrderedStackHuffmanTree()
    for byte in copy:
        node = HuffmanTree(byte)
        node.number = copy[byte]
        stack.ordered_insert(node)
    # In this step, two elements are popped off the stack simultaneously, and
    # are joined using a helper function, and then the resultant tree is pushed
    # (in order!) back onto the stack, until one tree remains on the stack.
    while not stack.one_more():
        stack.ordered_insert(_join_trees(stack.pop(), stack.pop()))
    # Finally, pop the remaining tree of the stack and clear the temporary
    # number attributes added to each of its nodes using a helper function.
    final = stack.pop()
    _clear_numbers(final)
    return final


def _join_trees(t1: HuffmanTree, t2: HuffmanTree) -> HuffmanTree:
    """ Returns a HuffmanTree with children t1 and t2. """
    joined = HuffmanTree(None, t1, t2)
    joined.number = t1.number + t2.number
    return joined


def _clear_numbers(t: HuffmanTree) -> None:
    """ Mutates <t> such that all nodes in it have number attribute None.
    >>> tree = HuffmanTree()
    >>> tree.number = 1
    >>> _clear_numbers(tree)
    >>> tree.number is None
    True
    >>> tree.number = 1
    >>> left = HuffmanTree(2)
    >>> left.number = 2
    >>> right = HuffmanTree(3)
    >>> right.number = 3
    >>> tree.left = left
    >>> tree.right = right
    >>> _clear_numbers(tree)
    """
    if t.is_leaf():
        t.number = None
        return
    else:
        t.number = None
        _clear_numbers(t.right)
        _clear_numbers(t.left)


def get_codes(tree: HuffmanTree) -> dict[int, str]:
    """ Return a dictionary which maps symbols from the Huffman tree <tree>
    to codes.

    >>> tree = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> d = get_codes(tree)
    >>> d == {3: "0", 2: "1"}
    True
    >>> get_codes(HuffmanTree())
    {}
    """
    return _get_codes_helper(tree)


def _get_codes_helper(tree: HuffmanTree, code: str = '') -> dict[int, str]:
    """ Recursive helper function for get_codes. """
    if tree.is_leaf():
        d = {}
        # if the tree is a leaf, and its symbol is None, then this is an empty
        # tree, and so we return an empty dictionary.
        if tree.symbol is None:
            return d
        # otherwise, we have reached a true base case where we are at a leaf
        # with a symbol, and so we assign the <code> parameter to tree.symbol in
        # d.
        d[tree.symbol] = code
        return d
    else:
        d = {}
        # we recurse on the left subtree if it exists, and pass in the <code>
        # parameter, plus a '0', since we are going left. The case where we
        # recurse for self.right is analagous.
        if tree.left is not None:
            left_codes = _get_codes_helper(tree.left, code + '0')
            for key in left_codes:
                d.setdefault(key, left_codes[key])
        if tree.right is not None:
            right_codes = _get_codes_helper(tree.right, code + '1')
            for key in right_codes:
                d.setdefault(key, right_codes[key])
        return d


def number_nodes(tree: HuffmanTree) -> None:
    """ Number internal nodes in <tree> according to postorder traversal. The
    numbering starts at 0.

    >>> left = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> right = HuffmanTree(None, HuffmanTree(9), HuffmanTree(10))
    >>> tree = HuffmanTree(None, left, right)
    >>> number_nodes(tree)
    >>> tree.left.number
    0
    >>> tree.right.number
    1
    >>> tree.number
    2
    """
    _number_nodes_helper(tree, _Counter())


def _number_nodes_helper(tree: HuffmanTree, counter: _Counter) -> None:
    """ Recursive helper function for number_nodes. """
    # we don't number leaves, unless the entire tree is empty
    if tree.is_leaf():
        if tree.symbol is None:
            tree.number = 0
        return
    else:
        # we recurse into the left and right trees, passing in (the mutable)
        # <counter> parameter to keep track of which number we are currently at
        # in the numbering stage.
        if tree.left is not None:
            _number_nodes_helper(tree.left, counter)
        if tree.right is not None:
            _number_nodes_helper(tree.right, counter)
        # finally, after the numbering for the left and right subtrees is
        # completed, number the root of this tree with the current count stored
        # in <counter>, and increment counter.
        tree.number = counter.count
        counter.count += 1


def avg_length(tree: HuffmanTree, freq_dict: dict[int, int]) -> float:
    """ Return the average number of bits required per symbol, to compress the
    text made of the symbols and frequencies in <freq_dict>, using the Huffman
    tree <tree>.

    The average number of bits = the weighted sum of the length of each symbol
    (where the weights are given by the symbol's frequencies), divided by the
    total of all symbol frequencies.

    >>> freq = {3: 2, 2: 7, 9: 1}
    >>> left = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> right = HuffmanTree(9)
    >>> tree = HuffmanTree(None, left, right)
    >>> avg_length(tree, freq)  # (2*2 + 7*2 + 1*1) / (2 + 7 + 1)
    1.9
    >>> avg_length(HuffmanTree(), {})
    0.0
    """
    weighted_sum = 0
    codes = get_codes(tree)
    for key in codes:
        weighted_sum += freq_dict[key] * len(codes[key])
    total_frequencies = 0
    for key in freq_dict:
        total_frequencies += freq_dict[key]
    try:
        return weighted_sum / total_frequencies
    except ZeroDivisionError:
        return 0.0


def compress_bytes(text: bytes, codes: dict[int, str]) -> bytes:
    """ Return the compressed form of <text>, using the mapping from <codes>
    for each symbol.
    >>> d = {0: "0", 1: "10", 2: "11"}
    >>> text = bytes([1, 2, 1, 0, 2])
    >>> result = compress_bytes(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111001', '10000000']
    >>> text = bytes([1, 2, 1, 0])
    >>> result = compress_bytes(text, d)
    >>> result == bytes([184])
    True
    >>> [byte_to_bits(byte) for byte in result]
    ['10111000']
    >>> compress_bytes(bytes([]), {}) == bytes([])
    True
    >>> compress_bytes(bytes([0]), {0: '00000001'}) == bytes([1])
    True
    """
    if len(text) == 0:
        return bytes([])
    code = []
    to_be_converted = ''
    length_of_to_be_converted = 0
    # loop through every symbol in text, acquiring its code from the <codes>
    # dictionary, and storing it in current_code. Then, we add every bit of
    # current_code to the to_be_converted variable, until either (a) we exhaust
    # all the contents of current_code, in which case we would move on to the
    # code of the next symbol in <text>, or (b) the length of to_be_converted
    # reaches 8, in which case we would convert it to bytes and append it to the
    # code list and reset to_be_converted to be the empty string.
    for symbol in text:
        current_code = codes[symbol]
        length_current_code = len(current_code)
        for i in range(length_current_code):
            if length_of_to_be_converted == 8:
                code.append(bits_to_byte(to_be_converted))
                to_be_converted = current_code[i]
                length_of_to_be_converted = 1
                continue
            to_be_converted += current_code[i]
            length_of_to_be_converted += 1
    # to_be_converted has still not been converted yet (after the last
    # iteration), so we must convert it.
    if len(to_be_converted) != 0:
        to_be_converted += '0' * (8 - length_of_to_be_converted)
        code.append(bits_to_byte(to_be_converted))
    return bytes(code)


def tree_to_bytes(tree: HuffmanTree) -> bytes:
    """ Return a bytes representation of the Huffman tree <tree>.
    The representation should be based on the postorder traversal of the tree's
    internal nodes, starting from 0.

    Precondition: <tree> has its nodes numbered.

    >>> tree = HuffmanTree(None, HuffmanTree(3, None, None), \
    HuffmanTree(2, None, None))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2]
    >>> left = HuffmanTree(None, HuffmanTree(3, None, None), \
    HuffmanTree(2, None, None))
    >>> right = HuffmanTree(5)
    >>> tree = HuffmanTree(None, left, right)
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2, 1, 0, 0, 5]
    >>> tree = build_huffman_tree(build_frequency_dict(b"helloworld"))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))\
            #doctest: +NORMALIZE_WHITESPACE
    [0, 104, 0, 101, 0, 119, 0, 114, 1, 0, 1, 1, 0, 100, 0, 111, 0, 108,\
    1, 3, 1, 2, 1, 4]
    >>> tree_to_bytes(HuffmanTree()) == bytes([])
    True
    """
    # leaves do not have children, so they don't have a bytes representation.
    if tree.is_leaf():
        return bytes([])
    else:
        # recurse into the left and right trees (if they exist) and concatenate
        # their bytes representation with ans
        ans = bytes([])
        if tree.left is not None:
            ans += tree_to_bytes(tree.left)
        if tree.right is not None:
            ans += tree_to_bytes(tree.right)
        # now we add the representation of the root node.
        ans += bytes([int(not tree.left.is_leaf())])
        ans += bytes([tree.left.symbol]) if tree.left.is_leaf() \
            else bytes([tree.left.number])
        ans += bytes([int(not tree.right.is_leaf())])
        ans += bytes([tree.right.symbol]) if tree.right.is_leaf() \
            else bytes([tree.right.number])
        return ans


def compress_file(in_file: str, out_file: str) -> None:
    """ Compress contents of the file <in_file> and store results in <out_file>.
    Both <in_file> and <out_file> are string objects representing the names of
    the input and output files.

    Precondition: The contents of the file <in_file> are not empty.
    """
    with open(in_file, "rb") as f1:
        text = f1.read()
    freq = build_frequency_dict(text)
    tree = build_huffman_tree(freq)
    codes = get_codes(tree)
    number_nodes(tree)
    print("Bits per symbol:", avg_length(tree, freq))
    result = (tree.num_nodes_to_bytes() + tree_to_bytes(tree)
              + int32_to_bytes(len(text)))
    result += compress_bytes(text, codes)
    with open(out_file, "wb") as f2:
        f2.write(result)

# ====================
# Functions for decompression


def generate_tree_general(node_lst: list[ReadNode],
                          root_index: int) -> HuffmanTree:
    """ Return the Huffman tree corresponding to node_lst[root_index].
    The function assumes nothing about the order of the tree nodes in the list.

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 1, 1, 0)]
    >>> generate_tree_general(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(10, None, None), \
HuffmanTree(12, None, None)), \
HuffmanTree(None, HuffmanTree(5, None, None), HuffmanTree(7, None, None)))
    """
    # if the left subtree type as defined by the ReadNode at <root_index> is
    # 0, then simply assign a leaf as the left subtree with the second byte
    # contained in that ReadNode. Otherwise, make a recursive call, but with
    # the <root_index> parameter being the second byte contained in this
    # ReadNode (which represents the index of that left subtree). The scenario
    # for the right subtree is analogous.
    tree = HuffmanTree()
    if node_lst[root_index].l_type == 0:
        tree.left = HuffmanTree(node_lst[root_index].l_data)
    else:
        tree.left = generate_tree_general(node_lst, node_lst[root_index].l_data)
    if node_lst[root_index].r_type == 0:
        tree.right = HuffmanTree(node_lst[root_index].r_data)
    else:
        tree.right = generate_tree_general(node_lst,
                                           node_lst[root_index].r_data)
    return tree


def generate_tree_postorder(node_lst: list[ReadNode],
                            root_index: int) -> HuffmanTree:
    """ Return the Huffman tree corresponding to node_lst[root_index].
    The function assumes that the list represents a tree in postorder.

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 0, 1, 0)]
    >>> generate_tree_postorder(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(5, None, None), \
HuffmanTree(7, None, None)), \
HuffmanTree(None, HuffmanTree(10, None, None), HuffmanTree(12, None, None)))
    >>> lst = [ReadNode(0, 104, 0, 101), ReadNode(0, 119, 0, 114), \
    ReadNode(1, 0, 1, 1), ReadNode(0, 100, 0, 111), ReadNode(0, 108,\
    1, 3), ReadNode(1, 2, 1, 4)]
    """
    return _generate_tree_postorder_helper(node_lst, root_index, _Counter())


def _generate_tree_postorder_helper(node_lst: list[ReadNode],
                                    root_index: int, found: _Counter = None) \
        -> HuffmanTree:
    """ A recursive helper function for generate_tree_postorder

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 0, 1, 0)]
    >>> generate_tree_postorder(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(5, None, None), \
HuffmanTree(7, None, None)), \
HuffmanTree(None, HuffmanTree(10, None, None), HuffmanTree(12, None, None)))
    >>> lst = [ReadNode(0, 104, 0, 101), ReadNode(0, 119, 0, 114), \
    ReadNode(1, 0, 1, 1), ReadNode(0, 100, 0, 111), ReadNode(0, 108,\
    1, 3), ReadNode(1, 2, 1, 4)]
    """
    l_type = node_lst[root_index].l_type
    l_data = node_lst[root_index].l_data
    r_type = node_lst[root_index].r_type
    r_data = node_lst[root_index].r_data
    tree = HuffmanTree()
    # if the tree has both right and left subtrees as leaves, then this is our
    # base case -- simply assign to leaves to the left and right subtrees.
    if l_type == 0 and r_type == 0:
        tree.left = HuffmanTree(l_data)
        tree.right = HuffmanTree(r_data)
    # otherwise, we follow the post ordering number procedure in reverse. In the
    # numbering process, we would number the left tree from top up, then the
    # right tree from top up, and then finally, the root. To work in reverse,
    # the
    else:
        found_before = found.count
        if r_type == 1:
            found.count += 1
            tree.right = _generate_tree_postorder_helper(node_lst, root_index
                                                         - 1, found)
        else:
            tree.right = HuffmanTree(r_data)
        difference = found.count - found_before
        if l_type == 1:
            found.count += 1
            tree.left = _generate_tree_postorder_helper(node_lst, root_index - 1
                                                        - difference, found)
        else:
            tree.left = HuffmanTree(l_data)
    return tree


def decompress_bytes(tree: HuffmanTree, text: bytes, size: int) -> bytes:
    """ Use Huffman tree <tree> to decompress <size> bytes from <text>.

    >>> tree = build_huffman_tree(build_frequency_dict(b'helloworld'))
    >>> number_nodes(tree)
    >>> decompress_bytes(tree, \
             compress_bytes(b'helloworld', get_codes(tree)), len(b'helloworld'))
    b'helloworld'
    """
    # first, create a string, bits, that contains the bytes representation of
    # entire <text> parameter.

    # bits = "".join([byte_to_bits(byte) for byte in text])
    codes = get_codes(tree)

    # the code_to_byte dictionary will act as an "inverse dictionary" of codes,
    # mapping codes to bytes instead of bytes to codes. The dictionary is built
    # in the for loop below.
    code_to_byte = {}
    for byte in codes:
        code_to_byte.setdefault(codes[byte], byte)
    to_be_converted = []
    current_code = ''
    found = 0
    # this loop follows the same description as the while loop below, but is
    # more time-efficient.
    for byte in text:
        r, current_code, found = _decompress_bytes_helper((byte, code_to_byte,
                                                           to_be_converted,
                                                           current_code, found,
                                                           size))
        if r:
            break

    # now, begin a loop that ends when we have found <size> bytes (since there
    # may be unwanted zeros at the end that we padded during compression). This
    # loop will treat the bits local variable as a queue, looking at every bit
    # from its beginning. Once it recognises a sequence of bits as a valid code
    # as defined by code_to_byte, it will map it to a byte, and append that byte
    # to the to_be_converted list, and then clear the current_code.

    # # while loop version
    # while found != size:
    #     current_code += bits[i]
    #     if current_code in code_to_byte:
    #         to_be_converted.append(code_to_byte[current_code])
    #         found += 1
    #         current_code = ''
    #     i += 1

    return bytes(to_be_converted)


def _decompress_bytes_helper(t: tuple[int, dict, list, str, int, int]) \
        -> tuple[bool, str, int]:
    """ A helper for the for loop in decompress bytes.
     """
    byte, code_to_byte, to_be_converted, current_code, found, size = t
    for bit in byte_to_bits(byte):
        current_code += bit
        if current_code in code_to_byte:
            to_be_converted.append(code_to_byte[current_code])
            found += 1
            current_code = ''
            if found == size:
                return True, current_code, found
    return False, current_code, found


def decompress_file(in_file: str, out_file: str) -> None:
    """ Decompress contents of <in_file> and store results in <out_file>.
    Both <in_file> and <out_file> are string objects representing the names of
    the input and output files.

    Precondition: The contents of the file <in_file> are not empty.
    """
    with open(in_file, "rb") as f:
        num_nodes = f.read(1)[0]
        buf = f.read(num_nodes * 4)
        node_lst = bytes_to_nodes(buf)
        # use generate_tree_general or generate_tree_postorder here
        tree = generate_tree_postorder(node_lst, num_nodes - 1)
        size = bytes_to_int(f.read(4))
        with open(out_file, "wb") as g:
            text = f.read()
            g.write(decompress_bytes(tree, text, size))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
