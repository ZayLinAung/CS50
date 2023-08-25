import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dic = {}
    for files in os.listdir(directory):
        print("Loading data from " + files)
        text_file = open(os.path.join(directory, files), encoding="utf8")
        data = text_file.read()
        text_file.close()
        dic[files] = data
    return dic


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = []
    for word in nltk.word_tokenize(document.lower()):
        if word not in nltk.corpus.stopwords.words("english"):
            filterWord = word.translate(str.maketrans('','',string.punctuation))
            if len(filterWord) > 0:
                words.append(filterWord)
        
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    dic = {}
    for files in documents:
        for words in documents[files]:
            docCount = 0
            for docs in documents:
                if words in documents[docs]:
                    docCount += 1
            dic[words] = math.log(len(documents) / docCount)
    return dic


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    fileRank = {}
    for docs in files:
        tf_idf = 0
        for words in files[docs]:
            if words in query:
                wordCount = 0
                for terms in files[docs]:
                    if terms == words:
                        wordCount += 1
                tf_idf += wordCount * idfs[words]
        fileRank[docs] = tf_idf

    topFiles = list(dict(sorted(fileRank.items(), key = lambda x: x[1], reverse = True)[:n]))
    return topFiles

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    SenRank = []
    for sen in sentences:
        idf = 0
        freq = 0
        for words in sentences[sen]:
            if words in query:
                freq += 1
                idf += idfs[words]
        density = freq / len(sentences[sen])
        SenRank.append((sen, idf, density))

    SenRank.sort(key=lambda x: (x[1], x[2]), reverse=True)

    topSen = []
    for sen in SenRank[:n]:
        topSen.append(sen[0])
    return topSen

    


if __name__ == "__main__":
    main()
