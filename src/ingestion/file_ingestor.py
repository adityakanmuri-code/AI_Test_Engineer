import os
import sys
import src.utils.logger as logger
import logging
from src.utils.exceptions import CustomException

from pathlib import Path
from pypdf import PdfReader
from docx import Document
from src.ingestion.text_formatter import TextFormater

class File_Ingestion():
    def file_ingestor(self,file_path:str):
        try:
            file_path = Path(file_path)
            formatter = TextFormater()
            if not file_path.exists():
                log_msg = f'ERROR : File not found in the location {file_path}'
                logging.info(log_msg)
                raise FileNotFoundError(log_msg,sys)
            if file_path.suffix.lower() == '.txt':
                text = file_path.read_text(encoding='utf-8')
            elif file_path.suffix.lower() == '.docx':
                document = Document(file_path)
                text = "\n".join(paragraph.text for paragraph in document.paragraphs)
            elif file_path.suffix.lower() == '.pdf':
                reader = PdfReader(file_path)
                pages = []
                for page in reader.pages:
                    txt = page.extract_text(extraction_mode="layout")
                    if txt:
                        pages.append(txt)
                text = '\n\n'.join(pages)
            else :
                log_message = f"ERROR : Invalid file type {file_path.suffix}"
                logging.info(log_message)
                raise ValueError(log_message,sys)
            text = formatter.normalize_text(text)
            return text
        except Exception as e:
            logging.info('ERROR : Unable to ingest the file')
            raise CustomException(e,sys)