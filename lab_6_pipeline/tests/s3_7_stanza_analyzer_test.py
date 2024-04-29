"""
Tests udpipe analyzer.
"""
# pylint: disable=protected-access,import-error,assignment-from-no-return
import json
import shutil
import unittest

import pytest
import stanza
from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH

from core_utils.article import article
from lab_6_pipeline.pipeline import CorpusManager, StanzaAnalyzer, TextProcessingPipeline
from lab_6_pipeline.tests.utils import pipeline_test_files_setup


class StanzaAnalyzerTest(unittest.TestCase):
    """
    Tests for stanza texts analysis.
    """

    def setUp(self) -> None:
        """
        Define start instructions for StanzaAnalyzerTest class.
        """
        path = PIPE_TEST_FILES_FOLDER / "reference_score_eight_analyzer_test.json"
        with path.open("r", encoding="utf-8") as ref:
            self.reference = json.load(ref)

        path = PIPE_TEST_FILES_FOLDER / "reference_score_eight_analyzer_from_conllu.json"
        with path.open("r", encoding="utf-8") as ref_from_conllu:
            self.reference_from_conllu = json.load(ref_from_conllu)

        self.texts = [
            "Красивая - мама красиво, училась в ПДД и "
            "ЖКУ по адресу Львовская 10 лет с почтой test ."
        ]
        self.stanza_analyzer = StanzaAnalyzer()

        pipeline_test_files_setup()
        article.ASSETS_PATH = TEST_PATH

        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        text_processing_pipeline = TextProcessingPipeline(corpus_manager, StanzaAnalyzer())
        text_processing_pipeline.run()

        self.articles = corpus_manager.get_articles()

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    @pytest.mark.lab_6_pipeline
    def test_analyze_method(self) -> None:
        """
        Check the correctness of the analyze method.
        """
        analysis = self.stanza_analyzer.analyze(self.texts)

        for reference, stanza_analysis in zip(self.reference[0], analysis[0].to_dict()[0]):
            self.assertEqual(reference, stanza_analysis)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    @pytest.mark.lab_6_pipeline
    def test_type_of_analyzer(self) -> None:
        """
        Check the type of the stanza pipeline.
        """
        self.assertIsInstance(self.stanza_analyzer._analyzer, stanza.pipeline.core.Pipeline)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    @pytest.mark.lab_6_pipeline
    def test_from_conllu_method(self) -> None:
        """
        Check the correctness of the from_conllu method.
        """
        from_conllu_format = self.stanza_analyzer.from_conllu(article=self.articles[1])

        for reference, stanza_analysis in zip(self.reference_from_conllu[0],
                                              from_conllu_format.to_dict()[0]):
            self.assertEqual(reference, stanza_analysis)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Define final instructions for ReferenceTextPreprocessBasicTest class.
        """
        shutil.rmtree(TEST_PATH)
