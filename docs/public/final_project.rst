Final project description
=========================

Each `team <https://docs.google.com/spreadsheets/d/
1dp7pSRHX8XXkAaTYJxhulDnp_VokA3b3SUoc4XAfc3s/edit#gid=0>`__
is to work with the corresponding folder:

-  22FPL1 team 1 - axmatova
-  22FPL1 team 2 - balmont
-  22FPL1 team 3 - blok
-  22FPL1 team 4 - bunin
-  22FPL1 team 5 - cvetaeva
-  22FPL2 team 1 - mandelstamm
-  22FPL2 team 2  - moritz
-  22FPL2 team 3  - pasternak
-  22FPL2 team 4  - silverage

All the files from the folder are to be joint into one ``.txt`` file
and then processed using UDPipe.

The resulting ``.conllu`` file is to be opened in a text editor
and then copied to an ``.xlsx`` file. To work with the file you will
need the following columns in the table:

-  token number
-  token
-  lemma
-  part of speech
-  morphological characteristics

Please delete all the remaining columns provided by UDPipe and add three new columns:

-  comments to POS tags
-  comments to characteristics
-  comments to tokens

Using the ``.conllu`` file you are supposed to make up the word frequency dictionary.
Once it is ready, you are welcome to work with the least popular word forms
to find the **mistakes in tokenization** made by UDPipe. If any of the word forms turn out
to be words joint with punctuation marks or words divided into tokens, you are supposed
to correct the mistakes in the ``.conllu`` file and write comments
in the “comments to tokens” column in the ``.xlsx`` file.

Next comes checking the table for mistakes in morphological annotation made by UDPipe.
Whenever you come across any mistakes in either POS tags or characteristics,
you are welcome to fill in the corresponding column with the comment in the ``.xlsx`` file
and make corrections in the ``.conllu`` file. When making judgements as to the **mistakes
in morphological annotation**, you are welcome to use the following sources:

1. `UD POS tags <https://universaldependencies.org/u/pos/all.html>`__.
2. `UD POS features <https://universaldependencies.org/u/feat/index.html>`__.
3. `UD Russian POS tags and features
   <https://universaldependencies.org/treebanks/ru_gsd/index.html>`__.
4. Dictionaries of the Russian language containing morphological information.

Please do not forget to refer to the sources you use in the comments.
You are supposed to stop working with the ``.conllu`` file and  ``.xlsx`` file
and send them to Klimova Margarita Andreevna together with the frequency dictionary
in the ``.xlsx`` format by **16 June**.

Klimova Margarita Andreevna will check your comments and corrections
and suggest improvements, if any.

.. note:: Correctness of the ``.conllu`` file will be checked with a script
          taken from the repository with code from the `Technical Track
          <https://github.com/fipl-hse/2023-2-level-ctlr/blob/main/
          admin_utils/final_project/checker.py>`__. You can also use it
          to check the ``.conllu`` file: run it locally and then,
          if it does not fail, send it to Klimova Margarita Andreevna.

          This script can be run from PyCharm or PowerShell from a root of the project,
          like this: ``python admin_utils/final_project/checker.py PATH_TO_FILE``.
          Your forks should contain this script already, so pull and use, otherwise,
          type to the chat and ask assistants.

          For example, you have file ``final.conllu``, place it in ``data`` folder:

          .. code:: bash

                |-- 2023-2-level-ctrl
                    |-- data
                        |-- final.conllu

          Then you can run the checker script with (do not forget to activate
          environment and update ``PYTHONPATH``):

          .. code:: bash

                python admin_utils/final_project/checker.py data/final.conllu

Meanwhile your task will be to prepare the **exam presentation**,
which should include a report of the mistakes in tokenization
and morphological annotation you came across - both a quantitative
and qualitative (typology of mistakes, possible reasons for them) analysis.
Time limit - 7 minutes.

The presentation is to be delivered at the exam. Assessment criteria:

1. The proportion of the identified mistakes;
2. The quality of their analysis in the comments section of the table and in the presentation;
3. The precision of corrections made in the .conllu file;
4. Following the time limit;
5. The quality of the oral presentation
   (text learnt by heart, fluency and intelligibility of speech);
6. The quality of the computer presentation;
7. The quality of answers to follow-up questions.

.. attention:: The mark you get as a result will have a coefficient of 0,8.
               The remaining 20% of the exam mark belongs to the mark
               for working with КрякваБот.
