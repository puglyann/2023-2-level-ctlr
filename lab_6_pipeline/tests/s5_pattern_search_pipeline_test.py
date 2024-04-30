"""
Tests for PatternSearchPipeline.
"""
import json
import shutil
import unittest

import pytest
from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH

from core_utils.article import article
from lab_6_pipeline import pipeline
from lab_6_pipeline.pipeline import CorpusManager, PatternSearchPipeline, StanzaAnalyzer
from lab_6_pipeline.tests.utils import pipeline_test_files_setup


class PatternSearchPipelineTests(unittest.TestCase):
    """
    Tests for PatternSearchPipeline realization.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Define start instructions for PatternSearchPipelineTests class.
        """
        pipeline_test_files_setup()
        shutil.copyfile(PIPE_TEST_FILES_FOLDER / "reference_score_eight_test.conllu",
                        TEST_PATH / "1_stanza_conllu.conllu")

        article.ASSETS_PATH = TEST_PATH
        pipeline.ASSETS_PATH = TEST_PATH

        cls.corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        path_to_article = cls.corpus_manager.get_articles()[1].get_meta_file_path()
        with open(path_to_article, 'r', encoding='utf-8') as meta_file:
            meta = json.load(meta_file)
        print(meta)
        cls.patterns = meta.pop('pattern_matches')
        print(cls.patterns)
        with open(path_to_article, 'w', encoding='utf-8') as meta_file:
            json.dump(meta, meta_file, sort_keys=False, indent=4,
                      ensure_ascii=False, separators=(',', ': '))

        pattern_searcher = PatternSearchPipeline(cls.corpus_manager,
                                                 StanzaAnalyzer(), ("VERB", "NOUN", "ADP"))
        pattern_searcher.run()

    @pytest.mark.mark10
    @pytest.mark.stage_5_pattern_search_pipeline_cheks
    @pytest.mark.lab_6_pipeline
    def test_patterns_are_correct(self) -> None:
        """
        Ensure patterns are matched correctly.
        """
        one_article = self.corpus_manager.get_articles()[1]
        path = one_article.get_meta_file_path()
        print(path)
        with open(path, 'r', encoding='utf-8') as meta_file:
            patterns = json.load(meta_file)['pattern_matches']
        print(self.patterns)
        print(patterns)
        self.assertEqual(self.patterns, patterns,
                         'Patterns were found incorrectly')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Define final instructions for PatternSearchPipelineTests class.
        """
        shutil.rmtree(TEST_PATH)
