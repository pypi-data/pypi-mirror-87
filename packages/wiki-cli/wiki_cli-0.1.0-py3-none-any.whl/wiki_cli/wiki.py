#!/usr/bin/env python3
"""Lookup words on wikipedia and print their extract."""

# pylint: disable=R0201
# pylint: disable=R0911
# pylint: disable=R1705

import json
import multiprocessing
import multiprocessing.pool
import subprocess
import sys
import typing

import requests
import termcolor
from bs4 import BeautifulSoup

URL = "https://{lang}.wikipedia.org/api/rest_v1/page/summary/{word}"
LANGS = ["de", "en"]


class Wiki:
    """Cli class."""

    def __init__(self, word: str):
        self.session = requests.Session()
        self.word = word
        self.pool = multiprocessing.pool.ThreadPool(
            max(multiprocessing.cpu_count() - 2, len(LANGS))
        )

    def run(self):
        """Run lookups in multiple languages in parallel."""
        results = self.pool.map(self.lookup, LANGS)
        self.pool.close()
        self.pool.join()
        errs = [res for res in results if isinstance(res, Exception)]
        res = [res for res in results if isinstance(res, str)]

        if errs:
            print("There have been errors:")

            for err in errs:
                print(err, file=sys.stderr)

        if not res:
            print("Nothing found", file=sys.stderr)
        else:
            print(res[0])

    def lookup(self, lang: str) -> typing.Union[str, Exception, None]:
        """Lookup the word in ``lang``."""
        response = self.session.get(URL.format(lang=lang, word=self.word))
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 404:
                return None
            else:
                return err

        try:
            data = response.json()
            #  print(data)
        except json.JSONDecodeError as err:
            return err

        try:
            if data["type"] == "standard":
                return self.format_standard_article(data)
            elif data["type"] == "disambiguation":
                return self.format_disambiguation_article(data)
            else:
                return ValueError(f'Unknown article type {data["type"]}')
        except KeyError as err:
            return err

    def _format_title(self, data) -> str:
        return termcolor.colored(data["title"], attrs=["bold"]) + "\n\n"

    def _format_link(self, data) -> str:
        return "\n\n" + termcolor.colored(
            data["content_urls"]["desktop"]["page"],
            color="blue",
            attrs=["underline"],
        )

    def _format_img(self, data) -> str:
        img = self.get_img(data)

        if img:
            return img + "\n"
        else:
            #  termcolor.cprint('No Image', color='grey', file=sys.stderr)
            return ""

    def _html_formatter_walk(self, root, prefix="") -> str:
        if not root:
            return ""
        elif root.name in (
            "html",
            "body",
            "span",
            "[document]",
        ):
            return "".join(self._html_formatter_walk(bit) for bit in root).strip()
        elif root.name == "p":
            return (
                "".join(self._html_formatter_walk(bit) for bit in root) + f"\n{prefix}"
            )
        elif root.name in ("b", "strong"):
            return termcolor.colored(
                "".join(self._html_formatter_walk(bit) for bit in root),
                attrs=["bold"],
            )
        elif root.name in ("i", "em"):
            return (
                "\x1b[3m"
                + "".join(self._html_formatter_walk(bit, prefix=prefix) for bit in root)
                + "\x1b[0m"
            )
        elif root.name == "ul":
            return "\n" + "".join(
                self._html_formatter_walk(bit, prefix=prefix + "  ") for bit in root
            )
        elif root.name == "br":
            return f"\n{prefix}"
        elif root.name == "li":
            return (
                f"{prefix}- "
                + "".join(
                    self._html_formatter_walk(bit, prefix=prefix + "  ") for bit in root
                )
                + "\n"
            )
        elif root.name is None:
            if str(root) == "\n":
                return ""

            return str(root).replace("\n", f"\n{prefix}")
        else:
            return root.string

    def _format_extract_html(self, data) -> str:
        extract_html = data["extract_html"]
        soup = BeautifulSoup(extract_html, parser="html.parser", features="lxml")

        return self._html_formatter_walk(soup).strip()

    def format_disambiguation_article(self, data) -> str:
        """Format a disambiguation article."""
        ret = self._format_title(data)
        ret += self._format_extract_html(data)
        ret += self._format_link(data)

        return ret

    def format_standard_article(self, data) -> str:
        """Format a standard article."""
        ret = self._format_img(data)
        ret += self._format_title(data)
        ret += self._format_extract_html(data)
        ret += self._format_link(data)

        return ret

    def get_img(self, data: typing.Dict[str, typing.Any]) -> typing.Optional[str]:
        """Download image from wikipedia and convert it to term string."""
        try:
            img_url = data["thumbnail"]["source"]
        except KeyError:
            #  print('No thumbnail', err)

            return None

        ret = self.session.get(img_url)
        try:
            ret.raise_for_status()
        except requests.exceptions.HTTPError:
            #  print('Could not fetch image', err)

            return None

        try:
            proc = subprocess.Popen(
                ["catimg", "-H", "20", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as err:
            print(err, file=sys.stderr)

            return None

        stdout, stderr = proc.communicate(input=ret.content)

        if stderr and stderr.strip():
            print(stderr.strip(), file=sys.stderr)

            return None

        return stdout.decode(sys.stdout.encoding)


def main():
    """Do it."""
    word = sys.argv[-1]
    wiki = Wiki(word)
    wiki.run()


if __name__ == "__main__":
    main()
