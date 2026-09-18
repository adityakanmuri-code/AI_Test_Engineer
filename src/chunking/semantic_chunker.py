import os
import sys
import src.utils.logger as logger
import logging
from src.utils.exceptions import CustomException

from src.config.settings import Config
from src.parser.section_parser import DocumentSection
from src.models.chunk import SemanticChunk
from typing import List
from transformers import AutoTokenizer
from dotenv import load_dotenv
import tiktoken

class SemanticChunker:
    def __init__(self,max_tokens:int = 1000):
        self.max_tokens = max_tokens

    def chunk_sections(self,sections:List[DocumentSection]) -> List[SemanticChunk] :
        try:
            if not sections:
                log_message = "ERROR : Empty text has been passed.Please check the sections in section_parser"
                logging.info(log_message)
                raise ValueError(log_message,sys)
            chunks = []
            for section in sections:
                section_chunks = self.__chunk_section(section)
                chunks.extend(section_chunks)
            return chunks
        except Exception as e:
            log_message = "ERROR: Unable to chunk the data in chunk_sections function"
            logging.info(log_message)
            raise CustomException(log_message,sys)

    def __chunk_section(self,section: DocumentSection) -> List[SemanticChunk]:
        try:
            if not section:
                log_message = "ERROR : Empty text has been passed.Please check the sections in section_parser"
                logging.info(log_message)
                raise ValueError(log_message,sys)

            paragraphs = self.__split_paragraphs(section.content)
            chunks = []
            current_text = ""
            chunk_index = 1

            for paragraph in paragraphs:
                candidate = (current_text+"\n"+paragraph).strip()
                len_candidate = self.__token_counter(candidate)
                if (len_candidate <= self.max_tokens):
                    current_text = candidate
                else:
                    if current_text:
                        chunks.append(
                            self.__create_chunk(section,current_text,chunk_index)
                        )
                        chunk_index += 1
                    current_text = paragraph
            if current_text:
                chunks.append(
                    self.__create_chunk(section,current_text,chunk_index)
                )
            return chunks
        except Exception as e:
            log_message = "ERROR : Unable to chunk the data in __chunk_section functions"
            logging.info(log_message)
            raise CustomException(log_message,sys)

    def __split_paragraphs(self,content: str) -> List[str]:
        try:
            if not content:
                log_message = "ERROR : Empty text has been passed.Please check the sections in __split_paragraphs"
                logging.info(log_message)
                raise ValueError(log_message,sys)
            paragraphs = content.split("\n\n")
            return[paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
        except Exception as e:
            log_message = "ERROR : Unable to split the data in __split_paragraphs functions"
            logging.info(log_message)
            raise CustomException(log_message,sys)        

    def __create_chunk(self,section: DocumentSection,content: str,chunk_index: int) -> SemanticChunk:
        try:
            if not content:
                log_message = "ERROR : Empty text has been passed.Please check the section in __create_chunk"
                logging.info(log_message)
                raise ValueError(log_message,sys)
            chunk_id = (f"{section.section_id}_{chunk_index:03d}")
            token_count = self.__token_counter(content.strip())
            return SemanticChunk(
                chunk_id = chunk_id,
                section_id = section.section_id,
                section_title = section.title,
                content=content,
                chunk_index=chunk_index,
                token_count=token_count
            )
        except Exception as e:
            log_message = "ERROR : Unable to split the data in __split_paragraphs functions"
            logging.info(log_message)
            raise CustomException(log_message,sys)
        
    def __token_counter(self,content:str) -> int:
        try:
            if not content:
                log_message = f"ERROR : Empty Text has been passed in {sys._getframe(0).f_code.co_name}"
                logging.info(log_message)
                raise ValueError(log_message,sys)
            config = Config()
            encoding_name = config.get("models","encoding")
            encoding = tiktoken.get_encoding(encoding_name)
            tokens = encoding.encode(content)
            return len(tokens)
        except Exception as e:
            log_message = f"ERROR : Unable to count the number of tokens in {sys._getframe(0).f_code.co_name}"
            logging.info(log_message)
            raise CustomException(log_message,sys)