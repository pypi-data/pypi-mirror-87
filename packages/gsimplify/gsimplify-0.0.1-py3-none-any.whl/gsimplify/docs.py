import collections
import pprint
from typing import List, Optional, Tuple

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from jinja2 import Template
from pydantic import BaseModel

from simplify.typedefs import DocType, FolderType

DEPTH_LEVELS = ["TITLE", "HEADING_1", "HEADING_2", "HEADING_3", "NORMAL_TEXT"]


class Docs:
    def __init__(self, doc: DocType, creds):
        self.document = doc
        self.service = build("docs", "v1", credentials=creds)
        self.get(doc.id)
        self.document.ast = self.parse()

    def __str__(self):
        return pprint.pformat(self.document)

    def __repr__(self):
        return str(self)

    def render(self, template: Template) -> str:
        return template.render(**self.document.dict())

    def get(self, id=str) -> dict:
        """
        Grabs the document from Google Docs
        """
        self.document.content = self.service.documents().get(documentId=id).execute()
        return self.document.content

    def parse(self):
        """
        Parses document into a dict-like parse tree.
        """
        ast = self.test_parse(self.document.content.get("body").get("content"))
        self.document.title = ast[0][0]

        return ast

    def recursive_parse(self, structure: list, depth=0) -> dict:
        """
        Recursive/monadic parser.
        """
        level = DEPTH_LEVELS[depth]
        ast = collections.OrderedDict()
        pretext = []
        posttext = []
        count = 0
        for outer_count, section in enumerate(structure):
            stop_loop = True
            if "paragraph" in section:
                paragraph = section.get("paragraph")
                style = paragraph.get("paragraphStyle").get("namedStyleType")
                if style == level:
                    content = "".join(
                        [
                            elm.get("textRun").get("content")
                            for elm in paragraph.get("elements")
                        ]
                    )

                    stop_count = 0
                    for inner_count, lookahead_section in enumerate(
                        structure[count + 1 :]
                    ):
                        if "paragraph" in lookahead_section:
                            inner_style = (
                                lookahead_section.get("paragraph")
                                .get("paragraphStyle")
                                .get("namedStyleType")
                            )
                            if (
                                inner_style == style and stop_count == 0
                            ):  # first encounter of equal depth
                                stop_count = inner_count
                                stop_loop = False
                                break
                    else:
                        stop_count = len(structure)

                    if count:
                        pretext = self.recursive_parse(structure[:count], depth=depth)
                    else:
                        pretext = collections.OrderedDict()

                    if count + 1 - stop_count:
                        posttext = self.recursive_parse(
                            structure[count + 1 : stop_count], depth=depth
                        )
                    else:
                        posttext = collections.OrderedDict()

                    ast[content] = (pretext, posttext)

                    if stop_loop:  # done
                        break
                    else:  # next elements are equal depth
                        del structure[:stop_count]
                        count = 0
                        continue  # skip the count incrementer
            count += 1
        else:
            if depth + 1 < len(DEPTH_LEVELS):
                ast[""] = (
                    collections.OrderedDict(),
                    self.recursive_parse(structure, depth=depth + 1),
                )
        return ast

    def test_parse(self, structure: list) -> List[Tuple[str, List]]:
        ast = []

        for section in structure:
            if "paragraph" not in section:
                continue

            paragraph = section.get("paragraph")
            style: str = paragraph.get("paragraphStyle").get("namedStyleType")

            content = "".join(
                [elm.get("textRun").get("content") for elm in paragraph.get("elements")]
            )

            depth_level = DEPTH_LEVELS.index(style)

            relative_depth_level = depth_level
            ast_slice = ast
            while relative_depth_level > 0:
                relative_depth_level -= 1
                if len(ast_slice) == 0:
                    ast_slice.append((None, []))
                ast_slice = ast_slice[-1][1]

            ast_slice.append((content, []))

        return ast
