from optparse import OptionParser
from string import whitespace
from sys import argv as _sys_argv
from sys import exit as _sys_exit
from sys import stderr as _sys_stderr

import pkg_resources

WHITESPACE = whitespace + '　'
VERSION = pkg_resources.get_distribution('suddenly').version


# TODO: verticalを実装
def get_suddenly_text(text: str) -> str:
    text = text.replace('\\n', '\n')
    lines = text.split('\n')
    len_ = max(list(map(lambda t: len(t), lines)))
    s = '＿' + '人' * (len_ + 2) + '＿' + '\n'

    for line in lines:
        line = line.strip(WHITESPACE)
        if line == '':
            continue
        s += f'＞　{line}　＜\n'

    s += '￣' + 'Y^' * (len_ + 2) + '￣'

    return s


def get_option_parser():
    usage = 'suddenly [options] [text1 text2 ...]'
    parser = OptionParser(usage=usage, version=VERSION)
    # parser.add_option(
    #     '-v',
    #     '--vertical',
    #     action='store_true',
    #     default=False,
    #     dest='vertical',
    # )
    return parser


def main(argv=_sys_argv[1:]):
    opt, texts = get_option_parser().parse_args(argv)

    if texts == []:
        print('text is not given.', file=_sys_stderr)
        _sys_exit(1)

    for text in texts:
        print(get_suddenly_text(text))
        print()


if __name__ == '__main__':
    main()
