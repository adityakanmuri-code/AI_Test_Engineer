import os
import sys
import src.utils.logger as logger
import logging
from src.utils.exceptions import CustomException
from src.config.settings import Config

import re

class TextFormater:

    def normalize_text(self,text:str) -> str:
        try:
            '''
                This function is used to normalize the text which means the following :
                1. Normalize White Spaces
                2. Normalize excessive blanks
                3. Remove excessive blank lines
                4. Replace unwanted text
                5. Normalize bullet artifacts
                6. Normalize the headings
                    6.1. Normalize heading lines
                    6.2. Normalize section headings
            '''
            if not text:
                log_message = 'ERROR : There is no text to normalize in normalize_text function'
                logging.info(log_message)
                raise ValueError(log_message,sys)
            #-----------------------------------------
            #1. Normalize the white spaces
            #-----------------------------------------
            text = text.replace("\r\n","\n")
            text = text.replace("\f","\n")
            text = text.replace("\r","\n")
            #-----------------------------------------
            #2. Normalize spaces
            #-----------------------------------------
            text = re.sub(
                r"[ \t]+",
                " ",
                text
            )
            #-----------------------------------------
            #3. Remove excessive blank lines
            #-----------------------------------------
            text = re.sub(
                r"\n{3,}",
                "\n\n",
                text
            )
            #-----------------------------------------
            #4. Replace unwanted text
            #-----------------------------------------
            text = self.__replace_text(text)
            #-----------------------------------------
            #5. Normalize bullet artifacts
            #-----------------------------------------
            text = self.__normalize_bullets(text)
            #-----------------------------------------
            #6. Normalize headings
            #-----------------------------------------
            text = self.__normalize_headings(text)
            return text
        except Exception as e:
            log_message = 'ERROR : Text has not been normalized in the normalize_text function'
            logging.info(log_message)
            raise CustomException(log_message,sys)

    #==========================================
    # 4. Replace unawanted text
    #==========================================
    def __replace_text(self,text:str):
        try:
            if not text:
                log_message = "ERROR : Text is empty in the __replace_text function"
                logging.info(log_message)
                raise ValueError(log_message,sys)
            config = Config()
            replace_patterns = config.get("ingest","replace_patterns")
            
            for pattern in replace_patterns:
                text = re.sub(pattern,"",text)
            return text
        except Exception as e:
            log_message = "ERROR : Unable to replace the text in __replace_text"
            logging.info(log_message)
            raise CustomException(log_message,sys)
    #==========================================
    # 5. Normalize Bullets
    #==========================================
    def __normalize_bullets(self,text) -> str:
        try:
            if not text:
                log_message = "ERROR : Text is empty in the __normalize_bullets function"
                logging.info(log_message)
                raise ValueError(log_message,sys)
            text = re.sub(
                r"(?m)^\s*[•●▪◦]\s+",
                "-",
                text
            )
            #Isolated bullet artifacts
            text = re.sub(
                r"(?m)^\s*[•●▪◦]\s*$",
                "",
                text
            )
            return text
        except Exception as e:
            log_message = "ERROR : Unable to normalize the bullets in __normalize_bullets"
            logging.info(log_message)
            raise CustomException(log_message,sys)
    #==========================================
    # 6. Normalize Headings
    #==========================================
    def __normalize_headings(self,text:str) -> str:
        try:
            if not text:
                log_message = 'ERROR : Empty text in the function __normalize_headings'
                logging.info(log_message)
                raise ValueError(log_message,sys)
            lines = text.splitlines()
            normalized_lines = []
            for line in lines:
                line = line.strip()
                if not line:
                    normalized_lines.append("")
                    continue
                normalized_line = self.__normalize_heading_line(line)
                normalized_lines.append(normalized_line)
            text = "\n".join(normalized_lines)
            # Formatting the section headers
            text = self.__format_sections(text)
            return text
        except Exception as e:
            log_message = 'ERROR : Headings have not been normalized in __normalize_headings function'
            logging.info(log_message)
            raise CustomException(log_message,sys)   
    #==========================================
    # 6.1 Normalize Individual Headings
    #==========================================
    def  __normalize_heading_line(self,line:str) -> str:
        try:
            if not line:
                log_message = "ERROR : Text is emtpy in the __normalize_heading_line function"
                logging.info(log_message)
                raise ValueError(log_message,sys)
            match = re.match(
                r"^((?:\d\s*)+)\s*\.\s*(.*)$",
                line
            )
            if match:
                section_number = match.group(1)
                heading_text = match.group(2)

                #Remove spaces between digits
                section_number = re.sub(
                    r"\s+",
                    "",
                    section_number)
                return f"<SECTION id = {section_number} title = {heading_text}>"
            # Subsection
            match = re.match(
                r"^((?:\d\s*)+)\s*\.\s*(\d+)\s+(.*)$",
                line
            )
            if match:
                major_number = re.sub(
                    r"\s+",
                    "",
                    match.group(1)
                )

                minor_number = match.group(2)
                heading_text = match.group(3)
                return(
                    f"{major_number}.{minor_number} "
                    f"{heading_text}"
                )
            return line    
        except Exception as e:
            log_message = "ERROR : Unable to normalize the headings in __normalize_heading_line function"
            logging.info(log_message)
            raise CustomException(log_message,sys)

    #==========================================
    # 6.2 Normalize Individual Headings
    #==========================================
    def __format_sections(self,text:str) -> str:
        try:
            if not text:
                log_message = "ERROR : Empty Text in __format_sections function"
                logging.info(log_message)
                raise ValueError(log_message,sys)
            lines = text.splitlines()
            formatted = []

            for line in lines:
                line = line.strip()

                if not line:
                    formatted.append("")
                    continue

                #-------------------------------------
                # Major Section
                #-------------------------------------
                if re.match(r'<SECTION\s+id\s*=\s*(\d+)\s+title\s*=\s*([^>]+)>',line):
                    formatted.append("")
                    formatted.append("="*60)
                    formatted.append(line)
                    formatted.append("="*60)
                    formatted.append("")

                    continue

                #-------------------------------------
                # Subsection
                #-------------------------------------
                if re.match(r"^\d+\.\d+\s+[A-Z]",line):
                    formatted.append("")
                    formatted.append(line)
                    formatted.append("")

                    continue

                formatted.append(line)

            return "\n".join(formatted)

        except Exception as e:
            log_message = "ERROR : Section Formatting has failed in __format_sections function"
            logging.info(log_message)
            raise CustomException(log_message,sys)
