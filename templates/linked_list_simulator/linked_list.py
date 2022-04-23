"""
=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.
"""
from __future__ import annotations
from typing import Any, Optional


class _Node:
    """A node in a linked list.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        A reference to another node, or None if no node is referenced.
    """
    item: Any
    next: Optional[_Node]

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List abstract data type that supports
    augmentation.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    _first: Optional[_Node]
    _length: int

    def __init__(self, items: list) -> None:
        """Initialize a new linked list containing the given items, and keep
        track of the length accordingly.

        The first node in the linked list contains the first item
        in <items>.
        """
        if len(items) == 0:
            self._first = None
            self._length = 0
        else:
            self._first = _Node(items[0])
            self._length = 1
            current = self._first
            for item in items[1:]:
                new = _Node(item)
                current.next = new
                current = new
                self._length += 1

    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        >>> LinkedList([]).is_empty()
        True
        >>> LinkedList([1, 2, 3]).is_empty()
        False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedList([]))
        '[]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def to_file(self, file_name: str) -> None:
        """ Export a string representation of this LinkedList to a file with
        name <file_name>. """
        if self._length == 0:
            with open(file_name, 'w') as file:
                file.write("Linked list is empty!")
                return

        to_write = self.__str__()
        print(type(to_write))
        print(to_write)
        with open(file_name, 'w') as file:
            print(f"STRING IS{str(to_write[0])}")
            print(f'LENGTH IS {len(str(to_write[0]))}')
            file.write((" " * ((len(str(to_write[0])) + 1) // 2)
                        + '|' + '\n') * 3 + " " *
                       ((len(str(to_write[0])) + 1) // 2) + "v" + '\n')
            for i in range(len(to_write)):
                file.write("|")
                file.write("-" * len(to_write[i]))
                file.write('|' + 3 * '-' + '|' + ' ' * 4)
            file.write('\n')

            for i in range(len(to_write)):
                file.write("|")
                file.write(str(to_write[i]))
                file.write('|')
                file.write('-' * 6 + '>' + ' ')
            file.write('NONE')
            file.write('\n')

            for i in range(len(to_write)):
                file.write("|")
                file.write("-" * len(to_write[i]))
                file.write('|' + 3 * '-' + '|' + ' ' * 4)

    def __getitem__(self, index: int) -> Any:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.
        """
        if index < 0:
            raise IndexError

        curr = self._first
        curr_index = 0

        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def insert(self, index: int, item: Any) -> None:
        """Insert the given item at the given index in this list.

        Raise IndexError if index > len(self) or index < 0.

        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.insert(2, 300)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200]'
        >>> lst.insert(5, -1)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200 -> -1]'
        >>> lst.insert(100, 2)
        Traceback (most recent call last):
        IndexError
        """
        if index < 0:
            raise IndexError

        # Create new node containing the item
        new_node = _Node(item)

        if index == 0:
            self._first, new_node.next = new_node, self._first
        else:
            # Iterate to (index-1)-th node.
            curr = self._first
            curr_index = 0
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index += 1

            if curr is None:
                raise IndexError
            else:
                # Update links to insert new node
                curr.next, new_node.next = new_node, curr.next
                self._length += 1

    def __len__(self) -> int:
        """Return the number of items in this list.

        >>> lst = LinkedList([])
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = LinkedList([1, 2, 3])
        >>> len(lst)
        3
        """
        return self._length

    def count(self, item: Any) -> int:
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        count = 0
        current = self._first
        while current is not None:
            if current.item == item:
                count += 1
            current = current.next
        return count

    def index(self, item: Any) -> int:
        """Return the index of the first occurrence of <item> in this list.

        Raise ValueError if the <item> is not present.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.index(1)
        0
        >>> lst.index(3)
        3
        >>> lst.index(148)
        Traceback (most recent call last):
        ValueError
        """
        count = 0
        current = self._first
        while current is not None:
            if current.item == item:
                return count
            current = current.next
            count += 1
        raise ValueError

    def __setitem__(self, index: int, item: Any) -> None:
        """Store item at position <index> in this list.

        Raise IndexError if index >= len(self).

        >>> lst = LinkedList([1, 2, 3])
        >>> str(lst)
        '[1 -> 2 -> 3]'
        >>> lst[0] = 100  # Equivalent to lst.__setitem__(0, 100)
        >>> lst[1] = 200
        >>> lst[2] = 300
        >>> str(lst)
        '[100 -> 200 -> 300]'
        """
        if index >= len(self) or index < 0:
            raise IndexError
        current_index = 0
        current = self._first
        while current_index != index:
            current = current.next
            current_index += 1
        current.item = item

    def delete_one(self, item: Any) -> None:
        """ Remove the *first* occurrence of <item> in this LinkedList.

        Raise ValueError if <item> is not in this LinkedList.

        >>> lst = LinkedList([1, 2, 3])
        >>> lst.delete_one(2)
        >>> str(lst)
        '[1 -> 3]'
        >>> lst = LinkedList([2, 2, 3])
        >>> lst.delete_one(2)
        >>> str(lst)
        '[2 -> 3]'
        """
        if len(self) == 0:
            raise ValueError
        if self._first.item == item:
            self._first = self._first.next
        curr = self._first
        while curr is not None:
            if curr.next.item == item:
                curr.next = curr.next.next
                return
            curr = curr.next
        raise ValueError

    def delete_all(self, item: Any) -> None:
        """ Remove *every* occurrence of <item> in this LinkedList.

        Raise ValueError if <item> is not in this LinkedList.

        >>> lst = LinkedList([2, 2, 3])
        >>> lst.delete_all(2)
        >>> str(lst)
        '[3]'
        >>> lst = LinkedList([1, 2, 3])
        >>> lst.delete_all(2)
        >>> str(lst)
        '[1 -> 3]'
        """
        if len(self) == 0:
            raise ValueError

        found = False

        while self._first.item == item:
            self._first = self._first.next
            found = True

        curr = prev = self._first
        while curr is not None:
            if curr.item == item:
                prev.next = curr.next
                found = True
                curr = curr.next
                continue
            prev = curr
            curr = curr.next
        if not found:
            raise ValueError


if __name__ == '__main__':
    import doctest
    doctest.testmod()
