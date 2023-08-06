import re
import sys
from collections import namedtuple
from enum import IntFlag
from pathlib import Path
from typing import Iterable, List, Generator, Union, Match, Any, Optional, Mapping, \
    Callable

__version__ = "0.5b1"
__all__ = [
    "doctest_iter_print",
    "doctest_print",
    "doctest_print_list",
    "remove_trailing_whitespaces",
    "repr_posix_path",
]

FIND_WHITESPACES = re.compile(r"[\s]+")
WhiteSpaceBlockPosition = namedtuple("WhiteSpaceBlockPosition", "start end")
WhiteSpaceBlockPositions = Iterable[WhiteSpaceBlockPosition]
BlockSectionPosition = namedtuple("BlockSectionPosition", "start end")
BlockSectionPositions = Iterable[BlockSectionPosition]
LINE_BREAK = "\n"


class Platforms(IntFlag):
    WINDOWS = 0
    LINUX = 1

    @classmethod
    def get_current_platform(cls):
        if sys.platform in ["win32"]:
            return Platforms.WINDOWS
        if sys.platform in ["linux"]:
            return Platforms.LINUX


_current_platform = Platforms.get_current_platform()
_REPLACE_TRAILING_WHITESPACE = re.compile("[\s]+$", re.MULTILINE)


APath = Union[str, Path]


def remove_trailing_whitespaces(text: str) -> str:
    """
    Removes trailing whitespaces from the text.

    Args:
        text(str):
            Text from which trailing whitespaces should be removed.

    Returns:
        str

    Examples:
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\n   "
        >>> remove_trailing_whitespaces(sample_text)
        'A sample text with\\n trailing whitespaces.'
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\nEnd. "
        >>> remove_trailing_whitespaces(sample_text)
        'A sample text with\\n trailing whitespaces.\\nEnd.'

    """
    return _REPLACE_TRAILING_WHITESPACE.sub("", text)


_ADDS_AN_IDENT_AT_SECOND_LINE = re.compile(LINE_BREAK, re.MULTILINE)


def _indent_block(paragraph: str, indent: str) -> str:
    """
    Indents a multiline paragraph.

    Args:
        paragraph(str):
            The paragraph which should be indented.

        indent(Optional[str]):
            Custom indentation.

    Returns:
        str

    Test:
        >>> print(_indent_block("a\\nparagraph", indent="--> "))
        --> a
        --> paragraph
    """
    if indent is None:
        indent = "    "
    return _ADDS_AN_IDENT_AT_SECOND_LINE.sub(LINE_BREAK + indent, indent + paragraph)


_windows_drive_letter_matcher = re.compile("^([a-z]):")


def _replace_windows_drive_letter(drive_letter_match: Match) -> str:
    """
    Replaces the windows drive letter with a forward slash encapsulation.

    Notes:
        Is used by :func:`repr_posix_path` using :func:`re.sub`.

    Args:
        drive_letter_match(Match):
            The regular expression matched drive letter.

    Returns:
        str
    """
    drive_letter = drive_letter_match.group(1)
    return "/{}".format(drive_letter)


def repr_posix_path(any_path: Union[str, Path]) -> str:
    """
    Represents the path on a Windows machine as a Posix-Path representation
    turning back slashes to forward slashes.

    Examples:
        >>> repr_posix_path("c:\\\\a\\\\path")
        '/c/a/path'
        >>> repr_posix_path(".\\\\a\\\\path")
        './a/path'
        >>> repr_posix_path(".\\\\a\\\\path")
        './a/path'

    Args:
        any_path(str, Path):
            Any type of path representation.

    Returns:
        str
    """
    busted_windows_drive_letter = _windows_drive_letter_matcher.sub(
        _replace_windows_drive_letter, str(any_path)
    )
    return str(busted_windows_drive_letter).replace("\\", "/")


def strip_base_path(base_path_to_strip: APath, path_to_show: APath) -> str:
    """
    Strips the given *base path* from the *path to show* and performing
    :func:`repr_posix_path` on the result.

    Examples:
        >>> strip_base_path("/a/root/path", "/a/root/path/some/place")
        '... /some/place'
        >>> strip_base_path("\\\\a\\\\root\\\\path", "/a/root/path/some/place")
        '... /some/place'
        >>> strip_base_path("/a/root/path", "\\\\a\\\\root\\\\path\\\\some\\\\place")
        '... /some/place'

    Args:
        base_path_to_strip:
            The base path, which should be removed from the view.

        path_to_show:
            The path which is going to be viewed.

    Returns:
        str
    """
    if _current_platform == Platforms.WINDOWS:
        path_to_show = str(path_to_show).replace("/", "\\")
        base_path_to_strip = str(base_path_to_strip).replace("/", "\\")
    elif _current_platform == Platforms.LINUX:
        path_to_show = str(path_to_show).replace("\\", "/")
        base_path_to_strip = str(base_path_to_strip).replace("\\", "/")
    stripped_path = str(path_to_show).replace(str(base_path_to_strip), "... ")
    return repr_posix_path(stripped_path)


def get_positions_of_whitespace_blocks(text: str) -> WhiteSpaceBlockPositions:
    """

    Args:
        text(str):

    Examples:
        >>> sample_text = "This is a    test string.    "
        >>> white_space_positions = get_positions_of_whitespace_blocks(sample_text)
        >>> for position in white_space_positions:
        ...     print(position)
        WhiteSpaceBlockPosition(start=4, end=5)
        WhiteSpaceBlockPosition(start=7, end=8)
        WhiteSpaceBlockPosition(start=9, end=13)
        WhiteSpaceBlockPosition(start=17, end=18)
        WhiteSpaceBlockPosition(start=25, end=29)
        >>> get_positions_of_whitespace_blocks("")
        []
        >>> sample_text = str(list(iter("abcde")))
        >>> white_space_positions = get_positions_of_whitespace_blocks(sample_text)
        >>> for position in white_space_positions:
        ...     print(position)
        WhiteSpaceBlockPosition(start=5, end=6)
        WhiteSpaceBlockPosition(start=10, end=11)
        WhiteSpaceBlockPosition(start=15, end=16)
        WhiteSpaceBlockPosition(start=20, end=21)

    Returns:
        WhiteSpaceBlockPositions
    """
    assert text is not None, "`text` cannot be None."
    return [
        WhiteSpaceBlockPosition(match.start(), match.end())
        for match in FIND_WHITESPACES.finditer(text)
    ]


def find_section_positions_at_whitespaces(
    text: str, maximum_line_width: int
) -> List[int]:
    """
    Finds the positions of sections. Whitespaces marks the used section positions.

    Args:
        text(str):
            The text in which

        maximum_line_width(int):
            The maximum linewidth.

    Returns:
        List[int]

    Examples:
        >>> sample_text = str(list(range(60)))
        >>> # section_positions = find_section_positions_at_whitespaces(sample_text, 40)
        >>> # for section in section_positions:
        #...     print(section)
        BlockSectionPosition(start=0, end=42)
        BlockSectionPosition(start=43, end=86)
        BlockSectionPosition(start=87, end=130)
        BlockSectionPosition(start=131, end=174)
        BlockSectionPosition(start=175, end=218)
        BlockSectionPosition(start=219, end=230)
        >>> sample_text = str(list(iter("abcde")))
        >>> section_positions = find_section_positions_at_whitespaces(sample_text, 40)
        >>> for section in section_positions:
        ...     print(section)
        BlockSectionPosition(start=0, end=25)

    """
    assert isinstance(
        text, (str, bytes, bytearray)
    ), "text must be a string or byte-like."
    full_text_fits_in_one_line = len(text) < maximum_line_width
    if full_text_fits_in_one_line:
        return [BlockSectionPosition(0, len(text))]

    block_positions = get_positions_of_whitespace_blocks(text)
    block_sections = []
    current_section_start = 0
    for block_position in block_positions:
        try:
            start_position, end_position = block_position
        except ValueError:
            raise ValueError("A block position must be a 2 item tuple of start & end.")

        current_relative_block_end = start_position - current_section_start
        found_section_with_adequate_width = (
            current_relative_block_end >= maximum_line_width
        )
        if found_section_with_adequate_width:
            block_sections.append(
                BlockSectionPosition(current_section_start, start_position)
            )
            current_section_start = end_position

    did_found_block_sections = len(block_sections) > 0
    if did_found_block_sections:
        last_section_end = block_sections[-1][1]
        text_length = len(text)
        if last_section_end < text_length:
            block_sections.append(
                BlockSectionPosition(current_section_start, text_length)
            )

    return block_sections


def iter_split_text(
    text: str, block_sections: BlockSectionPositions
) -> Generator[str, None, None]:
    """
    Splits a texts by :attribute:`BlockSectionPositions`.

    Args:
        text(str):
            Text which should be split.

        block_sections(BlockSectionPositions):
            Positions by which to split.

    Yields:
        str

    Examples:
        >>> sample_text = str(list(range(60)))
        >>> block_positions = find_section_positions_at_whitespaces(sample_text, 40)
        >>> for line in iter_split_text(sample_text, block_positions):
        ...     print(line)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
        13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
        35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
        46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
        57, 58, 59]
    """
    for start_position, end_position in block_sections:
        yield text[start_position:end_position]


def break_lines_at_whitespaces(text: str, maximum_line_width: int) -> str:
    """
    Breaks lines at whitespaces.

    Notes:
        Within this implementation the linewidth is not broken by block
        text elements, which exceeds the maximum line width.

    Args:
        text(str):
            Text which should be broken into lines with an maximum line width.

        maximum_line_width(int):
            The maximum line width.

    Returns:
        str

    Examples:
        >>> sample_text = str(list(range(80)))
        >>> result_as_block = break_lines_at_whitespaces(sample_text, 72)
        >>> print(result_as_block)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
        40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
        59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
        78, 79]
        >>> small_list = str(list(iter("abcdefghij")))
        >>> result_as_block = break_lines_at_whitespaces(small_list, 72)
        >>> print(result_as_block)
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    """
    section_positions = find_section_positions_at_whitespaces(
        text=text, maximum_line_width=maximum_line_width
    )
    return LINE_BREAK.join(iter_split_text(text, block_sections=section_positions))


def doctest_print_list(object_to_print: Iterable, line_width: int = 72):
    """
    Print the content of an Iterable breaking the resulting string at whitespaces.

    Args:
        object_to_print(Any):
            The object of which a block should be printed.

        line_width(int):
            The line width on which the resulting text is broken at whitespaces.

    Examples:
        >>> sample_object = list(range(80))
        >>> doctest_print_list(sample_object)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
        40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
        59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
        78, 79]
        >>> small_list = list(iter("abcdefghij"))

    """
    string_representation = str(object_to_print)
    prepared_print_representation = break_lines_at_whitespaces(
        string_representation, maximum_line_width=line_width
    )
    print(prepared_print_representation)


def doctest_print(
    anything_to_print: Any,
    max_line_width: Optional[int] = 0,
    indent: Optional[str] = None,
):
    """
    The general printing method for doctests.

    Notes:
        The argument *max_line_width* will break lines a whitespaces. If the
        single text exceeds the maximum linewidth it will not be broken within
        this implementation.

    Args:
        anything_to_print(Any):
            Anything which will be converted into a string and postprocessed,
            with default methods.

        max_line_width(Optional[int]):
            Sets the maximum linewidth of the print.

        indent(str):
            Additional indentation added to the docstring.

    Examples:
        >>> test_text = (
        ...     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed"
        ...     " do eiusmod tempor      incididunt ut labore et dolore magna"
        ...     " aliqua. Ut enim ad  minim veniam, quis nostrud exercitation"
        ...     " ullamco laboris  nisi ut  aliquip  ex ea commodo consequat."
        ... )
        >>> doctest_print(test_text[:84])
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
        >>> doctest_print(test_text, max_line_width=60)
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
        do eiusmod tempor      incididunt ut labore et dolore magna aliqua.
        Ut enim ad  minim veniam, quis nostrud exercitation ullamco laboris
        nisi ut  aliquip  ex ea commodo consequat.
        >>> doctest_print(test_text, max_line_width=60, indent="    ")
            Lorem ipsum dolor sit amet, consectetur adipiscing elit,
            sed do eiusmod tempor      incididunt ut labore et dolore
            magna aliqua. Ut enim ad  minim veniam, quis nostrud exercitation
            ullamco laboris  nisi ut  aliquip  ex ea commodo consequat.
        >>> small_list = list(iter("abcdefghij"))
        >>> doctest_print(small_list)
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        >>> doctest_print(small_list, max_line_width=60)
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    """
    string_representation = str(anything_to_print)
    prepared_print_representation = remove_trailing_whitespaces(string_representation)
    if indent is not None:
        indent = str(indent)
        indent_count = len(indent)
    else:
        indent_count = 0
    if max_line_width > 0:
        prepared_print_representation = break_lines_at_whitespaces(
            prepared_print_representation,
            maximum_line_width=max_line_width - indent_count,
        )
    if indent is not None:
        prepared_print_representation = _indent_block(
            paragraph=prepared_print_representation, indent=indent
        )
    print(prepared_print_representation)


def doctest_iter_print(
    iterable_to_print: Union[Mapping, Iterable],
    max_line_width: Optional[int] = 0,
    indent: Optional[str] = None,
    edits_item: Optional[Callable[[Any], Any]]=None,
):
    """
    Prints the first level of the iterable or mapping.

    Args:
        iterable_to_print(Union[Mapping, Iterable]):
            A Mapping or Iterable which first level will be iterated and printed.

        max_line_width(Optional[int]):
            Sets the maximum linewidth of the print.

        indent(Optional[str]):
            Additional indentation. The items of mappings will be indented
            additionally.

        edits_item(Callable[[Any], Any]):
            A callable which takes the 1st level item and returing the
            state, which should be printed.

    Examples:
        >>> sample_mapping = {"a": "mapping  ", "with": 3, "i": "tems  "}
        >>> doctest_iter_print(sample_mapping)
        a:
          mapping
        with:
          3
        i:
          tems
        >>> doctest_iter_print(sample_mapping, indent="..")
        ..a:
        ....mapping
        ..with:
        ....3
        ..i:
        ....tems
        >>> doctest_iter_print([1, 2, {"a": "mapping  ", "with": 3, "i": "tems  "}])
        1
        2
        {'a': 'mapping  ', 'with': 3, 'i': 'tems  '}
        >>> doctest_iter_print(["abc", "abcd", "abcde"], edits_item=lambda x: x[:3])
        abc
        abc
        abc
        >>> doctest_iter_print({"edit": 1, "item": 2}, edits_item=lambda x: x**2)
        edit:
          1
        item:
          4
    """
    edit_item_before_print = edits_item is not None
    if isinstance(iterable_to_print, Mapping):
        if indent is None:
            mapping_indent = "  "
        else:
            mapping_indent = str(indent) * 2
        for key in iterable_to_print:
            item_to_print = iterable_to_print[key]
            if edit_item_before_print:
                prepared_item = edits_item(item_to_print)
            else:
                prepared_item = item_to_print
            doctest_print(
                "{}:".format(str(key)), max_line_width=max_line_width, indent=indent
            )
            doctest_print(
                prepared_item, max_line_width=max_line_width, indent=mapping_indent
            )
    elif isinstance(iterable_to_print, Iterable):
        for item_to_print in iterable_to_print:
            if edit_item_before_print:
                prepared_item = edits_item(item_to_print)
            else:
                prepared_item = item_to_print
            doctest_print(prepared_item, max_line_width=max_line_width, indent=indent)
