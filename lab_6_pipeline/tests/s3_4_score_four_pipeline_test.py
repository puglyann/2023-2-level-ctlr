"""
Tests for TextProcessingPipeline (score 4).
"""
import shutil
import unittest
from string import punctuation

import pytest
from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH

from core_utils.article import article
from lab_6_pipeline.pipeline import CorpusManager, TextProcessingPipeline
from lab_6_pipeline.tests.utils import AnalyzerMock, pipeline_setup, pipeline_test_files_setup


class TextProcessingPipelineScoreFourReferenceProcess(unittest.TestCase):
    """
    TextProcessingPipeline for score 4 tests on reference data.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup test files for processing.
        """
        pipeline_test_files_setup(meta=True)
        article.ASSETS_PATH = TEST_PATH

        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        pipe = TextProcessingPipeline(corpus_manager)
        pipe.run()

    def setUp(self) -> None:
        """
        Define start instructions for TextProcessingPipelineScoreFourReferenceProcess class.
        """
        path = PIPE_TEST_FILES_FOLDER / "reference_score_four.txt"
        with path.open("r", encoding="utf-8") as reference:
            self.reference = reference.read()
        path = TEST_PATH / "1_cleaned.txt"
        with path.open("r", encoding="utf-8") as processed:
            self.processed = processed.read()

    @pytest.mark.mark4
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_reference_preprocessed_are_equal(self) -> None:
        """
        Ensure equal number of tokens in processed and reference texts.
        """
        # check number of tokens sequences
        self.assertEqual(
            len(self.reference.split()),
            len(self.processed.split()),
            msg=f"""Number of tokens sequences in reference
        {self.reference} and processed {self.processed} texts is different""",
        )

        # check tokenization
        self.assertEqual(
            self.reference.split(),
            self.processed.split(),
            msg="Pipe does not tokenize admin text. Check how you tokenize",
        )

    @pytest.mark.mark4
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_overall_format(self) -> None:
        """
        Ensure that there is no punctuation of uppercase in clean text.
        """
        self.assertTrue(self.processed.islower(), "Cleaned text must be lowercase")
        self.assertFalse(
            (set(self.processed) & set(punctuation)), "Cleaned text must not have any punctuation"
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Define final instructions for TextProcessingPipelineScoreFourReferenceProcess class.
        """
        shutil.rmtree(TEST_PATH)


class TextProcessingPipelineScoreFourMockAnalyzer(unittest.TestCase):
    """
    Tests for TextProcessingPipeline with mocking analyzer.
    """

    @pytest.mark.mark4
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_score_four_pipeline_with_analyzer_mock_can_execute(self) -> None:
        """
        Ensure pipeline for score 4 does not depend on analyzer.
        """
        pipeline_test_files_setup(meta=True)
        article.ASSETS_PATH = TEST_PATH

        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        pipe = TextProcessingPipeline(corpus_manager, AnalyzerMock())
        self.assertIsNone(pipe.run())
        shutil.rmtree(TEST_PATH)


class TextProcessingPipelineScoreFourStudentProcess(unittest.TestCase):
    """
    Tests for TextProcessingPipeline on student data.
    """

    def setUp(self) -> None:
        """
        Define start instructions for TextProcessingPipelineScoreFourReferenceProcess class.
        """
        pipeline_setup()
        CorpusManager(TEST_PATH)
        self.punctuation_marks = [",", ".", "-", ";", ":", "!", "?", "<"]

        self.articles = {}
        for file in TEST_PATH.iterdir():
            if file.name.endswith("_cleaned.txt"):
                with file.open("r", encoding="utf-8") as txt:
                    self.articles[int(file.name[:-12])] = txt.read()

    @pytest.mark.mark4
    @pytest.mark.stage_3_5_student_dataset_validation
    @pytest.mark.lab_6_pipeline
    def test_clean_tokens(self) -> None:
        """
        Ensure there is no punctuation of uppercase in cleaned text.
        """
        for article_id, article_text in self.articles.items():
            for token in article_text.split():
                message = f"There are some punctuation " f"marks found in article {article_id}"
                self.assertTrue(token not in self.punctuation_marks, message)
                if not token.isalpha():
                    continue
                message = f"Token {token} in article " f"{article_id} is not lowercase"
                self.assertTrue(token.islower(), msg=message)

    def tearDown(self) -> None:
        """
        Define final instructions for TextProcessingPipelineScoreFourReferenceProcess class.
        """
        shutil.rmtree(TEST_PATH)
