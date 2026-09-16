import os
import sys
import src.utils.logger as logger
import logging
from src.utils.exceptions import CustomException

from dataclasses import dataclass
from typing import Dict,List,Optional
import re

@dataclass
class DocumentSection:
    """
    Represents one major section of the BRD
    """
    section_id : str
    title : str
    content : str
    level : int = 1

class SectionParser:
    def document_parser(self,text:str) -> List[DocumentSection]:
        """
        Parse a formatted BRD into major sections.

        The parser identifies:
            1. Major Numbered Sections
            2. Appendix Sections
        """
        try:
            if not text:
                log_message = "ERROR : Empty text is passed in document_parser function."
                logging.info(log_message)
                raise ValueError(log_message,sys)
            
            lines = text.splitlines()
            sections : List[DocumentSection] = []
            current_section : Optional[DocumentSection] = None
            for raw_line in lines:
                line = raw_line.strip()
                if not line:

                    if current_section:
                        current_section.content += "\n"
                    continue
                #----------------------------------------
                # Ignore formatter separator lines
                #---------------------------------------- 
                if self.__is_seperator(line):
                    continue                  
                #----------------------------------------
                # New Major Section
                #----------------------------------------
                section_header = self.__detect_major_section(line)
                appendix_header = self.__detect_appendix(line)

                if section_header:
                    if current_section:
                        current_section.content = (current_section.content.strip())
                        sections.append(current_section)
                    section_id,title = section_header

                    current_section = DocumentSection(
                        section_id = section_id,
                        title = title,
                        content = "",
                        level = 1
                    )
                    continue
                #----------------------------------------
                # New Appendix Section
                #----------------------------------------
                if appendix_header:
                    if current_section:
                        current_section.content = (current_section.content.strip())
                        sections.append(current_section)

                    section_id,title = appendix_header

                    current_section = DocumentSection(
                        section_id = section_id,
                        title = title,
                        content="",
                        level=1
                    )
                    continue
                #----------------------------------------
                # Normal Content
                #----------------------------------------
                if current_section:
                    current_section.content += (line+ "\n")

            #--------------------------------------------
            #Save Final Section
            #--------------------------------------------
            if current_section:
                current_section.content = (current_section.content.strip())
                sections.append(current_section)
            return sections
        except Exception as e:
            log_message = "ERROR : Text has not been parsed in document_parser function."
            logging.info(log_message)
            raise CustomException(log_message,sys)
    #==============================================
    # MAJOR SECTION DETECTION
    #==============================================
    def __detect_major_section(self,line : str) -> Optional[tuple[str,str]] :
        try:
            if not line :
                log_message = "ERROR : Empty line has been passed in __detect_major_section function."
                logging.info(log_message)
                raise ValueError(log_message,sys)
            
            pattern = r"<SECTION\s+id\s*=\s*(\d+)\s+title\s*=\s*([^>]+)>"
            match = re.match(pattern,line)

            if not match:
                return None

            section_id = match.group(1)
            title = match.group(2).strip()

            if not self.__identify_section_title(title):
                return None

            return section_id,title
        except Exception as e:
            log_message = "ERROR : Text has not been parsed in __detect_major_section function."
            logging.info(log_message)
            raise CustomException(log_message,sys)

    #==========================================
    # SECTION TITLE VALIDATION
    #==========================================
    def __identify_section_title(self,title:str) -> bool:
        try:
            if not title :
                log_message = "ERROR : Empty title has been passed in __identify_section_title function."
                logging.info(log_message)
                raise ValueError(log_message,sys)
            known_titles = [
                "document purpose",
                "business background",
                "business objectives",
                "scope",
                "stakeholders",
                "source systems",
                "target systems",
                "business requirements",
                "business rules",
                "source-to-target transformation requirements",
                "data quality requirements",
                "incremental load requirements",
                "slowly changing dimension requirements",
                "reject and exception handling",
                "reconciliation requirements",
                "audit requirements",
                "batch processing requirements",
                "etl testing requirements",
                "critical banking data elements",
                "regulatory and compliance considerations",
                "security and data access requirements",
                "data retention requirements",
                "performance and sla requirements",
                "error handling requirements",
                "restart and recovery requirements",
                "acceptance criteria",
                "sample etl test scenarios",
                "business rules to test",
                "requirements traceability",
                "requirement identification structure",
                "expected etl test deliverables",
                "entry criteria",
                "exit criteria",
                "assumptions",
                "dependencies",
                "risks",
                "business acceptance",
            ]
            normalized_title = (re.sub(r"\s+"," ",title.lower()).strip())

            return any(normalized_title.startswith(known_title) for known_title in known_titles)
        except Exception as e:
            log_message = "ERROR : Title has not been parsed in __identify_section_title function."
            logging.info(log_message)
            raise CustomException(log_message,sys)

    #==========================================
    # APPENDIX DETECTION
    #==========================================
    def __detect_appendix(self,line:str) -> Optional[tuple[str,str]]:
        '''
            This function is used to detect appendix related headings
            Example:
                1. Appendix A - Source to Target Mapping
                2. Appendix B - Banking Domain Terminologies
        '''
        try:
            if not line:
                log_message = "ERROR : Empty line has been passed in __detect_appendix function."
                logging.info(log_message)
                raise ValueError(log_message,sys)

            pattern = r"^Appendix\s+([A-Z])\s*[—–-]\s*(.+)$"
            match = re.match(
                pattern,
                line.strip(),
                re.IGNORECASE
            )

            if not match:
                return None

            appendix_letter = match.group(1).strip()
            title = match.group(2).strip()

            section_id = f'Appendix {appendix_letter}'

            return section_id,title
        except Exception as e:
            log_message = "ERROR : Appendix has not been parsed in __detect_appendix function."
            logging.info(log_message)
            raise CustomException(log_message,sys)

    #==========================================
    # DICTIONARY REPRESENTATION
    #==========================================    
    def to_dict(self,sections : List[DocumentSection]) -> Dict[str,str]:
        return {
            section.section_id:(section.content) for section in sections
        }

    #==========================================
    # DICTIONARY REPRESENTATION
    #==========================================  
    def __is_seperator(self,line:str) -> bool:
        if not line:
            return False
        return bool(re.fullmatch(r"={10,}",line.strip()))    