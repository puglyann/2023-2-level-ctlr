"""
Tests for processing text.
"""
import shutil
import unittest

import pytest
from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH

from core_utils.article import article
from lab_6_pipeline.pipeline import CorpusManager, TextProcessingPipeline, UDPipeAnalyzer
from lab_6_pipeline.tests.utils import pipeline_test_files_setup


class TextProcessingPipelineScoreSixReferenceProcess(unittest.TestCase):
    """
    Tests for preprocessing of texts.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Define start instructions for TextProcessingPipelineScoreSixReferenceProcess class.
        """
        pipeline_test_files_setup()
        article.ASSETS_PATH = TEST_PATH

        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        pipe = TextProcessingPipeline(corpus_manager, UDPipeAnalyzer())
        pipe.run()

    def setUp(self) -> None:
        """
        Define start instructions for TextProcessingPipelineScoreSixReferenceProcess class.
        """
        path = PIPE_TEST_FILES_FOLDER / "reference_score_six_test.conllu"
        with path.open("r", encoding="utf-8") as ref:
            self.conllu_reference = ref.read()

        path = TEST_PATH / "1_udpipe_conllu.conllu"
        with path.open("r", encoding="utf-8") as file:
            self.conllu_processed = file.read()

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    @pytest.mark.lab_6_pipeline
    def test_conllu_reference_preprocessed_are_equal(self) -> None:
        """
        Ensure that reference and processed conllu files have equal number of lines.
        """
        special_message = (
            f"Number of lines in reference "
            f"{self.conllu_reference} and processed "
            f"{self.conllu_processed} texts is different"
        )
        self.assertEqual(len(self.conllu_reference.split("\n")),
                         len(self.conllu_processed.split("\n")),
                         msg=special_message)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    @pytest.mark.lab_6_pipeline
    def test_conllu_tokens_are_formatted(self) -> None:
        """
        Ensure that reference and processed conllu files have equal tokens and length.
        """
        ref_tokens = ["Красивая", "-", "мама", "красиво", ",",
                      "училась", "в", "ПДД", "и", "ЖКУ", "по",
                      "адресу", "Львовская", "10", "лет", "с",
                      "почтой", "test", ".",
        ]

        format_lines_number = list(
            i for i in self.conllu_processed.split("\n") if i.split("\t")[0].isnumeric()
        )
        self.assertEqual(len(ref_tokens), len(format_lines_number))

        for token_id, token in enumerate(ref_tokens):
            msg = (
                f"In conllu files, all tokens must be in lines\n"
                f"{token} is not in {format_lines_number[token_id]} at the second place"
            )
            self.assertEqual(token, format_lines_number[token_id].split("\t")[1], msg=msg)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    @pytest.mark.lab_6_pipeline
    def test_empty_line_in_to_conllu_method(self) -> None:
        """
        Check number of empty lines in conllu files.
        """
        self.assertEqual(self.conllu_reference[-2:], self.conllu_processed[-2:])

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Define final instructions for TextProcessingPipelineScoreSixReferenceProcess class.
        """
        shutil.rmtree(TEST_PATH)
