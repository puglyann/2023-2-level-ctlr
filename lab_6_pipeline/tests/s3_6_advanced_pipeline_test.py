# pylint: disable=protected-access
"""
Tests for advances morphological analysis pipeline.
"""
import shutil
import unittest
from pathlib import Path

import pytest
from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from pymorphy2 import MorphAnalyzer

from core_utils.article import article
from core_utils.article.ud import TagConverter
from lab_6_pipeline.pipeline import CorpusManager, MorphologicalAnalysisPipeline
from lab_6_pipeline.tests.utils import pipeline_test_files_setup


@pytest.mark.skip
class AdvancedMorphologicalAnalysisPipelineTest(unittest.TestCase):
    """
    Class for checking advanced morphological pipeline.
    """

    def setUp(self) -> None:
        """
        Define start instructions for AdvancedMorphologicalAnalysisPipelineTest class.
        """
        pipeline_test_files_setup()
        article.ASSETS_PATH = TEST_PATH

        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        self.pipeline = MorphologicalAnalysisPipeline(corpus_manager)
        self.pipeline.run()
        self.raw_text = corpus_manager.get_articles()[1].get_raw_text()

        path = PIPE_TEST_FILES_FOLDER / 'reference_score_ten_test.conllu'
        with path.open('r', encoding='utf-8') as ref:
            self.conllu_reference = ref.read()
        self.expected_text_w_morph = self.conllu_reference

        path = PIPE_TEST_FILES_FOLDER / 'reference_score_ten_wo_morph_test.conllu'
        with path.open('r', encoding='utf-8') as ref:
            self.conllu_reference = ref.read()
        self.expected_text_wo_morph = self.conllu_reference

    @pytest.mark.mark10
    @pytest.mark.stage_3_6_advanced_morphological_processing
    @pytest.mark.lab_6_pipeline
    def test_processing_with_morph_tags(self) -> None:
        """
        Test advanced processing with morphological tags.
        """
        conllu_sentences = self.pipeline._process(self.raw_text)
        expected_sentences = conllu_sentences[0].get_conllu_text(
            include_morphological_tags=True
        )
        self.assertEqual(self.expected_text_w_morph, f"{expected_sentences}\n")

    @pytest.mark.mark10
    @pytest.mark.stage_3_6_advanced_morphological_processing
    @pytest.mark.lab_6_pipeline
    def test_processing_without_morph_tags(self) -> None:
        """
        Test advanced processing without morphological tags.
        """
        conllu_sentences = self.pipeline._process(self.raw_text)
        expected_sentences = conllu_sentences[0].get_conllu_text(
            include_morphological_tags=False
        )
        self.assertEqual(self.expected_text_wo_morph, f"{expected_sentences}\n")

    def tearDown(self) -> None:
        """
        Define final instructions for AdvancedMorphologicalAnalysisPipelineTest class.
        """
        shutil.rmtree(TEST_PATH)
