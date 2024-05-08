.. _ud-format-label:

Working with UD format and ``CoNLL-U``
======================================

UD (Universal Dependencies) is a framework for consistent
annotation of grammar (parts of speech, morphological features, and
syntactic dependencies) across different human languages. All this
annotation is usually stored in a format called ``CoNLL-U``, that is
a vertical, table-like format.

.. contents:: Content:
   :depth: 2

UD
--

The UD format for storing morphological information is structured as
follows: ``FeatureName=Value|FeatureName=Value|FeatureName=Value...``
where ``FeatureName`` is a name of the morphological feature of the
token (for example, ``Number``) and ``Value`` is the actual value of the
feature (for example, ``Sing`` - short for singular).

For example:

-  ``Animacy=Inan|Case=Acc|Degree=Pos|Gender=Masc|Number=Sing``

   -  ``Animacy=Inan`` - inanimate
   -  ``Case=Acc`` - accusative case
   -  ``Degree=Pos`` - degree of comparison: positive/first degree
   -  ``Gender=Masc`` - masculine gender
   -  ``Number=Sing`` - singular number

.. note:: The list of all tags used in the UD system is available on
          the `dedicated page <https://universaldependencies.org/u/feat/index.html>`__.

``CoNLL-U`` structure
---------------------

After processing articles, you should save
annotated data in a ``.conllu`` file.
It has the following structure, where each field is responsible for:

+-------------+-------------------------------------------------------------+--------------------+
| Field       | Description                                                 | Library            |
+=============+=============================================================+====================+
| **ID**      | Word index, integer starting at 1                           | ``spacy_udpipe``,  |
|             | for each new word in the sentence                           | ``stanza``         |
+-------------+-------------------------------------------------------------+--------------------+
| **FORM**    | Word form or punctuation symbol                             | ``spacy_udpipe``,  |
|             |                                                             | ``stanza``         |
+-------------+-------------------------------------------------------------+--------------------+
| **LEMMA**   | Lemma or stem of word form                                  | ``spacy_udpipe``,  |
|             |                                                             | ``stanza``         |
+-------------+-------------------------------------------------------------+--------------------+
| **UPOS**    | Universal POS tag                                           | ``spacy_udpipe``,  |
|             |                                                             | ``stanza``         |
+-------------+-------------------------------------------------------------+--------------------+
| **XPOS**    | Language-specific POS tag                                   | ``spacy_udpipe``,  |
|             |                                                             | ``stanza``         |
+-------------+-------------------------------------------------------------+--------------------+
| **FEATS**   | List of morphological features                              | ``spacy_udpipe``,  |
|             | structured as                                               | ``stanza``         |
|             | ``FeatureName=Value|FeatureName=Value|FeatureName=Value...``|                    |
|             | as per UD format                                            |                    |
+-------------+-------------------------------------------------------------+--------------------+
| **HEAD**    | Head of the current word                                    | ``spacy_udpipe``,  |
|             |                                                             | ``stanza``         |
+-------------+-------------------------------------------------------------+--------------------+
| **DEPREL**  | Universal dependency relation to the HEAD                   | ``spacy_udpipe``,  |
|             |                                                             | ``stanza``         |
+-------------+-------------------------------------------------------------+--------------------+
| **DEPS**    | Enhanced dependency graph in the form of a list of          | ``spacy_udpipe``,  |
|             | head-deprel pairs                                           | ``stanza``         |
+-------------+-------------------------------------------------------------+--------------------+
| **MISC**    | Any other annotation                                        | ``stanza``         |
+-------------+-------------------------------------------------------------+--------------------+

In addition, you must take into account that:

-  New sentences start with the token ID being ``1``;
-  Fields cannot be empty. If no value for a field, the ``_`` is used;
-  Comments usually consist of the sentences and are denoted using
   ``#``.

Let’s explain the first line
``1	Красивая красивый ADJ _ Case=Nom|Degree=Pos|Gender=Fem|Number=Sing 3 amod _ _``
from `Desired output <https://github.com/fipl-hse/2023-2-level-ctlr/blob/main/lab_6_pipeline/tests/
test_files/reference_score_six_test.conllu>`__ for mark 6:

-  ``1`` - ID
-  ``Красивая`` - text of the token
-  ``красивый`` - lemma of the token
-  ``ADJ`` - POS
-  ``_`` - language specific POS - none in this case
-  ``Case=Nom|Degree=Pos|Gender=Fem|Number=Sing`` -
   morphological features of the token as per
   `tags <https://universaldependencies.org/u/feat/index.html>`__:

   -  ``Case=Nom`` - nominative case
   -  ``Degree=Pos`` - degree of comparison: positive/first degree
   -  ``Gender=Fem`` - feminine gender
   -  ``Number=Sing`` - singular number

-  ``3`` - the ID of the HEAD for the current token. HEAD is ``мама``
   in this case
-  ``amod`` - relation to the HEAD token (``amod`` - adjectival modifier
   as per `tags <https://universaldependencies.org/u/dep/amod.html>`__)
-  ``_`` - pair of HEAD:RELATION for the current token
-  ``_`` - any other annotation (none in this case)

   -  For mark 8 you will have ``start_char=0|end_char=8`` in this field.
      It denotes the start and end of the token in characters.

.. attention:: More information about the structure of the ``CoNLL-U``
               format is available on the `dedicated
               page <https://universaldependencies.org/format.html>`__.
