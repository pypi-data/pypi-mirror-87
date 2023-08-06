import logging
import os
import pathlib
from typing import List
from urllib.parse import urlparse
from urllib.request import urlopen

import regex as re
import stanza
from bs4 import BeautifulSoup
from langdetect import detect
from nesteddictionary import NestedDict

from texta_mlp.document import Document
from texta_mlp.entity_mapper import EntityMapper
from texta_mlp.exceptions import LanguageNotSupported


DEFAULT_LANG_CODES = ("et", "ru", "en")
USE_GPU_FOR_STANZA = True

ENTITY_MAPPER_DATA_URLS = (
    "https://git.texta.ee/texta/texta-resources/-/raw/master/entity_mapper/addresses.json",
    "https://git.texta.ee/texta/texta-resources/-/raw/master/entity_mapper/companies.json"
)

CONCATENATOR_DATA_FILES = (
    "https://git.texta.ee/texta/texta-resources/-/raw/master/concatenator/months.txt",
    "https://git.texta.ee/texta/texta-resources/-/raw/master/concatenator/not_entities.txt",
    "https://git.texta.ee/texta/texta-resources/-/raw/master/concatenator/space_between_not_ok.txt",
)

DEFAULT_RESOURCE_DIR = os.path.join(os.getcwd(), "data")
SUPPORTED_ANALYZERS =  (
    "lemmas",
    "pos_tags",
    "transliteration",
    "ner",
    "addresses",
    "emails",
    "phone_strict",
    "entities",
    "namemail",
    "bounded"
)


class MLP:

    def __init__(self, language_codes=DEFAULT_LANG_CODES, default_language_code=DEFAULT_LANG_CODES[0],
                 use_default_language_code=True, resource_dir: str = DEFAULT_RESOURCE_DIR, logging_level="error"):


        self.supported_langs = language_codes
        self.logger = logging.getLogger()
        self.default_lang = default_language_code
        self.use_default_lang = use_default_language_code
        self.langs_to_transliterate = ["ru"]
        self.resource_dir = resource_dir

        self.resource_dir_pathlib = pathlib.Path(resource_dir)
        self.not_entities_path = self.resource_dir_pathlib / "concatenator" / "not_entities.txt"
        self.space_between_not_ok_path = self.resource_dir_pathlib / "concatenator" / "space_between_not_ok.txt"
        self.months_path = self.resource_dir_pathlib / "concatenator" / "months.txt"

        self.download_stanza_resources(self.resource_dir, self.supported_langs, logger=self.logger)
        self.download_entity_mapper_resources(self.resource_dir, logger=self.logger)
        self.download_concatenator_resources(self.resource_dir, logger=self.logger)

        self.stanza_pipelines = self._load_stanza_pipelines(logging_level)
        self.entity_mapper = self._load_entity_mapper()
        self.loaded_entity_files = []

        self.not_entities = self._load_not_entities()
        self.space_between_not_ok = self._load_space_between_not_ok()
        self.months = self._load_months()
        self.concat_resources = {
            "months": self.months,
            "space_between_not_ok": self.space_between_not_ok,
            "not_entities": self.not_entities
        }


    @staticmethod
    def download_stanza_resources(resource_dir: str, supported_langs: List[str], logger=None):
        """
        Downloads Stanza resources if not present in resources directory.
        By default all is downloaded into data directory under package directory.
        """
        stanza_resource_path = pathlib.Path(resource_dir) / "stanza"
        if logger: logger.info(f"Downloading Stanza models into the directory: {str(stanza_resource_path)}")
        stanza_resource_path.mkdir(parents=True, exist_ok=True)  # Create the directories with default permissions including parents.
        for language_code in supported_langs:
            # rglob is for recursive filename pattern matching, if it matches nothing
            # then the necessary files do not exist and we should download them.
            if not list(stanza_resource_path.rglob("{}*".format(language_code))):
                stanza.download(language_code, str(stanza_resource_path))


    @staticmethod
    def download_entity_mapper_resources(resource_dir: str, logger=None, entity_mapper_urls: tuple = ENTITY_MAPPER_DATA_URLS):
        entity_mapper_resource_path = pathlib.Path(resource_dir) / "entity_mapper"
        entity_mapper_resource_path.mkdir(parents=True, exist_ok=True)
        for url in entity_mapper_urls:
            file_name = urlparse(url).path.split("/")[-1]
            file_path = entity_mapper_resource_path / file_name
            if not file_path.exists():
                if logger: logger.info(f"Downloading entity mapper file {file_name} into the directory: {url}")
                response = urlopen(url)
                content = response.read().decode()
                with open(file_path, "w", encoding="utf8") as fh:
                    fh.write(content)


    def _load_entity_mapper(self):
        # create Entity Mapper instance
        data_dir = os.path.join(self.resource_dir, "entity_mapper")
        data_files = [os.path.join(data_dir, path) for path in os.listdir(data_dir)]
        self.loaded_entity_files = data_files
        return EntityMapper(data_files)


    @staticmethod
    def normalize_input_text(text: str) -> str:
        """
        Normalizes input text so it won't break anything.
        :param: str text: Input text.
        :return: Normalized text.
        """
        text = str(text)
        bs = BeautifulSoup(text, "lxml")
        text = bs.get_text(' ')  # Remove html.
        text = re.sub('(\n){2,}', '\n\n', text)
        text = re.sub('( )+', ' ', text)
        text = text.strip()
        return text


    def detect_language(self, text):
        """
        Detects language of input text.
        If language not in supported list, language is defaulted or exception raised.
        :param: str text: Text to be analyzed.
        :return: Language code.
        """
        # try to detect language
        try:
            lang = detect(text)
        except:
            lang = None
        # check if detected language is supported
        if lang not in self.supported_langs:
            if self.use_default_lang:
                lang = self.default_lang
            else:
                raise LanguageNotSupported("Detected language is not supported: {}.".format(lang))
        return lang


    def generate_document(self, raw_text, analyzers, json_object=None, doc_paths="text", lang=None):
        processed_text = MLP.normalize_input_text(raw_text)
        # detect language
        if not lang:
            lang = self.detect_language(processed_text)
        # check if processed text not empty
        if processed_text:
            # Separate all the words into a separate list.
            words = self._get_stanza_tokens(lang, processed_text)
            entities = self._get_stanza_ner(lang, processed_text)
        else:
            words = []
            entities = []

        document = Document(
            original_text=processed_text,
            dominant_language_code=lang,
            stanza_words=words,
            stanza_entities=entities,
            analyzers=analyzers,
            json_doc=json_object,
            doc_path=doc_paths,
            entity_mapper=self.entity_mapper,
            concat_resources=self.concat_resources
        )
        return document


    @staticmethod
    def _load_analyzers(analyzers, supported_analyzers):
        if analyzers == ["all"]:
            return [analyzer for analyzer in supported_analyzers if analyzer != "all"]
        return [analyzer for analyzer in analyzers if (analyzer in supported_analyzers and analyzer != "all")]


    def _get_stanza_tokens(self, lang: str, raw_text: str):
        # This is a HACK to compensate Stanza errors in tokenizing Russian phone numbers
        # Replaces "-" between digits to "_" so it won't be split into separate tokens (1/2)
        if lang == "ru":
            raw_text = re.sub(r"(?<=\d)-(?=\d)", "_", raw_text)

        # Separate all the words into a separate list.

        pipeline = self.stanza_pipelines[lang](raw_text)

        words = []
        for sentence in pipeline.sentences:
            for word in sentence.words:
                # Russian HACK (2/2)
                # replaces back "#" to "-" between digits.
                if lang == "ru":
                    word.text = re.sub(r"(?<=\d)_(?=\d)", "-", word.text)
                words.append(word)
        return words


    def _get_stanza_ner(self, lang: str, raw_text: str):
        pipeline = self.stanza_pipelines[lang](raw_text)
        entities = []
        for sentence in pipeline.sentences:
            for entity in sentence.entities:
                entities.append(entity)
        return entities


    def _load_stanza_pipelines(self, logging_level):
        """
        Initializes Stanza Pipeline objects all at once to save time later.
        """
        stanza_pipelines = {}
        for lang in self.supported_langs:
            stanza_resource_path = pathlib.Path(self.resource_dir) / "stanza"
            stanza_pipelines[lang] = stanza.Pipeline(
                lang=lang,
                processors="tokenize,lemma,pos,ner",
                dir=str(stanza_resource_path),
                use_gpu=USE_GPU_FOR_STANZA,
                logging_level=logging_level
            )
        return stanza_pipelines


    def process(self, raw_text: str, analyzers: list = ["all"], lang=None):
        """
        Processes raw text.
        :param: raw_text str: Text to be processed.
        :param: analyzers list: List of analyzers to be used.
        :return: Processed text as document ready for Elastic.       
        """
        loaded_analyzers = self._load_analyzers(analyzers, SUPPORTED_ANALYZERS)
        document = self.generate_document(raw_text, loaded_analyzers, lang=lang)
        if document:
            for analyzer in loaded_analyzers:
                # For every analyzer, activate the function that processes it from the
                # document class.
                getattr(document, analyzer)()
            return document.to_json()
        else:
            return None


    def lemmatize(self, raw_text: str, lang=None):
        """
        Lemmatizes input text.
        :param: raw_text str: Text to be lemmatized.
        :return: Lemmatized string.
        """
        document = self.process(raw_text, analyzers=["lemmas"], lang=lang)
        return document["text"]["lemmas"]


    def process_docs(self, docs: List[dict], doc_paths: List[str], analyzers=["all"]):
        """
        :param docs: Contains tuples with two dicts inside them, the first being the document to be analyzed and the second is the meta information that corresponds to the document for transport purposes later on.
        :param doc_paths: Dot separated paths for how to traverse the dict for the text value you want to analyze.
        :param analyzers: List of strings to determine which procedures you want your text to be analyzed with.
        :return: List of dictionaries where the mlp information is stored inside texta_facts and the last field of the doc_path in the format {doc_path}_mlp.
        """
        # Container for keeping the tuples of the doc and meta pairs.
        container = []
        for document in docs:
            for doc_path in doc_paths:
                # Traverse the (possible) nested dicts and extract their text values from it as a list of strings.
                # Since the nested doc_path could lead to a list there are multiple pieces of text which would be needed to process.
                doc_texts = NestedDict(document).get(doc_path)
                doc_texts = [doc_texts] if isinstance(doc_texts, str) else doc_texts
                for raw_text in doc_texts:
                    analyzers = self._load_analyzers(analyzers, SUPPORTED_ANALYZERS)
                    doc = self.generate_document(raw_text, analyzers, document, doc_paths=doc_path)
                    if doc:
                        for analyzer in analyzers:
                            # For every analyzer, activate the function that processes it from the
                            # document class.
                            getattr(doc, analyzer)()
                        data = doc.document_to_json()
                        container.append(data)
                    else:
                        container.append(None)

        return container


    @staticmethod
    def download_concatenator_resources(resource_dir: str, logger):
        concat_resource_dir = pathlib.Path(resource_dir) / "concatenator"
        concat_resource_dir.mkdir(parents=True, exist_ok=True)
        for url in CONCATENATOR_DATA_FILES:
            file_name = urlparse(url).path.split("/")[-1]
            file_path = concat_resource_dir / file_name
            if not file_path.exists():
                if logger: logger.info(f"Downloading concatenator file {file_name} into the directory: {url}")
                response = urlopen(url)
                content = response.read().decode()
                with open(file_path, "w", encoding="utf8") as fh:
                    fh.write(content)


    def _load_not_entities(self):
        not_entities = list()
        with open(self.not_entities_path, "r", encoding="UTF-8") as file:
            for line in file.readlines():
                not_entities += [line.strip().lower()]
        return not_entities


    def _load_space_between_not_ok(self):
        space_between_not_ok = list()
        with open(self.space_between_not_ok_path, "r", encoding="UTF-8") as file:
            for line in file.readlines():
                space_between_not_ok += [line.strip()]

        return re.compile("|".join(space_between_not_ok))


    def _load_months(self):
        months = list()
        with open(self.months_path, "r", encoding="UTF-8") as file:
            for line in file.readlines():
                months += [line.strip()]
        return months
