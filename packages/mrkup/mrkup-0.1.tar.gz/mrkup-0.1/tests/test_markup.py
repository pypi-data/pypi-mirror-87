import pytest
from mrkup import Comment, PI, Tag


class TestComment:
    @pytest.mark.parametrize("level,indent,expected", [
        (1, 4, "\n    <!--Just a comment-->"),
        (2, None, "<!--Just a comment-->"),
    ])
    def test_stringify(self, level, indent, expected):
        comment = Comment("Just a comment")
        assert comment.stringify(level, indent) == expected

    def test_repr(self):
        comment = Comment("Just a comment")
        assert repr(comment) == "Comment('Just a comment')"


class TestTag:
    @pytest.mark.parametrize("level,indent,tag,expected", [
        # Open tag
        (1, 2,
         Tag("input", {"type": "text", "class": "info"},
             children=[Tag("hr", close=False)]),
         """
  <input type="text" class="info">
    <hr>
  </input>"""),

        # Tag with string child
        (1, 2,
         Tag("p", children=["hello"]), """
  <p>
    hello
  </p>"""),

        # Self-closed tag
        (1, None,
         Tag("img", attrs={"src": "server/file.jpg"}, close=None),
         '<img src="server/file.jpg" />'),

        # Closed tag and unformatted stringification
        (1, None,
         Tag("ol", children=[Tag("li", children=["One"]),
                             Tag("li", children=["Two"])]),
         "<ol><li>One</li><li>Two</li></ol>"),

        # Often used 'tag' (actually a declaration)
        (1, None,
         Tag("!DOCTYPE", {"html": None}, close=False),
         "<!DOCTYPE html>")
    ])
    def test_stringify(self, level, indent, tag, expected):
        assert tag.stringify(level, indent) == expected

    def test_invalid(self):
        with pytest.raises(ValueError):
            Tag("opentag", close=False, children=["hi"])

    def test_str(self):
        tag = Tag("html")
        assert str(tag) == "html"

    def test_repr(self):
        tag = Tag("html")
        assert repr(tag) == "Tag('html', {}, [], True)"


class TestPI:
    @pytest.mark.parametrize("level,indent,tag,expected", [
        (1, 2,
         PI("xml", {"version": "1.0", "encoding": "UTF-8"}),
         """
  <?xml version="1.0" encoding="UTF-8"?>"""),
    ])
    def test_stringify(self, level, indent, tag, expected):
        assert tag.stringify(level, indent) == expected

    def test_repr(self):
        pi_instr = PI("xml")
        assert repr(pi_instr) == "PI('xml', {})"
