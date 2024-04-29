"""
Tests udpipe analyzer.
"""
# pylint: disable=assignment-from-no-return
import unittest

import pytest
from admin_utils.test_params import PIPE_TEST_FILES_FOLDER

from lab_6_pipeline.pipeline import UDPipeAnalyzer


class UDPipeAnalyzerTest(unittest.TestCase):
    """
    Tests udpipe texts analysis.
    """

    def setUp(self) -> None:
        """
        Define start instructions for UDPipeAnalyzerTest class.
        """
        path = PIPE_TEST_FILES_FOLDER / "reference_score_six_test.conllu"
        with path.open("r", encoding="utf-8") as ref:
            self.conllu_reference = ref.read()

        self.texts = [
            "Красивая - мама красиво, училась в ПДД и ЖКУ"
            " по адресу Львовская 10 лет с почтой test ."
        ]
        self.udpipe_analyzer = UDPipeAnalyzer()

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    @pytest.mark.lab_6_pipeline
    def test_xpos_tag_replacement_in_analyzer(self) -> None:
        """
        Ensure that XPOS tags are replaced with '_' in CoNLL-U format.
        """
        conllu_format = self.udpipe_analyzer.analyze(self.texts)
        self.assertEqual(conllu_format[0].split("\t")[4], "_")

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    @pytest.mark.lab_6_pipeline
    def test_headers_are_included(self):
        """
        Check id of sentence.
        """
        conllu_format = self.udpipe_analyzer.analyze(self.texts)[0].format()
        header_line = conllu_format.split("\n")[0]
        self.assertIn("sent_id", header_line)

        self.assertEqual(header_line.split()[-1], "1")

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    @pytest.mark.lab_6_pipeline
    def test_analyze_method(self) -> None:
        """
        Ensure that reference and processed conllu are equal.
        """
        conllu_format = self.udpipe_analyzer.analyze(self.texts)

        for reference, ud_analysis in zip(
            self.conllu_reference.splitlines(), conllu_format[0].splitlines()
        ):
            self.assertEqual(reference, ud_analysis)
