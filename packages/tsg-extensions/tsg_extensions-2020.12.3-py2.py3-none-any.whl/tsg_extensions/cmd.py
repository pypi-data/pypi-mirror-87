# -*- coding: UTF-8 -*-
"""
Unique syntax for formatting sample CLI commands
"""
import re
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

CMD_RE = '\$(.*)\$'

class CmdExtension(Extension):
    def extendMarkdown(self, md, config):
        self.md = md
        md_pattern = CmdInlineProcessor(CMD_RE)
        md_pattern.md = md
        md.inlinePatterns.register(md_pattern, 'cmd', 71)


class CmdInlineProcessor(InlineProcessor):
    def __init__(self, pattern, md=None):
        """The default class compiles with re.DOTALL, so newline chars are matched"""
        self.pattern = pattern
        self.compiled_re = re.compile(pattern)
        # Api for Markdown to pass safe_mode into instance
        self.safe_mode = False
        self.md = md

    def handleMatch(self, m, data):
        if m.group(0).strip():
            label = m.group(0).strip()[1:-1] # slice off the leading and trailing $
            cmd = etree.Element('code')
            cmd.text = label
            cmd.set('class', 'command')
        else:
            cmd = ''
        return cmd, m.start(0), m.end(0)


def makeExtension(**kwargs):
    return CmdExtension(**kwargs)
