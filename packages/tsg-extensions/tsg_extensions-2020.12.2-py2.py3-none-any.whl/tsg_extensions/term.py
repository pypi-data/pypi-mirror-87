# -*- coding: UTF-8 -*-
"""
Overrides the HTML generated for an indented code block by wrapping it in a <div>
defining a CSS class "terminal". This allows the code block to look like a Linux/UNIX
terminal when displayed in a web page.

For example, when you write some markdown like this:

# Some heading

Run the following command:

    some output that looks like a terminal

Here's what the resulting HTML looks like:
<h1>Some heading</h1>
<p>Run the following command:</p>
<div class="terminal">
 <pre>
   <code>some output that looks like a terminal
   </code>
 </pre>
</div>

The use of a <div> is so we get a solid block, instead of the background color
simply wrapping the text.
"""
import xml.etree.ElementTree as ET

import markdown
from markdown.blockprocessors import CodeBlockProcessor, util, BlockParser


class TermTreeProcessor(markdown.treeprocessors.Treeprocessor, markdown.extensions.Extension):
    def run(self, root):
        for idx, element in enumerate(root):
            if element.tag == 'pre':
                try:
                    if element[0].tag == 'code':
                        div = self.make_div(element)
                        root[idx] = div
                except IndexError:
                    continue

    def make_div(self, pre_element):
        div = ET.Element('div')
        div.append(pre_element)
        pre_element.set('class', 'terminal')
        return div

    def extendMarkdown(self, md):
        md.treeprocessors.register(TermTreeProcessor(), 'terminal', 15)


def makeExtension(**kwargs):
    return TermTreeProcessor(**kwargs)
