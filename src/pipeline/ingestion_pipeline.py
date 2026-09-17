import os
import sys
import src.utils.logger as logger
import logging
from src.utils.exceptions import CustomException

from src.ingestion.file_ingestor import File_Ingestion
from src.parser.section_parser import SectionParser
from src.chunking.semantic_chunker import SemanticChunker


class BRDPreprocessingPipeline:

    def __init__(self):
        self.ingestor = File_Ingestion()
        self.parser = SectionParser()
        self.chunker = SemanticChunker(max_characters=4000)

    def preformat_pipeline(self,file_path:str):
        try:
            #1 Text Ingestion and Formatter
            formatted_text = self.ingestor.file_ingestor(file_path=file_path)

            #2 Section Parsing
            sections = self.parser.document_parser(formatted_text)

            #3 Semantic Chunking
            chunks = self.chunker.chunk_sections(sections)

            return chunks
        except Exception as e:
            log_message = f"ERROR: Ingestion Pipeline has failed at {sys._getframe(0).f_code.co_name}"
            logging.info(log_message)
            raise CustomException(log_message,sys)
