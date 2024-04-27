"""
Avril Mauro & Katelyn Donn
DS 3500 Homework 3 NLP App
February 25, 2023
"""

from nlp_visualizer import TextProcessor
import random as rand
import nlp_parsers as par
from exception import OutOfRangeError


def validate_num(num):
    """ raise errors if num is out of range """
    try:
        assert int(num) <= 10, 'Cannot analyze more than 10 files at a time'
        assert int(num) >= 1, 'Must select at least 1 file'

    except AssertionError as ae:
        raise OutOfRangeError(num, msg=str(ae))

    else:
        pass


def main():
    # initialize the Text Processor framework class
    tp = TextProcessor()

    # import the file name
    file = 'tedtalks.csv'

    try:
        # select a user specified number of files (random)
        num = int(input('How many ted talks do you want to analyze today?\n'))
        validate_num(num)

        # generate text indices to extract from csv
        idx0 = rand.randint(1, 2462)
        idx1 = idx0 + num
        print(f'\nLoading {num} Ted Talks...')

        # load the texts
        for i in range(idx0, idx1):
            tp.load_text(file, parser=par.csv_parser, index=i, p_type='csv', url_header='https://www.ted.com/talks/')

        print('\n---------\nComplete!\n---------\n')

        # ask the user to pick a visualization
        visual = int(input('What visualization would you like to see?\n'
                           '\t1. Sankey Diagram of Most Common k Words\n'
                           '\t2. Barcharts of Most Common k Words of Each File\n'
                           '\t3. Sunburst Diagram of Longest Word from Each File\n'
                           '\t4. All of the above.\n'))

        # display the visualizations
        tp.visualize(visual)

    except OutOfRangeError as er:
        # if inputs are out of range, restart the program
        print('\n---------\nError:', str(er), '\n---------\n',
              '\nStarting over ....\n')
        main()


if __name__ == "__main__":
    main()
