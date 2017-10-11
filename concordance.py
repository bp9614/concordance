import re


def split_file(file: str, encoding: str = None) -> (list, set):
    with open(file, 'r', encoding=encoding) as smp_file:
        sample = smp_file.read().splitlines()

    lines = [(' '.join((str(num), line)),
              {word for word in re.split("[^a-z']", line.lower())})
             for num, line in enumerate(sample, 1) if line]
    dictionary = {word for line in sample for word
                  in re.split("[^a-z']", line.lower()) if word}

    return lines, dictionary


def exclude(dictionary: set, exclude_words: iter = None, file: str = None,
            encoding: str = None) -> None:
    if not exclude_words:
        exclude_words = set()

    if file:
        with open(file, 'r', encoding=encoding) as excluding:
            exclude_words = ({word for line in excluding.read().splitlines()
                              for word in re.split("[^a-z']", line.lower())} |
                             exclude_words)

    dictionary.difference_update(exclude_words)


def get_concordance(lines: list, dictionary: set, output:str = None) -> None:
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
    lines, dictionary = split_file('sample/greenEggs.txt')
    # exclude(dictionary, exclude_words={'a', 'of', 'the'})
    get_concordance(lines, dictionary, 'sample/greenEggsOutput.txt')


if __name__ == '__main__':
    main()
