import os
import sys
from src.utils.exceptions import CustomException
import src.utils.logger as logger
import logging

from pydantic import BaseModel,Field,field_validator
from typing import Annotated
from models.req_source import Source
import re

class Business_Rules(BaseModel):
    try:
        logger.log_separator("Creating the pydantic class for Business Rules")
        id : Annotated[
            str,
            Field(description="Unique Identifier of the Business Rules")
        ]
        rule : Annotated[
            str,
            Field(description="Actual Description of the Business Rule",max_length=300)
        ]
        confidence : Annotated[
            int,
            Field(default=0,description="This field is hold the confidence level of the LLM output")
        ]
        source : Annotated[
            Source,
            Field(description="Source information of the requirement")
        ]

        logging.info("Validating if the Business Rule is having 'BR' in prefix")
        @field_validator('id')
        @classmethod
        def validate_businessrule_prefix(cls,value:str):
            '''
                Validating if the Business Rule is having 'BR' in prefix
                Examples:
                    BR001 -> Valid
                    BR-001 -> Valid
                    USR001 -> Invalid
            '''
            pattern = r'^BR'
            if not re.match(pattern,value):
                raise ValueError("Business Rule should start with BR as prefix")
            return value
        logger.log_separator("Creating the pydantic class for Business Rules has been completed.")
    except Exception as e:
        logging.info(f'ERROR : {e}')
        raise CustomException(e,sys)
