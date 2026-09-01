import unittest
from xmltohtml import markdown_to_html_node # type: ignore
import re

class TestTextNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_comobo(self):
        md = """
        
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_comobo2(self):
        md = """
        
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

```
This is text that _should_ remain
the **same** even with inline stuff
```

- oh look
- un unordered list
- oops forgot a space
- that should be fine though


1. oopsie too many enters, hopefully nothing
2. untoward happens
3. lol
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre><ul><li>oh look</li><li>un unordered list</li><li>oops forgot a space</li><li>that should be fine though</li></ul><ol><li>oopsie too many enters, hopefully nothing</li><li>untoward happens</li><li>lol</li></ol></div>",
        )

    def test_regex(self):
        self.assertEqual(r"^- ", r"^" + r"- ")

    def test_regex_split(self):
        self.assertEqual(2, len(re.split(r"\d+\. ", "1. oopsie too many errors, hopefully nothing", maxsplit=1)))

if __name__ == "__main__":
    unittest.main()