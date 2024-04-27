"""
Avril Mauro & Katelyn Donn
DS 3500 Core framework class for NLP Comparative Analysis
February 25, 2023
"""

from collections import Counter, defaultdict
from nltk.corpus import stopwords
from plotly.subplots import make_subplots
from utils import sort_limit_dict
from exception import OutOfRangeError
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sankey as sk
import itertools
import string
import nltk

# download needed for first run
nltk.download('stopwords')


class TextProcessor:
    filecount = 0

    def __init__(self):
        """ manage data about different texts that are registered in the framework """
        self.data = defaultdict(dict)  # our data extracted from text files

    @staticmethod
    def _default_parser(filename):
        """ reads a text file, removes punctuation, spaces, and capital letters;
        generates a results dictionary which records word count for each word,
        total number of words in the file, and the length of each word """
        with open(filename) as f:
            lines = f.readlines()
            lines = [text.replace("\n", '') for text in lines]
            words = str(lines).translate(str.maketrans('', '', string.punctuation)).lower().split(' ')
            stop_words = TextProcessor.load_stop_words(stopwords.words('english'), words)
            words = [w for w in words if w not in stop_words]
            f.close()

        results = {'word_count': dict(Counter(words)),
                   'num_words': len(words),
                   'word_length': dict(zip([w for w in words], [len(w) for w in words]))}

        return results

    def _save_results(self, label, results):
        """ Integrate parsing results into internal state
        label: unique label for a text file that we parsed
        results: the data extracted from the file as a dictionary attribute-->raw data
        """
        self.data[label] = results

    def load_text(self, filename, index=None, label=None, parser=None, p_type=None, url_header=None):
        """ Register a document with the framework """
        if parser is None:  # do default parsing of standard .txt file
            results = TextProcessor._default_parser(filename)

        elif p_type == 'csv':
            results, label = parser(filename, index, url_header)

        else:
            results = parser(filename)

        if label is None:
            label = filename

        # Save / integrate the data we extracted from the file
        # into the internal state of the framework
        self.filecount += 1
        self._save_results(label, results)

    def load_stop_words(stopfile, word_list):
        """ generates a list of common or stop words found in a list of words """

        stop_list = ['like', 'applause', 'laughter', 'us', 'one', 'going', 'really',
                     'much', 'also', 'got', 'would', 'said']

        # identifies words in the text file that exist in stopfile, adds to stop list
        for word in word_list:
            if word in stopfile:
                stop_list.append(word)

        return set(stop_list)

    def intersect_words(self):
        """ finds the words present in all text files """

        # create a list of sets for all the words in each file
        set_list = []
        for file, results in self.data.items():
            set_list.append(set(results['word_count'].keys()))

        # intersect each set onto itself until none are left
        idx = 0
        setA = set_list[0]
        while idx < (len(set_list) - 1):
            setB = setA.intersection(set_list[idx + 1])
            setA = setB
            idx += 1

        # return set of words present in all text files
        return setA

    def top_k(self, k=3):
        """finds a user specified amount of most common words
            that are present in all text files within self.data """

        try:
            # identify the words that appear in all files
            inter_words = self.intersect_words()

            # cannot output more words than what already exists in the intersection
            assert k <= len(inter_words), 'k is too large'
            assert type(k) == int, 'k must be a positive integer'

        except AssertionError as ae:
            raise OutOfRangeError(k, str(ae))

        else:
            inter_counts = defaultdict(lambda: 0)
            for w in inter_words:
                for file, results in self.data.items():
                    inter_counts[w] += results['word_count'][w]

            # find top k words across all files
            top_k = sort_limit_dict(inter_counts, limit=k)

            return top_k

    def numwords_barchart(self, k=5):
        """ generates subplots showing a user specified amount of
            most common words for each file as bar charts """

        try:
            assert k <= 20, 'too many words selected, please select less than 20'

        except AssertionError as ae:
            raise OutOfRangeError(k, str(ae))

        else:
            # identify number of rows needed for subplot
            if self.filecount % 3 != 0:
                r = int((self.filecount // 3) + 1)
            else:
                r = int(self.filecount / 3)

            # create subplots
            fig = make_subplots(rows=r, cols=3,
                                subplot_titles=list(self.data.keys()),
                                x_title='Words', y_title='Word Count')

            # identify all possible subplot positions
            pos = list(itertools.product(list(range(1, r + 1)), list(range(1, 4))))

            # find the most common words from each file
            for idx, file in enumerate(self.data):
                top_words = sort_limit_dict(self.data[file]['word_count'], limit=k)

                # bar plot the words and their frequencies
                fig.add_trace(
                    go.Bar(x=tuple(top_words.keys()), y=tuple(top_words.values()), name=file),
                    row=pos[idx][0], col=pos[idx][1]
                )

            # label the plot and display
            fig.update_layout(height=800, title={'text': 'Top Words in Each File', 'xanchor': 'center'})
            fig.show()

    def wordcount_sankey(self, word_list=None, k=5):
        """ map each text to user-specified number of words
        using a Sankey diagram, where the thickness of the line
        is the number of times that word occurs in the text. """

        # build rows in the dataframe (i.e. [filename, word, word_count])
        rows = []
        for file, results in self.data.items():
            for word in self.top_k(k).keys():
                row_data = file, word, results['word_count'][word]
                rows.append(row_data)

        # source = filenames, target = words, values = wordcounts
        df = pd.DataFrame(rows, columns=['src', 'targ', 'vals'])

        # generate sankey diagram
        sk.make_sankey(df, 'src', 'targ', vals='vals')

    def wordlength_sunburst(self):
        """ generates a sunburst diagram of the longest word in each file
            and the amount of vowels vs consonant in that word. """

        # identify vowels
        vowels = 'aeiou'

        # initiate a list to build the rows in our dataframe
        rows = []

        # for each file, find the longest word and its length
        for file, results in self.data.items():
            lw = sort_limit_dict(results['word_length'], limit=1)
            for k, v in lw.items():
                l_word = k
                l_length = v

            # count the vowels in the longest word
            v_count = 0
            v_count = len([v_count + 1 for letter in l_word if letter in vowels])

            # load data in the rows
            row0 = [file, l_word, l_length, v_count, 'vowel']
            row1 = [file, l_word, l_length, l_length - v_count, 'consonant']
            rows.append(row0)
            rows.append(row1)

        # create the dataframe for the diagram
        df = pd.DataFrame(rows, columns=['title', 'longest_word', 'word_length', 'letters', 'vow_ratio'])

        # initialize a figure and display the sunburst diagram
        fig = px.sunburst(df, path=['title', 'longest_word', 'vow_ratio'], values='letters')
        fig.show()

    def visualize(self, viz_type=4):
        """ generates a visualization based on user input of selected viz choices
            1. Sankey Diagram
            2. Barchart Subplots
            3. Sunburst Diagram
            4. All of the Above
        """
        try:
            assert viz_type in [1, 2, 3, 4], 'Input must be one of the options provided: 1, 2, 3, 4'

        except AssertionError as ae:
            raise OutOfRangeError(viz_type, msg=str(ae))

        else:
            if viz_type == 1:
                k = int(input('\nHow many common words do you want to analyze?\n'))
                self.wordcount_sankey(k=k)

            if viz_type == 2:
                k = int(input('How many common words do you want to analyze?\n'))
                self.numwords_barchart(k=k)

            if viz_type == 3:
                self.wordlength_sunburst()

            if viz_type == 4:
                k = int(input('How many common words do you want to analyze?\n'))
                self.wordcount_sankey(k=k)
                self.numwords_barchart(k=k)
                self.wordlength_sunburst()


