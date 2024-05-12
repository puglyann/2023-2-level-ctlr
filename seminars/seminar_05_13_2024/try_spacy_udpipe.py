"""
Listing for practice with spacy-udpipe module

Warning!
The following functions are NOT to be imported in your work.
Instead, use it as a reference for library API.

0. Installation

spacy-udpipe is not a standard Python library: it is not pre-installed.
Make sure to specify library name and version in the requirements.txt file!
Make sure to install the library in your working environment!
"""
from pathlib import Path

try:
    import spacy
    import spacy_udpipe
except ImportError:
    print('No libraries installed. Failed to import.')

from core_utils.constants import UDPIPE_MODEL_PATH
from core_utils.pipeline import AbstractCoNLLUAnalyzer


def load_model(model_path: Path) -> spacy.Language | AbstractCoNLLUAnalyzer:
    """
    1. Loading model

    This is a necessary step for your work with lab 6.

    Let's use spacy-udpipe interface to read the pre-downloaded UDPipe model.
    Find the path to the model and pass it as an argument.

    NOTE:
        `spacy_udpipe.load_from_path` accepts 2 arguments:
            1. language specification (for us, it is `ru` for the Russian language)
            2. path to the model as a string

    Args:
        model_path (Path): Path to pre-downloaded UDPipe model

    Returns:
        spacy.Language: Language model
    """
    model = spacy_udpipe.load_from_path(
        lang="ru",
        path=str(model_path)
    )
    return model


def explore_model(model: spacy.Language) -> dict | None:
    """
    2. Exploring model

    This is NOT a necessary step for your work with lab 6.
    It helps us understand the model while we learn the framework.

    Spacy Model comprises various pipelines e.g. tagging, lemmatization etc.
    Let's check which pipelines are added to the model.

    Args:
        model (spacy.Language): Language model

    Returns:
        dict: Language model pipelines summary
    """
    return model.analyze_pipes()


def enable_conllu_formatting(model: spacy.Language) -> spacy.Language:
    """
    3. Adding CoNLL-U formatter

    This is a necessary step for your work with lab 6.

    To be able to produce CoNNL-U formatted annotations,
    we need to add a special pipeline to the Spacy model.

    For this, we use `add_pipe` model method, which accepts:
        1. pipe name (in our case, `conll_formatter`)
        2. configuration

    In configuration, we want to specify the following:
        - conversion map for XPOS feature: for this model, XPOS tags are not specified, so
          we want to convert empty string "" to the appropriate missing value symbol "_"
        - whether resulting ConLL-U files should include headers with sentence number and text:
          for your work, it is required that annotated files contain headers, so we specify
          this argument to be `True`

    Args:
        model (spacy.Language): Language model

    Returns:
        spacy.Language: Language model with added UD pipe
    """
    model.add_pipe(
        "conll_formatter",
        last=True,
        config={"conversion_maps": {"XPOS": {"": "_"}}, "include_headers": True},
    )
    return model


def annotate_text(model: spacy.Language, text: str) -> str:
    """
    4. Annotating text with CoNLL-U format

    This is a necessary step for your work with lab 6.

    In order to produce a string with CoNNL-U annotation, we need to
        1. Analyze text via UDPipe model via call method
        2. Extract formatted string from the special attribute

    Args:
        model (spacy.Language): Language model
        text (str): text to analyze via UDPipe model

    Returns:
        str: CoNLL-U annotation
    """
    analyzed_text = model(text)
    conllu_annotation = analyzed_text._.conll_str
    return str(conllu_annotation)


def export_conllu_annotation(annotation: str, path: Path) -> None:
    """
    5. Save extracted features to CoNLL-U file

    This is a necessary step for your work with lab 6.

    `spacy-udpipe` model interface does not permit direct saving
    of extracted linguistic features to a .conllu file.
    For this reason, production of such files is to be done manually.
    Create a file with a specified path and write extracted
    string with CoNLL-U annotation to this file.
    Make sure to add additional newline!

    Args:
        annotation (str): CoNLL-U annotation of the text
        path (str): Path to the resulting file with CoNLL-U annotation
    """
    with open(path, 'w', encoding='utf-8') as annotation_file:
        annotation_file.write(annotation)
        annotation_file.write("\n")


def main() -> None:
    """
    Entrypoint for a seminar's listing
    """
    # 1. Read the UDPipe model
    #    It is pre-downloaded for you from https://universaldependencies.org/
    udpipe_model = load_model(UDPIPE_MODEL_PATH)
    assert isinstance(udpipe_model, spacy.Language)

    # 2. Explore the loaded UDPipe model and explain
    #    whether it is ready to perform CoNLL-U annotation
    model_summary = explore_model(udpipe_model)
    print(model_summary)

    # 3. Add CoNLL-U formatting pipeline to the model
    enable_conllu_formatting(udpipe_model)
    model_summary = explore_model(udpipe_model)
    print(model_summary)
    assert isinstance(model_summary, dict)
    assert 'conll_formatter' in model_summary['summary']

    # 4. Annotate text using CoNNL-U format
    text_to_analyze = "Привет! Я люблю программировать."
    annotation = annotate_text(udpipe_model, text_to_analyze)
    print(annotation)
    assert 'Aspect=Imp|Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Ac' in annotation

    # 5. Write extracted CoNLL-U annotation to the file
    conllu_file_path = Path('analyzed_text.conllu')
    export_conllu_annotation(annotation, conllu_file_path)


if __name__ == "__main__":
    main()
