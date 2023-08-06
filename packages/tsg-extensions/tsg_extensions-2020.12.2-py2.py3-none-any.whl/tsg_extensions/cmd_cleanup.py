#-*- coding: UTF-8 -*-
"""Works in tandem with the ``cmd.py`` extension to escape the < and > chars"""
import re
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

from .cmd import CMD_RE


class CmdCleanupExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        md.preprocessors.register(CmdCleanupPreprocessor(md), 'cmd_cleanup', 20)


class CmdCleanupPreprocessor(Preprocessor):
    def run(self, lines):
        """Detect lines with CMD_RE syntax, and escape the < and > chars"""
        for idx, line in enumerate(lines):
            if re.search(CMD_RE, line):
                new_line = line.replace('<', '&lt;').replace('>', '&gt;').replace(r'\\', r'\\\\').replace('*', '\*')
                lines[idx] = new_line
        return lines


def makeExtension(**kwargs):  # pragma: no cover
    return CmdCleanupExtension(**kwargs)
