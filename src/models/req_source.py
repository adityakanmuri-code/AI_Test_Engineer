import os
import sys
from src.utils.exceptions import CustomException
import src.utils.logger as logger
import logging

from pydantic import BaseModel,Field
from typing import Annotated,Optional

class Source(BaseModel):
        try:
            logger.log_separator("Creating the pydantic class for Source")
            page : Optional[
                    Annotated[
                            int,
                            Field(description="This field has the page number where the information has been extracted.")
                    ]
            ]
            section : Optional[
                    Annotated[
                            str,
                            Field(description="This field has the section from where the information has been extracted.")
                    ]
            ]
            paragraph : Optional[
                    Annotated[
                            str,
                            Field(description="This field has the paragraph from where the information has been extracted")
                    ]
            ]
            logger.log_separator("Creating the pydantic class for Source has been completed")
        except Exception as e:
              logging.info(f'ERROR: {e}')
              raise CustomException(e,sys)