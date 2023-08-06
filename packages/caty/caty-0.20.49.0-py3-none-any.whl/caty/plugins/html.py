from htmldump.html_parser import HTML as Parser

from .base import RawReader, TextDumper


class HTML(RawReader, TextDumper):
    ext = 'html', 'htm'

    def load(self, raw):
        return Parser(raw)

    def parse(self, html):
        for node in html.body.walk_relative():
            yield node
            if node.data:
                yield node.data

