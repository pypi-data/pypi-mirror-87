import abc
import json
import logging
import re
from collections import defaultdict
from pathlib import Path
from robot.libdocpkg import htmlwriter
from docgen import rest

# Populated dynamically
CONVERTERS = {}


def convert(libdoc, fmt, dirname):
    """Convert libdoc model into output file."""
    converter = CONVERTERS.get(fmt)
    if not converter:
        raise ValueError(f"Unknown conversion format: {fmt}")

    filename = Path(libdoc.name.replace(".", "_"))
    filename = filename.with_suffix(converter.EXTENSION)

    path = Path(dirname) / filename
    converter().convert(libdoc, path)
    logging.info("Created file: %s", path)


class ConverterMeta(abc.ABCMeta):
    def __new__(cls, name, bases, namespace, **kwargs):
        converter = super().__new__(cls, name, bases, namespace, **kwargs)
        if name == "BaseConverter":
            return converter

        if not getattr(converter, "NAME", None):
            raise ValueError(f"Undefined 'NAME' attribute in {converter}")
        if not getattr(converter, "EXTENSION", None):
            raise ValueError(f"Undefined 'EXTENSION' attribute in {converter}")
        if converter.NAME in CONVERTERS:
            raise ValueError(f"Duplicate converter for {converter.NAME}")

        CONVERTERS[converter.NAME] = converter
        return converter


class BaseConverter(metaclass=ConverterMeta):
    NAME = None
    EXTENSION = None

    @abc.abstractmethod
    def convert(self, libdoc, output):
        raise NotImplementedError


class JsonConverter(BaseConverter):
    NAME = "json"
    EXTENSION = ".json"

    class _NullFormatter:
        def html(self, doc, *args, **kwargs):
            return doc

    def convert(self, libdoc, output):
        data = htmlwriter.JsonConverter(self._NullFormatter()).convert(libdoc)
        with open(output, "w") as fd:
            json.dump(data, fd, indent=4)


class JsonHtmlConverter(BaseConverter):
    NAME = "json-html"
    EXTENSION = ".json"

    def convert(self, libdoc, output):
        formatter = htmlwriter.DocFormatter(
            libdoc.keywords, libdoc.doc, libdoc.doc_format
        )
        data = htmlwriter.JsonConverter(formatter).convert(libdoc)

        # Format keyword shortdoc with correct formatter, strip extra HTML tags
        for keyword in data["keywords"]:
            shortdoc = formatter.html(keyword["shortdoc"])
            shortdoc = re.search(r"<p>(.*)<\/p>", shortdoc)

            if shortdoc is None:
                logging.warning(
                    "Missing shortdoc: %s.%s", data["name"], keyword["name"]
                )
                continue

            keyword["shortdoc"] = shortdoc.group(1)

        with open(output, "w") as fd:
            json.dump(data, fd, indent=4)


class XmlConverter(BaseConverter):
    NAME = "xml"
    EXTENSION = ".xml"

    def convert(self, libdoc, output):
        libdoc.save(output, "XML")


class HtmlConverter(BaseConverter):
    NAME = "html"
    EXTENSION = ".html"

    def convert(self, libdoc, output):
        libdoc.save(output, "HTML")


class XmlHtmlConverter(BaseConverter):
    NAME = "xml-html"
    EXTENSION = ".html"

    def convert(self, libdoc, output):
        libdoc.save(output, "XML:HTML")


class RestConverter(BaseConverter):
    NAME = "rest"
    EXTENSION = ".rst"

    IGNORE = (r"^:param.*", r"^:return.*")

    def __init__(self):
        self.ignore_block = False

    def convert(self, libdoc, output):
        writer = rest.RestWriter()
        with writer.heading(libdoc.name):
            self.overview(writer, libdoc)
            # self.inits(writer, libdoc)
            self.keywords(writer, libdoc)
        writer.save(output)

    def filter_docstring(self, text):
        output = []
        for line in text.split("\n"):
            if any(re.match(pattern, line) for pattern in self.IGNORE):
                self.ignore_block = True
                continue
            if line.startswith(" ") and self.ignore_block:
                continue

            self.ignore_block = False
            output.append(line)
        return "\n".join(output)

    @staticmethod
    def escape_string(text):
        return text.replace("*", "\\*")

    def overview(self, writer, libdoc):
        with writer.heading("Description"):
            writer.fieldlist(("Library scope", libdoc.scope))
            writer.raw(self.filter_docstring(libdoc.doc))

    def inits(self, writer, libdoc):
        with writer.heading("Init"):
            for init in libdoc.inits:
                writer.raw(init.doc)

    def keywords(self, writer, libdoc):
        groups = defaultdict(list)
        for keyword in libdoc.keywords:
            name = Path(keyword.source).stem
            groups[name].append(keyword)

        def _init_first(string):
            return string == "__init__", string

        with writer.heading("Keywords"):
            if len(groups) > 1:
                for group, keywords in sorted(groups.items(), key=_init_first):
                    group = "main" if group == "__init__" else group
                    with writer.heading(group.title()):
                        for keyword in keywords:
                            self._keyword(writer, keyword)
            else:
                keywords = next(iter(groups.values())) if groups else []
                for keyword in keywords:
                    self._keyword(writer, keyword)

    def _keyword(self, writer, keyword):
        with writer.field(keyword.name):
            fields = []
            if keyword.args:
                args = (self.escape_string(arg) for arg in keyword.args)
                fields.append(("Arguments", ", ".join(args)))
            if keyword.tags:
                fields.append(("Tags", ", ".join(keyword.tags)))
            writer.fieldlist(*fields)
            writer.raw(self.filter_docstring(keyword.doc))


class RestHtmlConverter(RestConverter):
    NAME = "rest-html"
    EXTENSION = ".rst"

    def convert(self, libdoc, output):
        formatter = htmlwriter.DocFormatter(
            libdoc.keywords, libdoc.doc, libdoc.doc_format
        )

        doc = self._raw_html(formatter.html(libdoc.doc))
        try:
            # Robot Framework < 3.2
            libdoc.doc = doc
        except AttributeError:
            # Robot Framework >= 3.2
            libdoc._doc = doc

        for init in libdoc.inits:
            init.doc = self._raw_html(formatter.html(init.doc))
        for kw in libdoc.keywords:
            kw.doc = self._raw_html(formatter.html(kw.doc))

        super().convert(libdoc, output)

    def _raw_html(self, content):
        output = [".. raw:: html", ""]
        for line in content.splitlines():
            output.append(f"   {line}")
        return "\n".join(output)
