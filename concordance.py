import re


def parse_file(file: str, encoding: str = None) -> (list, set):
    """Parses the file for lines, words in the line, and words in the file.

    Reads the file to get every line and numbers them and combines it with a
    set of every word in that line, then creates a set of every word
    (lower case) in the file. Any blank line is removed, but they still
    contribute to the line number.
    :param file: Sample file to extract lines and words from.
    :param encoding: Character set used by the file.
    :return: A list of tuples containing each line and the words in them, and
    a set of every word in the file.
    """
    with open(file, 'r', encoding=encoding) as smp_file:
        sample = smp_file.read().splitlines()

    lines = [(' '.join((str(num), line)),
              {word for word in re.split("[^a-z']", line.lower())})
             for num, line in enumerate(sample, 1) if line]
    dictionary = {word for line in sample for word
                  in re.split("[^a-z']", line.lower()) if word}

    return lines, dictionary


def exclude(dictionary: set, exclude_words: iter = None,
            file: str = None, encoding: str = None) -> set:
    """Returns the set after removing any the given words from it.

    :param dictionary: Set of words to have words removed from.
    :param exclude_words: Iterable that contains values to remove from
    dictionary.
    :param file: File containing words to remove from dictionary.
    :param encoding: Character set used by the file.
    :return: Set of words with the given words removed from it.
    """
    if not exclude_words:
        exclude_words = set()

    if file:
        with open(file, 'r', encoding=encoding) as excluding:
            exclude_words = ({word for line in excluding.read().splitlines()
                              for word in re.split("[^a-z']", line.lower())} |
                             exclude_words)

    return dictionary - exclude_words


def exclude_update(dictionary: set, exclude_words: iter = None,
                   file: str = None, encoding: str = None) -> None:
    """Removes any instance of the given words from the set.

    :param dictionary: Set of words to have words removed from.
    :param exclude_words: Iterable that contains values to remove from
    dictionary.
    :param file: File containing words to remove from dictionary.
    :param encoding: Character set used by the file.
    """
    if not exclude_words:
        exclude_words = set()

    if file:
        with open(file, 'r', encoding=encoding) as excluding:
            exclude_words = ({word for line in excluding.read().splitlines()
                              for word in re.split("[^a-z']", line.lower())} |
                             exclude_words)

    dictionary.difference_update(exclude_words)


def get_concordance(lines: list, dictionary: set, output: str = None) -> None:
    """Creates the concordance and outputs it to a file or the terminal.

    :param lines: A list of sentences along with each word in that line.
    :param dictionary: A set of words to generate a concordance from the lines.
    :param output: Outputs the results to a file if given or the terminal if
    not.
    """
    if output:
        output = open(output, 'w')

    print('\n'.join(line for line,_ in lines), end='\n\n', file=output)
    for word in sorted(dictionary):
        print(''.join((word, ':')), file=output)
        print('\n'.join(line for line, line_words in lines if word
                        in line_words), end='\n\n', file=output)

    if output:
        output.close()


def main():
    lines, dictionary = parse_file('sample/greenEggs.txt')
    # exclude_update(dictionary, file='sample/ExcludeTheseWords.txt')
    get_concordance(lines, dictionary, 'sample/greenEggsOutput.txt')


if __name__ == '__main__':
    main()
