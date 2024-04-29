Core utils
==========

.. toctree::
    :maxdepth: 1
    :titlesonly:
    :caption: Full API

    ../../core_utils/core_utils.api.rst

Core utils package contains auxiliary materials to help you implement
your laboratory works. We are going to over each of its parts
to guide you when and how to use it.

Article package
---------------

The ``article`` package is responsible for handling the articles you
have collected from your website. You are going to use it for both
Lab 5 and Lab 6. See exhaustive guide for :ref:`ctlr-article-label`.

Tools package
-------------

This package contains ``ud_validator.py`` module.
It is responsible for verifying that the generated CoNLL-U files match the
format. For more details on the CoNLL-U format, refer to :ref:`ud-format-label`.

As a part of Lab 6, you are to perform a morphological analysis of the
collected articles. Results must be saved as a CoNLL-U file.
The correctness of the file format can be verified via `script prepared for you
<https://github.com/fipl-hse/2023-2-level-ctlr/blob/main/core_utils/tools/ud_validator/validate.py>`__.
To learn how to use it, refer to the :ref:`ud-format-label`.

Configurations DTO
------------------

The ``config_dto.py`` module defines a :py:class:`core_utils.config_dto.ConfigDTO` abstraction.
This abstraction is responsible for indicating what fields must be passed as
a configuration settings along with what their types must be.

They match the fields of the ``scrapper_config.json`` configuration file.
For more details on what each of the parameters presents, refer to :ref:`scrapper-label`.

.. note:: During implementation of Lab 5, make sure to return
          a ``ConfigDTO`` instance from the
          :py:func:`lab_5_scrapper.scrapper.Config._extract_config_content` method.

Module with constants
---------------------

``constants.py`` module defines the following constant values:

-  ``PROJECT_ROOT``: a path to ``2023-2-level-ctlr`` folder,
   which the root of the current project;
-  ``ASSETS_PATH``: a path to ``2023-2-level-ctlr/tmp/article`` folder,
   where all the collected articles must be stored;
-  ``CRAWLER_CONFIG_PATH``: a path to the ``lab_5_scrapper/scrapper_config.json``
   file with configuration parameters for scrapper;
-  ``NUM_ARTICLES_UPPER_LIMIT``: a maximum number for articles to be
   collected, anything above this number must be considered invalid;
-  ``TIMEOUT_LOWER_LIMIT``: a minimum number of seconds for a timeout,
   anything below this number must be considered invalid;
-  ``TIMEOUT_UPPER_LIMIT``: a maximum number of seconds for a timeout,
   anything above this number must be considered invalid.

.. note:: Can you tell why the folder for articles is located in the
          directory with the name ``tmp``?

.. note:: Make sure to import these constants from the ``constants.py`` module
          and use them whenever you need to specify a path or boundary values
          (for example, when validating configuration values).

Visualizer module
-----------------

As a final part of Lab 6, students are expected to perform an
analysis of distribution of part-of-speech tags in the processed
collected articles. This is where ``visualizer.py`` module comes into play.
Its :py:func:`core_utils.visualizer.visualize` function takes an
``Article`` instance along with a path and creates a graph depicting
POS distribution in the specified location.

Before calling it, make sure you have already filled the
``pos_frequencies`` field of the corresponding meta file during
``POSFrequencyPipeline`` execution.

.. note:: :py:func:`core_utils.visualizer.visualize` function must be called
          during the execution of
          :py:meth:`lab_6_pipeline.pipeline.POSFrequencyPipeline.run` method.

.. note:: The name of the resulting image must have the same id as
          the article analysed.

Tests package
-------------

To make sure that the provided materials work as intended, they are
thoroughly tested. The ``tests`` package
contains a number of unit-tests for ``article`` package,
``config_dto.py`` module, and ``visualizer.py`` module.

During work on Lab 5 and Lab 6, you do not need to
interact with these tests. However, you should suspect that the provided
modules behave unexpectedly, examination of these tests may help catch
the bug. Any suggestion on improvements of core utils is encouraged and
rewarded.
