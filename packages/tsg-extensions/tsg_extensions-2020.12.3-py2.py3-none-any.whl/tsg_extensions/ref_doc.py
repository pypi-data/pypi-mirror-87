# -*- coding: UTF-8 -*-
"""
Modified Markdown syntax for generating links to Dell EMC KBs & documents.
"""
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

REFDOC_RE = r'\[\[([\w0-9_.: -]+)\]\]'


class RefDocExtension(Extension):
    def extendMarkdown(self, md, config):
        self.md = md
        md_pattern = RefDocInlineProcessor(REFDOC_RE)
        md_pattern.md = md
        md.inlinePatterns.register(md_pattern, 'ref_doc', 70)


class RefDocInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        if m.group(1).strip():
            html_class = 'ref-doc'
            label = m.group(1).strip()
            url, title = self.build_url(label)
            a = etree.Element('a')
            a.text = title
            a.set('href', url)
            a.set('class', html_class)
            a.set('target', '_blank')
        else:
            a = ''
        return a, m.start(0), m.end(0)

    def build_url(self, label):
        base = 'https://www.dell.com/support/kbdoc/en-us/'
        label_bits = label.split(' ')
        if label_bits[0].lower() == 'kb':
            middle = '{}'.format(label_bits[-1].strip())
            title = 'article {}'.format(label_bits[-1].strip())
        elif label_bits[0].lower() == 'bug':
            middle = label_bits[-1].strip()
            base = 'https://bugs.west.isilon.com/'
            title = 'Bug {}'.format(middle)
        elif label_bits[-1].lower().startswith('docu'):
            base = 'https://dl.dell.com/content/'
            middle = label_bits[-1]
            title = ' '.join(label_bits[:-1])
        else:
            base = 'https://www.dellemc.com/resources/en-us/asset/white-papers/products/storage/'
            middle = label_bits[-1]
            title = ' '.join(label_bits[:-1])
        return '{}{}'.format(base, middle), title

def makeExtension(**kwargs):
    return RefDocExtension(**kwargs)
