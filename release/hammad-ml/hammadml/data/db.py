from hammadpy.core import Text
from whoosh import index as whoosh_index
from whoosh.analysis import StandardAnalyzer, FancyAnalyzer, LanguageAnalyzer, KeywordAnalyzer
from whoosh.fields import Schema, TEXT, ID, KEYWORD
from whoosh.qparser import QueryParser, QueryParserError, MultifieldParser
import pandas as pd
from typing import Optional, List, Dict
import pathlib as pl
import uuid

"""
hammadml.data.db
Author: Hammad Saeed
Contact: hammad@supportvectors.com
Website: python.hammad.fun

This module contains the Database class which provides a simple interface for creating and searching a Whoosh search index.

Classes:
    Database: This class provides a simple interface for creating and searching a Whoosh search index.

Methods:
    create(self, dir: Optional[str] = None, schema: Optional[Schema] = None, analyzer: Optional[str] = "standard"): Creates a new index.
    add(self, documents: List[Dict[str, str]], shared_id: Optional[bool] = False): Adds documents to the index.
    search(self, query: str, fields: Optional[List[str]] = None): Searches the index.
"""

#==============================================================================#

class Database:
    def __init__(self):
        """
        Initializes the search index.
        """
        self.text = Text()

    def create(self, dir: Optional[str] = None, schema: Optional[Schema] = None, analyzer: Optional[str] = "standard"):
        """
        Creates a new index.

        Args:
            dir (Optional[str]): Path to the index directory.
            schema (Optional[Schema]): A Whoosh Schema to define the index structure.
            analyzer (Optional[str]): The type of analyzer to use. Options are "standard", "fancy", "language", and "keyword".

        Returns:
            None
        """
        if schema is None and analyzer == "standard":
            self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=StandardAnalyzer(), stored=True))
        elif schema is None and analyzer == "fancy":
            self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=FancyAnalyzer(), stored=True))
        elif schema is None and analyzer == "language":
            self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=LanguageAnalyzer(), stored=True))
        elif schema is None and analyzer == "keyword":
            self.schema = Schema(id=ID(stored=True), content=KEYWORD(analyzer=KeywordAnalyzer(), stored=True))
        else:
            self.schema = schema
        if dir is None:
            self.index_dir = "./databases/db"
            if not pl.Path(self.index_dir).exists():
                pl.Path(self.index_dir).mkdir(parents=True, exist_ok=True)
        else:
            self.index_dir = dir
            if not pl.Path(self.index_dir).exists():
                pl.Path(self.index_dir).mkdir(parents=True, exist_ok=True)
        self.ix = whoosh_index.create_in(self.index_dir, self.schema)

    def load_dataset(self, path: str, id_column: str, content_column: str):
        """
        Adds documents to an index, by reading a dataset.

        Args:
            path (str): The path to the dataset.
            id_column (str): The name of the column containing the document IDs.
            content_column (str): The name of the column containing the document content.
        """
        if not self.ix:
            self.create()
        df = pd.read_csv(path)
        writer = self.ix.writer()
        for i, row in df.iterrows():
            writer.add_document(id=row[id_column], content=row[content_column])
        writer.commit()

    def load_docs(self, dir: str, type: str):
        """
        Adds documents to an index, by reading a directory of files.

        Args:
            dir (str): The directory to read from.
            type (str): The type of documents to read. Options are "txt", "pdf".
        """

    def add(self, documents: List[Dict[str, str]], shared_id: Optional[bool] = False):
        """
        """
        if shared_id:
            if not self.ix:
                self.create()
            writer = self.ix.writer()
            for doc in documents:
                writer.add_document(id="shared", content=doc["content"])
            writer.commit()
        if not self.ix:
            self.create()
        writer = self.ix.writer()
        for doc in documents:
            if 'id' not in doc:
                id = str(uuid.uuid4())
            else:
                id = doc['id']
            writer.add_document(id=id, content=doc["content"])
        writer.commit()

    def search(self, query: str, fields: Optional[List[str]] = None):
        """
        Searches the index.

        Args:
            query (str): The query to search for.
            fields (Optional[List[str]]): A list of fields to search in.

        Returns:
            List[Dict[str, str]]: A list of search results.
        """
        if not self.ix:
            self.create()
        with self.ix.searcher() as searcher:
            if fields is None:
                parser = QueryParser("content", schema=self.schema)
            else:
                parser = MultifieldParser(fields, schema=self.schema)
            try:
                q = parser.parse(query)
                results = searcher.search(q)
                return results
            except QueryParserError as e:
                return self.text.say(message=f"QueryParserError: {e}", color="red", bold=True)
    
#==============================================================================#
    
if __name__ == "__main__":

    db = Database()
    db.create()
    db.add([{"content": "This is a test document."}, {"content": "This is another test document."}])
    db.search("test")