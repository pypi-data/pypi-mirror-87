#  Copyright (c) 2020 Robert Lieck
from unittest import TestCase
from pathlib import Path

from corpusinterface import config
from corpusinterface.config import init_config, reset_config, load_config, clear_config, summary, \
    get, corpora, \
    set, set_key_value, set_default, \
    add_corpus, delete_corpus, corpus_params, getbool
from corpusinterface.util import CorpusExistsError, CorpusNotFoundError, DuplicateCorpusError, DuplicateDefaultsError, \
    __DEFAULT__, __INFO__, __ROOT__, __PARENT__, __PATH__, __URL__, __ACCESS__, __LOADER__


class Test(TestCase):

    def setUp(self):
        reset_config()

    def tearDown(self):
        reset_config()

    def test_init(self):
        # should always run smoothly
        reset_config()
        # expects default config to be there (should work)
        clear_config(clear_default=True)
        init_config(default=True)
        # expects config file ~/corpora/corpora.ini to be there (should fail on a "clean" system)
        clear_config(clear_default=True)
        self.assertRaises(FileNotFoundError, lambda: init_config(home=True))
        # expects config file corpora.ini in current working directory to be there
        clear_config(clear_default=True)
        self.assertRaises(FileNotFoundError, lambda: init_config(local=True))

    def test_load_config(self):
        # assert default config was loaded and DEFULT section is there
        self.assertTrue(__DEFAULT__ in config.config)
        # assert the test config was not yet loaded
        self.assertFalse('a test section' in config.config)
        # load it
        load_config('tests/test_config.ini', merge_defaults=True)
        # assert it's there now
        self.assertTrue('a test section' in config.config)
        # assert the multi-line value is correctly parsed
        self.assertEqual('test values\nover multiple lines', config.config['a test section']['with'])
        # assert empty values are correctly parsed (also check that capitalisation is ignored)
        self.assertEqual(None, config.config['a test section']['A VALUE THAT IS'])
        # assert references are correctly parsed
        self.assertEqual('backref to test values\nover multiple lines', config.config['a test section']['and'])

        # assert error for duplicate corpora if only merging defaults
        self.assertRaises(DuplicateCorpusError, lambda: load_config('tests/test_config.ini', merge_defaults=True))
        # assert error for duplicate defaults if only merging duplicates
        self.assertRaises(DuplicateDefaultsError, lambda: load_config('tests/test_config.ini', merge_duplicates=True))
        # assert loading works if merging both
        load_config('tests/test_config.ini', merge_duplicates=True, merge_defaults=True)

        # assert both works if there are no duplicates
        load_config('tests/test_corpora.ini')

    def test_get_methods(self):
        # init and load test corpora
        reset_config('tests/test_corpora.ini')
        root = Path("~/corpora").expanduser()
        # check get method returns the unprocessed values
        self.assertEqual(None, get("Test Corpus", __INFO__))
        self.assertEqual(root, get("Test Corpus", __ROOT__))
        self.assertEqual(root / "Test Corpus", get("Test Corpus", __PATH__))
        self.assertEqual(None, get("Test Corpus", __PARENT__))
        self.assertEqual(None, get("Test Corpus", __ACCESS__))
        self.assertEqual(None, get("Test Corpus", __URL__))
        self.assertEqual("FileCorpus", get("Test Corpus", __LOADER__))

        # check summary
        self.assertEqual("[Test Corpus]\n"
                         f"    {__INFO__}: None\n"
                         f"    {__ROOT__}: {root}\n"
                         f"    {__PATH__}: {root / 'Test Corpus'}\n"
                         f"    {__PARENT__}: None\n"
                         f"    {__ACCESS__}: None\n"
                         f"    {__URL__}: None\n"
                         f"    {__LOADER__}: FileCorpus", summary("Test Corpus"))
        self.assertEqual("[Test Corpus]\n"
                         f"    {__INFO__}: None\n"
                         f"    {__ROOT__}: ~/corpora\n"
                         f"    {__PATH__}: None\n"
                         f"    {__PARENT__}: None\n"
                         f"    {__ACCESS__}: None\n"
                         f"    {__URL__}: None\n"
                         f"    {__LOADER__}: FileCorpus", summary("Test Corpus", raw=True))

        # check corpus_params returns iterator over processed values
        self.assertEqual(sorted([(__INFO__, "Some info"),
                                 (__ROOT__, root / "Test Corpus"),
                                 (__PATH__, root / "Test Corpus" / "Test Sub-Corpus"),
                                 (__PARENT__, "Test Corpus"),
                                 (__ACCESS__, None),
                                 (__URL__, None),
                                 (__LOADER__, "FileCorpus")]),
                         sorted(list(corpus_params("Test Sub-Corpus"))))

        # corpus_params with unknown corpus raises
        self.assertRaises(CorpusNotFoundError, lambda: list(corpus_params("Unknown Corpus")))

        # check default root
        global_root = Path('~/corpora').expanduser()
        self.assertEqual(global_root, get("Test Corpus", __ROOT__))
        # check warning for relative root
        with self.assertWarns(RuntimeWarning):
            relative_root = Path('some/relative/path')
            self.assertFalse(relative_root.is_absolute())
            self.assertEqual(relative_root, get("Test Relative Root", __ROOT__))
        # check root for sub- and sub-sub-corpora
        self.assertEqual(global_root / "Test Corpus", get("Test Sub-Corpus", __ROOT__))
        self.assertEqual(global_root / "Test Corpus" / "Test Sub-Corpus", get("Test Sub-Sub-Corpus", __ROOT__))

        # check path for normal corpus
        self.assertEqual(global_root / "Test Corpus", get("Test Corpus", __PATH__))
        # check relative path
        self.assertEqual(global_root / "some/relative/path", get("Test Relative Path", __PATH__))
        # check absolute path
        self.assertEqual(Path("/some/absolute/path"), get("Test Absolute Path", __PATH__))
        self.assertEqual(Path("~/some/absolute/path").expanduser(), get("Test Absolute Path Home", __PATH__))
        
        # check path for sub- and sub-sub-corpora
        self.assertEqual(global_root / "Test Corpus" / "Test Sub-Corpus", get("Test Sub-Corpus", __PATH__))
        self.assertEqual(global_root / "Test Corpus" / "Test Sub-Corpus" / "Test Sub-Sub-Corpus",
                         get("Test Sub-Sub-Corpus", __PATH__))

        # check sub-corpora with relative and absolute path
        self.assertEqual(global_root / "some/relative/path", get("Test Relative Sub-Path", __PATH__))
        self.assertEqual(Path("/some/absolute/path"), get("Test Absolute Sub-Path", __PATH__))
        self.assertEqual(Path("~/some/absolute/path").expanduser(), get("Test Absolute Sub-Path Home", __PATH__))

    def test_add_get_delete_corpora(self):
        # clear config
        clear_config()
        # some corpora
        corpus_list = ["First Corpus", "Second Corpus", "Third Corpus"]
        # add them one by one
        for idx, corpus in enumerate(corpus_list):
            # add corpus
            add_corpus(corpus)
            # check get corpora
            self.assertEqual(corpus_list[:idx + 1], list(corpora()))
        # delete them one by one
        for idx, corpus in enumerate(corpus_list):
            # delete corpus
            delete_corpus(corpus)
            # check get corpora
            self.assertEqual(corpus_list[idx + 1:], list(corpora()))

        # delete non-existent corpus
        self.assertRaises(CorpusNotFoundError, lambda: delete_corpus("Does not exist"))
        delete_corpus("Does not exist", not_exists_ok=True)

    def test_set_and_add_corpus(self):
        # add corpus
        self.assertFalse("XXX" in config.config)
        add_corpus("XXX")
        self.assertTrue("XXX" in config.config)

        # raise when existing corpus is reset
        self.assertRaises(CorpusExistsError, lambda: add_corpus("XXX"))

        # setting non-string corpus warns
        with self.assertWarns(RuntimeWarning):
            self.assertFalse(1 in config.config)
            add_corpus(1)
            self.assertFalse(1 in config.config)
            self.assertTrue("1" in config.config)

        # set value in section to None
        self.assertFalse("YYY" in config.config["XXX"])
        set("XXX", YYY=None)
        self.assertTrue("YYY" in config.config["XXX"])
        self.assertEqual(None, config.config["XXX"]["YYY"])
        self.assertNotEqual('None', config.config["XXX"]["YYY"])

        # warning for non-string keys and values (except None for value)
        with self.assertWarns(RuntimeWarning):
            set_key_value("XXX", key=1, value=None)
            self.assertEqual(None, get("XXX", 1))
        with self.assertWarns(RuntimeWarning):
            set_key_value("XXX", "1", 2)
            self.assertNotEqual(2, get("XXX", 1))
            self.assertEqual("2", get("XXX", 1))

        # raise if corpus not found
        self.assertRaises(CorpusNotFoundError, lambda: set_key_value("Does not exist", key="key", value="value"))

        # set value in section
        set("XXX", YYY="ZZZ")
        self.assertEqual("ZZZ", config.config["XXX"]["YYY"])

        # set value in DEFAULT
        set_default(AAA=None)
        self.assertEqual(None, get("XXX", "AAA"))
        set_default(AAA="BBB")
        self.assertEqual("BBB", get("XXX", "AAA"))

        # add corpus
        add_corpus("new corpus", key1="val1", key2="val2")
        self.assertEqual("val1", get("new corpus", "key1"))
        self.assertEqual("val2", get("new corpus", "key2"))
        # add existing corpus raises
        self.assertRaises(CorpusExistsError, lambda: add_corpus("new corpus"))

    def test_getboolean(self):
        for val in ['1', 'yes', 'true', 'on', 1, True]:
            self.assertTrue(getbool(val))
        for val in ['0', 'no', 'false', 'off', 0, False]:
            self.assertFalse(getbool(val))
        for val in [123, "lkj"]:
            self.assertRaises(ValueError, lambda: getbool(val))

    def test_clear(self):
        # check that the default section is there
        self.assertEqual([config.__DEFAULT__], list(config.config))
        # clear config (don't remove default)
        clear_config()
        # check only config section is left
        self.assertEqual([config.__DEFAULT__], list(config.config))
        # check its not empty
        self.assertGreater(len(list(config.config[config.__DEFAULT__])), 0)
        # now also clear default
        clear_config(clear_default=True)
        # check its empty now
        self.assertEqual(len(list(config.config[config.__DEFAULT__])), 0)
        # reset
        reset_config()
        # check that there is the default section in config again
        self.assertEqual([config.__DEFAULT__], list(config.config))

    def test_summary(self):
        clear_config(clear_default=True)
        load_config("tests/test_config.ini")
        self.assertEqual(f"[{__DEFAULT__}]\n"
                         "    default_key: default_value\n"
                         "\n"
                         "[a test section]"
                         "\n    with: test values\n"
                         "over multiple lines\n"
                         "    a value that is: None\n"
                         "    and: backref to test values\n"
                         "over multiple lines\n"
                         "    default_key: default_value", summary())
