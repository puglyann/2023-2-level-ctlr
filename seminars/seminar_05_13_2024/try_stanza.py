"""
Listing for practice with stanza module

0. Installation

Warning!
The following functions are NOT to be imported in your work.
Instead, use it as a reference for library API.

0. Installation

stanza is not a standard Python library: it is not pre-installed.
Make sure to specify library name and version in the requirements.txt file!
Make sure to install the library in your working environment!
"""
from pathlib import Path

from core_utils.pipeline import CoNLLUDocument, StanzaDocument

try:
    import stanza
    from stanza.models.common.doc import Document
    from stanza.pipeline.core import Pipeline
    from stanza.utils.conll import CoNLL
except ImportError:
    print('No libraries installed. Failed to import.')


def load_model() -> Pipeline:
    """
    1. Loading model

    This is a necessary step for your work with lab 6.

    Let's use stanza interface to do the following:
        1. Download stanza model
        2. Initialize a pipeline with downloaded model

    Notice that, similar to spacy-udpipe, stanza models consist of
    different pipelines such as tokenization, PoS tagging
    and dependency parsing. For this reason, we specify
    required analysis stages in the arguments.

    Returns:
        stanza.pipeline.core.Pipeline: Language model
    """
    language = "ru"
    processors = "tokenize,pos,lemma,depparse"
    stanza.download(lang=language, processors=processors, logging_level="INFO")
    model = Pipeline(
        lang=language,
        processors=processors,
        logging_level="INFO",
        download_method=None
    )
    return model


def analyze_text(model: Pipeline, text: str) -> Document | list[StanzaDocument]:
    """
    2. Extracting the features from the text

    This is a necessary step for your work with lab 6.

    Stanza's interface for analyzing the text is a little different:
        1. `process` method accepts a Document instance (or a list of such instances),
            containing a text to be processed
        2. Document instance is initialized with the following arguments:
           - list of sentences in the CoNLL-U format,
             if available (in our case, leave it empty)
           - original text

    The returned instance already contains information about lemmas,
    morphological features, PoS etc., but not in the CoNNL-U format

    Args:
        model (stanza.pipeline.core.Pipeline): Language model
        text (str): text to analyze via UDPipe model

    Returns:
        stanza.models.common.doc.Document: annotated text
    """
    analyzed = model.process(Document([], text=text))
    return analyzed


def export_conllu_annotation(document: Document, path: Path) -> None:
    """
    3. Save extracted features to CoNLL-U file

    This is a necessary step for your work with lab 6.

    Stanza allows for direct dump of extracted information to the .conllu file.
    For this, we use `write_doc2conll` method from
    stanza.utils.conll.CoNLL module.
    It accepts Document instance with analyzed text and
    a path where the file should be saved.

    Args:
        document (stanza.models.common.doc.Document): Analyzed text
        path (str): path to the resulting file with CoNLL-U annotation
    """
    CoNLL.write_doc2conll(
        doc=document,
        filename=path,
    )


def import_conllu_annotation(path: Path) -> Document | CoNLLUDocument:
    """
    4. Import Document with text description from CoNLL-U file

    This is a necessary step for your work with lab 6.

    Conversely, stanza support creation of Document from .conllu files.
    For this, we use `conll2doc` method from
    stanza.utils.conll.CoNLL module.
    It accepts a path to a CoNLL-U file.

    Args:
        path (str): path to the resulting file with CoNLL-U annotation

    Returns:
        stanza.models.common.doc.Document: Analyzed text
    """
    return CoNLL.conll2doc(input_file=path)


def extract_linguistic_feature(document: Document, feature: str) -> list[list[int | str]]:
    """
    5. Extract annotation for each word individually

    This is a necessary step for your work with lab 6.

    Stanza allows for access for each CoNLL-U markup feature for each word individually.
    This can help you perform qualitative analysis over text
    (e.g. calculating statistics of a particular feature occurrence
    or exploring grammar structure of a sentence).

    Structure of the analyzed text is organized as follows:
    stanza.Document: [
          stanza.Sentence : [stanza.Word, stanza.Word, ...]
          stanza.Sentence : [stanza.Word, stanza.Word, ...]
          ...]

    So, in order to access information about each particular word,
    one has to firstly iterate over `Document.sentences` attribute.
    It contains a list of `stanza.Sentence` objects.
    Each `stanza.Sentence` object, it its turn, has `Sentence.words`
    attribute, which contains a list of `stanza.Word` objects.

    Finally, `stanza.Word` contains all features used for
    CoNLL-U annotation: id, lemma, upos, head, deprel, misc etc.
    To conveniently access each feature, convert `stanza.Word`
    to Python dictionary with `.to_dict()` method.
    Sample resulting dictionary:
    {
          "id": 2,
          "text": "люблю",
          "lemma": "любить",
          "upos": "VERB",
          "feats": "Aspect=Imp|Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act",
          "head": 0,
          "deprel": "root",
          "misc": "",
          "start_char": 10,
          "end_char": 15
    }

    Args:
        document (stanza.models.common.doc.Document): Analyzed text
        feature (str): Name of CoNLL-U feature to extract

    Returns:
        list[list[int | str]]: Extracted features
    """
    sentences_features = []
    for conllu_sentence in document.sentences:
        sentence_features = []
        for word in conllu_sentence.words:
            word_feature = word.to_dict()[feature]
            sentence_features.append(word_feature)
        sentences_features.append(sentence_features)
    return sentences_features


def main() -> None:
    """
    Entrypoint for a seminar's listing
    """
    # 1. Download and initialize Stanza model
    stanza_model = load_model()
    assert isinstance(stanza_model, stanza.pipeline.core.Pipeline)

    # 2. Extract linguistic features
    text_to_analyze = "Привет! Я люблю программировать."
    analyzed_text = analyze_text(stanza_model, text_to_analyze)
    assert isinstance(analyzed_text, Document)
    print(analyzed_text)

    # 3. Save extracted features to .conllu file
    conllu_file_path = Path('analyzed_text.conllu')
    export_conllu_annotation(analyzed_text, conllu_file_path)
    assert conllu_file_path.exists()

    # 4. Load text and its properties from .conllu file
    loaded_analyzed_text = import_conllu_annotation(conllu_file_path)
    assert isinstance(loaded_analyzed_text, Document)
    print(loaded_analyzed_text)

    # 5. Extract particular features from each word in each sentence
    upos_information = extract_linguistic_feature(loaded_analyzed_text, "upos")
    assert upos_information == [['NOUN', 'PUNCT'], ['PRON', 'VERB', 'VERB', 'PUNCT']]
    deprel_information = extract_linguistic_feature(loaded_analyzed_text, "deprel")
    assert deprel_information == [['root', 'punct'], ['nsubj', 'root', 'xcomp', 'punct']]
    head_information = extract_linguistic_feature(loaded_analyzed_text, "head")
    assert head_information == [[0, 1], [2, 0, 2, 2]]


if __name__ == "__main__":
    main()
