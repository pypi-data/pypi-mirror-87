"""
core mrkup module
"""

from typing import List, Optional, Union
import abc


def _stringify(level: int,
               indent: Optional[int],
               taginfo: dict,
               tag_start: str = "",
               tag_end: str = "/") -> str:
    """
    For use by the strinfigy() methods of Tag and PI objects

    level: indentation level
    indent: number of spaces per indentation level
    taginfo: attributes of the Tag object being stringified
    tag_start: starting of opening tag before tag name
    tag_end: ending of opening tag after tag name

    For example, in

        <?tst echo "hello" !>

    "?" is tag_start
    "!" is tag_end
    """
    # start opening tag
    if indent is None:
        space = ""
    else:
        space = "\n" + (level * (' ' * indent))
    tag_str = f"{space}<{tag_start}{taginfo['name']}"

    for key in taginfo['attrs']:
        if taginfo['attrs'][key] is None:
            tag_str += f" {key}"
        else:
            tag_str += f" {key}=\"{taginfo['attrs'][key]}\""

    # end opening tag
    if taginfo["close"] is None:
        # if self-closed tag
        tag_str += f" {tag_end}>"
        return tag_str

    tag_str += f"{tag_start}>"
    if taginfo["close"] is False:
        return tag_str

    # children
    for child in taginfo["children"]:
        if isinstance(child, Node):
            # handle non-strings
            tag_str += child.stringify(level+1, indent)
        else:
            # handle plain strings
            if indent is not None:
                tag_str += space + " " * indent
            tag_str += str(child)

    # closing tag
    if indent is not None:
        tag_str += "\n" + (level * (' ' * indent))
    tag_str += f"<{tag_end}{taginfo['name']}>"

    return tag_str


class Node(abc.ABC):
    """
    Abstract class representing all supported nodes except plain strings.
    Including comments and tags
    """
    def __str__(self):
        """# To satifsy pylint (R0903)"""

    @abc.abstractmethod
    def stringify(self, level: int, indent: Optional[int]):
        """
        Abstract method which should return a stringified form of the node
        """


class Comment(Node):
    """
    Represent a comment
    """
    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f"Comment({self.text!r})"

    def __str__(self):
        return f"<!--{self.text}-->"

    def stringify(self,
                  level: int = 0,
                  indent: Optional[int] = 2) -> str:
        """
        Format the comment to a string.

        Value of level is ignored if indent is None.

        Args:
          level: indentation level
          indent: number of spaces per indentation level. None if
            not to be pretty printed.

        Returns:
          A stringified form of the comment.
        """
        if indent is None:
            return str(self)
        space = "\n" + level * (' ' * indent)
        return f"{space}{self}"


class NamedNode(Node):
    """
    Abstract method representing all nodes which has a name and can have
    attributes.
    """
    def __init__(self,
                 name: str,
                 attrs: Optional[dict]):
        self.name = name
        if attrs is None:
            self.attrs = {}
        else:
            self.attrs = attrs

    def __str__(self):
        return self.name


class Tag(NamedNode):
    """
    Represent a tag
    """
    def __init__(self,
                 name: str,
                 attrs: dict = None,
                 children: List[Union[Node, str]] = None,
                 close: Optional[bool] = True):
        """
        Args:
          name: name of tag
          attrs: attributes of tag as a dictionary. Attributes without
            value can have their value as None
          children: child tags, comments and text of the tag as a list
          close: determines if the tag is explicitly closed (True),
            self-closed (None) or not closed (False)

        Examples:
        >>> tag = Tag(name="input",
                      attrs={"type": "text", "required": None}, close=None)
        >>> tag.stringify()
        <input type="text" required />

        >>> tag = Tag(name="br", close=False)
        >>> tag.stringify()
        <br>

        >>> tag = Tag(name="p", children=["Hello"])
        >>> tag.stringify()
        <p>
          Hello
        </p>
        """
        super().__init__(name, attrs)
        if close is not True and children is not None:
            raise ValueError("Only closed tags can have children")
        if children is None:
            self.children = []
        else:
            self.children = children
        self.close = close

    def __repr__(self):
        return (f"Tag({self.name!r}, {self.attrs!r}, {self.children!r}, "
                f"{self.close!r})")

    def stringify(self,
                  level: int = 0,
                  indent: Optional[int] = 2) -> str:
        """
        Format the tag and its children to a string.

        Value of level is ignored if indent is None.

        Args:
          level: indentation level
          indent: number of spaces per indentation level. None if
            not to be pretty printed.

        Returns:
          A stringified form of the tag with all its children.
        """
        taginfo = {"name": self.name,
                   "attrs": self.attrs,
                   "children": self.children,
                   "close": self.close}
        return _stringify(level, indent, taginfo)


class PI(NamedNode):
    """
    Represent a processing instruction
    """
    def __init__(self,
                 name: str,
                 attrs: dict = None):
        super().__init__(name, attrs)

    def __repr__(self):
        return f"PI({self.name!r}, {self.attrs!r})"

    def stringify(self,
                  level: int = 0,
                  indent: Optional[int] = 2) -> str:
        """
        Format the processing instruction to a string.

        Value of level is ignored if indent is None.

        Args:
          level: indentation level
          indent: number of spaces per indentation level. None if
            not to be pretty printed.

        Returns:
          A stringified form of the processing instruction.
        """
        taginfo = {"name": self.name,
                   "attrs": self.attrs,
                   "children": None,
                   "close": False}
        return _stringify(level, indent, taginfo, "?", "?")
