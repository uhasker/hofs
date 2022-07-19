from hofs.common.functional import FunctionalIterator
from hofs.filelike.file_likes import File, FileIterator


class TextFile(File):
    def __init__(self, path: str, encoding: str = "utf-8"):
        super().__init__(path)

        self.encoding = encoding

    @property
    def content(self) -> str:
        """
        The content of the file.

        :return: The content.
        """
        with open(str(self.path), "r", encoding=self.encoding) as file:
            return file.read()

    @property
    def lines(self) -> FunctionalIterator[str]:
        """
        The lines of this file.

        :return: A list of lines.
        """
        with open(str(self.path), "r", encoding=self.encoding) as file:
            return FunctionalIterator(file.readlines())

    @property
    def words(self) -> FunctionalIterator[str]:
        """
        The words of this file. It is assumed that words are separated by whitespace.

        :return: A list of words.
        """
        return FunctionalIterator(self.content.split())

    @property
    def char_count(self) -> int:
        """
        The number of characters of this file.

        :return: The number of characters.
        """
        return len(self.content)

    cc = char_count

    @property
    def word_count(self) -> int:
        """
        The number of words of this file.

        :return: The number of words.
        """
        return self.words.len()

    wc = word_count

    @property
    def line_count(self) -> int:
        """
        The number of lines of this file.

        :return: The number of lines.
        """
        return self.lines.len()

    lc = line_count

    def __repr__(self) -> str:
        return f"TextFile({self.path})"


class TextFileIterator(FunctionalIterator[TextFile]):
    def map_char_count(self) -> FunctionalIterator[int]:
        """
        Map the files to their character counts.

        Note that it is implicitly assumed that all the files are valid text files.
        This function is equivalent to map(lambda file: file.text_file().char_count).

        :return: A functional iterator containing the character counts.
        """
        return self.map(lambda file: file.char_count)

    map_cc = map_char_count

    def map_word_count(self) -> FunctionalIterator[int]:
        """
        Map the files to their word counts.

        Note that it is implicitly assumed that all the files are valid text files.
        This function is equivalent to map(lambda file: file.text_file().word_count).

        :return: A functional iterator containing the word counts.
        """
        return self.map(lambda file: file.word_count)

    map_wc = map_word_count

    def map_line_count(self) -> FunctionalIterator[int]:
        """
        Map the files to their line counts.

        Note that it is implicitly assumed that all the files are valid text files.
        This function is equivalent to map(lambda file: file.text_file().line_count).

        :return: A functional iterator containing the line counts.
        """
        return self.map(lambda file: file.line_count)

    map_lc = map_line_count


# Add attributes to File & FileIterator


def text_file(self: File, encoding: str = "utf-8") -> "TextFile":
    """
    Get a TextFile object for this file.
    Note that you are responsible to ensure that the underlying file is a valid
    text file (since this is very expensive to ensure automatically). This function
    will always succeed, even if the underlying file is not a valid text file.
    However, when calling paths on the resulting TextFile object, errors will occur.
    :param encoding: The encoding to use.
    :return: The obtained TextFile object.
    """
    return TextFile(self.path, encoding)


setattr(File, "text_file", text_file)
setattr(File, "t", text_file)


def text_file_iterator(self: FileIterator) -> "TextFileIterator":
    return TextFileIterator(self.map(lambda file: file.text_file()))


setattr(FileIterator, "text_file_iterator", text_file_iterator)
setattr(FileIterator, "t", text_file_iterator)
