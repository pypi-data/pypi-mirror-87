# mrkup

<a href="https://pypi.org/project/mrkup"><img alt="PyPI" src="https://img.shields.io/pypi/v/mrkup"></a>
<a href="https://codeberg.org/ju-sh/mrkup/src/branch/master/LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/pypi/l/mrkup"></a>

Just marking things up...

Compose HTML (and some XML) using Python.

<i>mrkup</i> can be used to compose html programatically which can then be converted to string but cannot parse html from external sources.

<h2>Installation</h2>

You need Python>=3.6 to use <i>mrkup</i>.

It can be installed from PyPI with pip using

```
    pip install mrkup
```

<h2>Usage</h2>

<i>mrkup</i> consists of three classes:

 - `Tag`
 - `Comment`
 - `PI`

which may be imported like

```
    from mrkup import Comment, PI, Tag
```

<h3>Tags</h3>

Used to compose tags.

```
    Tag(name: str,
        attrs: dict = None,
        children: List[Union[Node, str]] = None,
        close: Optional[bool] = True)
```

`Tag` objects have the following attributes:

 - name: tag's name
 - attrs: dictionary with attributes of tag.
 - children: list of children tags and strings of the tag
 - close: value determining whether the tag should be closed separately or self-closed or unclosed.

If an attribute need to be specified without value, it should be present in the `attrs` dictionary as a key but with its value as `None`. Like

```
    >>> text = Tag("input", attrs={"type": "text", "required": None},
    ...            close=None)
    >>> text.stringify(indent=None)
    '<input type="text" required />'
```

`children` would have the list of `Tag`s and `strs`s that comes under the tag object.

`close` value can be used to control the manner in which the tag is closed as follows:

 - True: Allow a separate closing tag (default)
 - None: Self-closed tag
 - False: Don't close tag

Like

```
    # close=True (separate closing tag)
    >>> text = Tag("p", children=["Hello!"])
    >>> print(text.stringify())

    <p>
      Hello!
    </p>

```

```
    # close=None (self-closed tag)
    >>> text = Tag("img", attrs={"src": "server/img.jpg"}, close=None)
    >>> text.stringify(indent=None)
    '<img src="server/img.jpg" />'
```

```
    # close=False (open tag)
    >>> text = Tag("br", close=False)
    >>> text.stringify(indent=None)
    '<br>'
```

Note: `children` attribute of a `Tag` object is ignored during stringification if its `close` value is not True.

Note: `attrs` and `children` attributes of a `Tag` object can be accessed and modified like a normal dict and list respectively.

Note: In <i>mrkup</i>, the `<!DOCTYPE html>` declaration is meant to be implemented with the `Tag` class itself like

```
    >>> doctype = Tag("!DOCTYPE", attrs={"html": None})
    >>> doctype.stringify(indent=None)
    '<!DOCTYPE html>'
```

<h3>Comments</h3>

Used to compose HTML comments.

```
    Comment(text: str)
```

Like

```
    >>> comment = Comment("Just a comment")
    >>> comment.stringify(indent=None)
    '<!--Just a comment-->'
```

<h3>Processing instructions</h3>

Can be used for composing the XML version declaration like

```
    PI(name: str,
       attrs: dict = None)
```

Like

```
    >>> xml_pi = PI("xml", attrs={"version": "1.0", "encoding": "UTF-8"})
    >>> xml_pi.stringify(indent=None)
    '<?xml version="1.0" encoding="UTF-8"?>'
```

<h3>Converting to string</h3>

The composed HTML can be converted to an equivalent string using the `stringify()` method of the objects.

<h4>Indentation</h4>

Indentation level and number of spaces per indentation level used by the `stringify()` method can be specified using the `level` and `indent` argument respectively.

By default `stringify()` does pretty-printing with `indent` value `2`.

If `indent` is `None`, pretty-printing is disabled and value of `level` is ignored.

<h3>Style and script data</h3>

JavaScript contents of `<script>` and CSS of `<style>` are simply treated as plain text in <i>mrkup</i>.

Like

```
    >>> content = "p { text-align: center; }"
    >>> style = Tag("style", children=[content])
    >>> print(style.stringify())
    <style>
      p { text-align: center; }
    </style>
```

<h3>No HTML validation</h3>
<i>mrkup</i> doesn't perform any validation to be sure that the tags are valid HTML.

So we could also use it to create some XML..

<h3>Example</h3>

```
from mrkup import Tag, Comment

# doctype is not part of the html tag
doctype = Tag("!DOCTYPE", attrs={"html": None}, close=False)

comment = Comment("Here comes the list!")
ol = Tag("ol")
for loc in ['home', 'about', 'contact']:
    a = Tag("a", attrs={"href": f"/{loc}.html"}, children=[loc.title()])
    li = Tag("li", children=[a])
    ol.children.append(li)
h1 = Tag("h1", children=["Hey there!"])
img = Tag("img", attrs={"src": "server/img.jpg"}, close=False)
br = Tag("br", close=None)
body = Tag("body", children=[h1, img, br, "\n", comment, ol])

title = Tag("title", children=["Mrkup your markup"])
link = Tag("link", attrs={"href": "style.css", "rel": "stylesheet"},
           close=None)
script = Tag("script", attrs={"src": "script.js", "type": "text/javascript"})
head = Tag("head", children=[title, link, script])

html = Tag("html", children=[head, body])

# Generate string version
doc = doctype.stringify() + html.stringify()
print(doc)
```

This would generate the following:

```
<!DOCTYPE html>
<html>
  <head>
    <title>
      Mrkup your markup
    </title>
    <link href="style.css" rel="stylesheet" />
    <script src="script.js" type="text/javascript">
    </script>
  </head>
  <body>
    <h1>
      Hey there!
    </h1>
    <img src="server/img.jpg">
    <br />
    

    <!--Here comes the list!-->
    <ol>
      <li>
        <a href="/home.html">
          Home
        </a>
      </li>
      <li>
        <a href="/about.html">
          About
        </a>
      </li>
      <li>
        <a href="/contact.html">
          Contact
        </a>
      </li>
    </ol>
  </body>
</html>
```
