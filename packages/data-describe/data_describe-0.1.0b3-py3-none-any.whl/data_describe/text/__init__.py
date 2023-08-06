"""data-describe text.

This subpackage provides functionality to process and analyze unstructured, free-form text using text analytics & Natural Language Processing (NLP).
"""
from data_describe.text.text_preprocessing import (  # noqa: F401
    tokenize,
    to_lower,
    remove_punct,
    remove_digits,
    remove_single_char_and_spaces,
    remove_stopwords,
    lemmatize,
    stem,
    bag_of_words_to_docs,
    create_tfidf_matrix,
    create_doc_term_matrix,
    preprocess_texts,
    ngram_freq,
    filter_dictionary,
)
