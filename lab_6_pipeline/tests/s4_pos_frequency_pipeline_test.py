"""
Tests for POS frequency pipeline.
"""
# pylint: disable=no-name-in-module
import json
import shutil
import unittest

import pytest
from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH

from core_utils.article import article
from lab_6_pipeline import pipeline
from lab_6_pipeline.pipeline import (CorpusManager, EmptyFileError, POSFrequencyPipeline,
                                     StanzaAnalyzer)
from lab_6_pipeline.tests.utils import pipeline_test_files_setup


class PosFrequencyPipelineTests(unittest.TestCase):
    """
    Tests for POSFrequencyPipeline realization.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Define start instructions for PosFrequencyPipelineTests class.
        """
        pipeline_test_files_setup()
        shutil.copyfile(PIPE_TEST_FILES_FOLDER /
                        "reference_score_eight_test.conllu",
                        TEST_PATH / "1_stanza_conllu.conllu")

        article.ASSETS_PATH = TEST_PATH
        pipeline.ASSETS_PATH = TEST_PATH

        cls.corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        path = cls.corpus_manager.get_articles()[1].get_meta_file_path()
        with open(path, 'r', encoding='utf-8') as meta_file:
            meta = json.load(meta_file)
        print(meta)
        cls.frequencies = meta.pop('pos_frequencies')
        print(cls.frequencies)
        with open(path, 'w', encoding='utf-8') as meta_file:
            json.dump(meta,
                      meta_file,
                      sort_keys=False,
                      indent=4,
                      ensure_ascii=False,
                      separators=(',', ': '))

        pos_pipe = POSFrequencyPipeline(cls.corpus_manager, StanzaAnalyzer())
        pos_pipe.run()

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    @pytest.mark.lab_6_pipeline
    def test_meta_files_readable(self) -> None:
        """
        Ensure meta files are not corrupt.
        """
        failed = False
        try:
            one_article = self.corpus_manager.get_articles()[1]
            path = one_article.get_meta_file_path()
            with open(path, 'r', encoding='utf-8') as meta_file:
                json.load(meta_file)
        except json.decoder.JSONDecodeError:
            failed = True
        finally:
            message = 'Generated meta files are corrupt: ' \
                      'check how you update .json files'
            self.assertFalse(failed, message)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    @pytest.mark.lab_6_pipeline
    def test_frequencies_are_correct(self) -> None:
        """
        Ensure frequencies are counted correctly.
        """
        one_article = self.corpus_manager.get_articles()[1]
        path = one_article.get_meta_file_path()
        print(path)
        with open(path, 'r', encoding='utf-8') as meta_file:
            frequencies = json.load(meta_file)['pos_frequencies']
        print(self.frequencies)
        print(frequencies)
        self.assertEqual(self.frequencies, frequencies,
                         'POS frequencies are calculated incorrectly')

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    @pytest.mark.lab_6_pipeline
    def test_images_are_generated(self) -> None:
        """
        Ensure images are generated.
        """
        msg = 'POSFrequencyPipeline does not create image ' \
              'file for at least one of articles available'
        ids_available = set(
            map(
                lambda filename: int(str(filename.name).split('_', maxsplit=1)[0]),
                TEST_PATH.iterdir()
            )
        )
        for identifier in ids_available:
            path = TEST_PATH / f'{identifier}_image.png'
            self.assertTrue(path.is_file(), msg)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    @pytest.mark.lab_6_pipeline
    def test_pos_throws_error(self) -> None:
        """
        Ensure that POS pipe raises EmptyFileError.
        """
        with open(TEST_PATH / "1_stanza_conllu.conllu", 'w',
                  encoding='utf-8') as file:
            file.write('')

        new_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)

        new_pipe = POSFrequencyPipeline(new_manager, StanzaAnalyzer())
        with self.assertRaises(EmptyFileError):
            new_pipe.run()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Define final instructions for PosFrequencyPipelineTests class.
        """
        shutil.rmtree(TEST_PATH)
