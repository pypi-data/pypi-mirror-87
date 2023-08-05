"""Contains the parser for OSIS format files."""

import os
from functools import lru_cache

try:
    from defusedxml import ElementTree
except ModuleNotFoundError:
    from xml.etree import ElementTree

from pythonbible.bible.bible_parser import BibleParser, sort_paragraphs
from pythonbible.bible.osis.constants import BOOK_IDS, get_book_by_id
from pythonbible.errors import InvalidVerseError
from pythonbible.verses import get_book_chapter_verse, get_verse_id

XML_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "versions")

XPATH_BOOK = ".//xmlns:div[@osisID='{}']"
XPATH_BOOK_TITLE = f"{XPATH_BOOK}/xmlns:title"
XPATH_VERSE = ".//xmlns:verse[@osisID='{}.{}.{}']"
XPATH_VERSE_PARENT = f"{XPATH_VERSE}/.."


class OSISParser(BibleParser):
    """
    Parse files containing scripture text in the OSIS format.

    OSISParser extends BibleParser and contains all the functionality necessary
    to parse XML files that are in the OSIS format.
    """

    def __init__(self, version):
        """
        Initialize the OSIS parser.

        Set the version, the element tree from the appropriate version XML file,
        and the namespaces.

        :param version:
        """
        super(OSISParser, self).__init__(version)

        self.tree = ElementTree.parse(
            os.path.join(XML_FOLDER, f"{self.version.value.lower()}.xml")
        )
        self.namespaces = {"xmlns": _get_namespace(self.tree.getroot().tag)}

    @lru_cache(maxsize=None)
    def get_book_title(self, book):
        """
        Given a book, return the full title for that book from the XML file.

        :param book:
        :return: the full title string
        """
        book_title_element = self._get_book_title_element(book)
        return book_title_element.text

    @lru_cache(maxsize=None)
    def get_short_book_title(self, book):
        """
        Given a book, return the short title for that book from the XML file.

        :param book:
        :return: the short title string
        """
        book_title_element = self._get_book_title_element(book)
        return book_title_element.get("short")

    @lru_cache(maxsize=None)
    def _get_book_title_element(self, book):
        xpath = XPATH_BOOK_TITLE.format(BOOK_IDS.get(book))
        return self.tree.find(xpath, namespaces=self.namespaces)

    def get_scripture_passage_text(self, verse_ids, **kwargs):
        """
        Get the scripture passage for the given verse ids.

        Given a list of verse ids, return the structured scripture text passage
        organized by book, chapter, and paragraph.

        If the include_verse_number keyword argument is True, include the verse
        numbers in the scripture passage; otherwise, do not include them.

        :param verse_ids:
        :param kwargs
        :return: an OrderedDict(Book, OrderedDict(int, list(string)))
        """
        if verse_ids is None or len(verse_ids) == 0:
            return None

        # Sort the verse ids and the convert it into a tuple so it's hashable
        verse_ids.sort()
        verse_ids = tuple(verse_ids)

        # keyword arguments
        include_verse_number = kwargs.get("include_verse_number", True)

        return self._get_scripture_passage_text_memoized(
            verse_ids, include_verse_number
        )

    @lru_cache(maxsize=None)
    def _get_scripture_passage_text_memoized(self, verse_ids, include_verse_number):
        paragraphs = _get_paragraphs(
            self.tree,
            self.namespaces,
            verse_ids,
            include_verse_number,
        )

        return None if paragraphs == [] else sort_paragraphs(paragraphs)

    def get_verse_text(self, verse_id, **kwargs):
        """
        Get the scripture text for the given verse id.

        Given a verse id, return the string scripture text passage for that verse.

        If the include_verse_number keyword argument is True, include the verse
        numbers in the scripture passage; otherwise, do not include them.

        :param verse_id:
        :param kwargs:
        :return:
        """
        if verse_id is None:
            raise InvalidVerseError("Verse id cannot be None.")

        # keyword arguments
        include_verse_number = kwargs.get("include_verse_number", True)

        return self._get_verse_text_memoized(verse_id, include_verse_number)

    @lru_cache(maxsize=None)
    def _get_verse_text_memoized(self, verse_id, include_verse_number):
        paragraphs = _get_paragraphs(
            self.tree,
            self.namespaces,
            tuple([verse_id]),
            include_verse_number,
        )
        verse_text = ""

        for chapters in paragraphs.values():
            for chapter_paragraphs in chapters.values():
                verse_text = chapter_paragraphs[0]
                break

        return verse_text


@lru_cache(maxsize=None)
def _get_namespace(tag):
    return tag[tag.index("{") + 1 : tag.index("}")]


@lru_cache(maxsize=None)
def _strip_namespace_from_tag(tag):
    return tag.replace(_get_namespace(tag), "").replace("{", "").replace("}", "")


def _get_paragraphs(tree, namespaces, verse_ids, include_verse_number):
    current_verse_id = verse_ids[0]
    book, chapter, verse = get_book_chapter_verse(current_verse_id)
    paragraph_element = tree.find(
        XPATH_VERSE_PARENT.format(BOOK_IDS.get(book), chapter, verse), namespaces
    )
    paragraphs, current_verse_id = _get_paragraph_from_element(
        paragraph_element,
        verse_ids,
        current_verse_id,
        include_verse_number,
    )
    current_verse_index = verse_ids.index(current_verse_id) + 1
    paragraph_dictionary = {}

    if current_verse_index < len(verse_ids):
        paragraph_dictionary = _get_paragraphs(
            tree,
            namespaces,
            verse_ids[current_verse_index:],
            include_verse_number,
        )

    book_dictionary = paragraph_dictionary.get(book)

    if book_dictionary is None:
        book_dictionary = {}

    chapter_list = book_dictionary.get(int(chapter))

    if chapter_list is None:
        chapter_list = []

    paragraphs.extend(chapter_list)
    book_dictionary[int(chapter)] = paragraphs
    paragraph_dictionary[book] = book_dictionary

    return paragraph_dictionary


@lru_cache(maxsize=None)
def _get_paragraph_from_element(
    paragraph_element,
    verse_ids,
    current_verse_id,
    include_verse_number,
):
    new_current_verse_id = current_verse_id
    paragraphs = []
    paragraph = ""
    skip_till_next_verse = False

    for child_element in list(paragraph_element):
        (
            child_paragraph,
            skip_till_next_verse,
            new_current_verse_id,
        ) = _handle_child_element(
            child_element,
            verse_ids,
            skip_till_next_verse,
            new_current_verse_id,
            include_verse_number,
        )

        if len(child_paragraph) == 0:
            continue

        if len(paragraph) > 0 and not paragraph.endswith(" "):
            paragraph += " "

        paragraph += child_paragraph

    paragraphs.append(clean_paragraph(paragraph))
    return paragraphs, new_current_verse_id


@lru_cache(maxsize=None)
def _handle_child_element(
    child_element,
    verse_ids,
    skip_till_next_verse,
    current_verse_id,
    include_verse_number,
):
    tag = _strip_namespace_from_tag(child_element.tag)

    if tag == "verse":
        return _handle_verse_tag(
            child_element,
            verse_ids,
            skip_till_next_verse,
            current_verse_id,
            include_verse_number,
        )

    if tag in ["w", "transChange"] and not skip_till_next_verse:
        return (
            _get_element_text_and_tail(child_element),
            skip_till_next_verse,
            current_verse_id,
        )

    if tag in ["rdg"] and not skip_till_next_verse:
        return (
            _get_element_text(child_element),
            skip_till_next_verse,
            current_verse_id,
        )

    if tag in ["q", "note"] and not skip_till_next_verse:
        paragraph = ""

        if tag == "q":
            paragraph += _get_element_text_and_tail(child_element)

        new_current_verse_id = current_verse_id

        for grandchild_element in list(child_element):
            (
                grandchild_paragraph,
                skip_till_next_verse,
                new_current_verse_id,
            ) = _handle_child_element(
                grandchild_element,
                verse_ids,
                skip_till_next_verse,
                current_verse_id,
                include_verse_number,
            )

            paragraph += grandchild_paragraph

        return clean_paragraph(paragraph), skip_till_next_verse, new_current_verse_id

    return "", skip_till_next_verse, current_verse_id


@lru_cache(maxsize=None)
def _handle_verse_tag(
    child_element,
    verse_ids,
    skip_till_next_verse,
    current_verse_id,
    include_verse_number,
):
    paragraph = ""
    osis_id = child_element.get("osisID")

    if osis_id is None:
        return paragraph, skip_till_next_verse, current_verse_id

    book_id, chapter, verse = child_element.get("osisID").split(".")
    book = get_book_by_id(book_id)
    verse_id = get_verse_id(book, int(chapter), int(verse))

    if verse_id in verse_ids:
        if skip_till_next_verse:
            skip_till_next_verse = False

            if current_verse_id is not None and verse_id > current_verse_id + 1:
                paragraph += "... "

        if include_verse_number:
            paragraph += f"{verse}. "

        paragraph += _get_element_text_and_tail(child_element)

        return paragraph, skip_till_next_verse, verse_id

    skip_till_next_verse = True
    return paragraph, skip_till_next_verse, current_verse_id


@lru_cache(maxsize=None)
def _get_element_text_and_tail(element):
    return _get_element_text(element) + _get_element_tail(element)


@lru_cache(maxsize=None)
def _get_element_text(element):
    return element.text.replace("\n", " ") if element.text else ""


@lru_cache(maxsize=None)
def _get_element_tail(element):
    return element.tail.replace("\n", " ") if element.tail else ""


@lru_cache(maxsize=None)
def clean_paragraph(paragraph):
    cleaned_paragraph = paragraph.replace("¶", "").replace("  ", " ")
    cleaned_paragraph = cleaned_paragraph.strip()
    return cleaned_paragraph
