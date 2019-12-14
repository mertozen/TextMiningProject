"""
Zemberek: Turkish Tokenization Example
Java Code Example: https://bit.ly/2PsLOkj
"""

from os.path import join

import pandas as pd

import dask.dataframe as dd


from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if not value in lst2]
    return lst3

if __name__ == '__main__':

    ZEMBEREK_PATH: str = join('..', '..', 'bin', 'zemberek-full.jar')

    startJVM(
        getDefaultJVMPath(),
        '-ea',
        f'-Djava.class.path={ZEMBEREK_PATH}',
        convertStrings=False
    )

    TurkishTokenizer: JClass = JClass('zemberek.tokenization.TurkishTokenizer')
    Token: JClass = JClass('zemberek.tokenization.Token')
    tokenizer: TurkishTokenizer = TurkishTokenizer.DEFAULT

    with open(
        join('..', '..', 'data', 'normalization','raw_texts','ekonomi','1.txt'),
        'r',
        encoding = 'cp1254'
    ) as document_file:
        document = document_file.read()

    with open(
            join('..', '..', 'data', 'normalization','stopwords.txt'),
            'r',
            encoding='utf-8'
    ) as stopwords_file:
        stopwordstext = stopwords_file.read()


    tokenizer: TurkishTokenizer = TurkishTokenizer.builder().ignoreTypes(
        Token.Type.Punctuation,
        Token.Type.NewLine,
        Token.Type.SpaceTab,
        Token.Type.Number
    ).build()
    words = list(tokenizer.tokenize(JString(document)))
    stop_words = list(tokenizer.tokenize(JString(stopwordstext)))

    for token in intersection(words,stop_words):
        print(token)

    shutdownJVM()
