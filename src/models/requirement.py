import os
import sys
from src.utils.exceptions import CustomException
import src.utils.logger as logger
import logging


from pydantic import BaseModel,Field,field_validator
from typing import Literal,Annotated
from models.req_source import Source
import re

class Requirement(BaseModel):
    try:
        logger.log_separator("Creating the pydantic class for Requirement")
        id : Annotated[
            str,
            Field(description="The field is used to provide a unique identifier for the requirement")
        ]
        category : Annotated[
            Literal['Functional','Non-Functional','Business'],
            Field(default='Business',description="This field is used to identify the category of the requirement")
        ]
        priority : Annotated[
            Literal['High','Medium','Low'],
            Field(default='Medium',description="This field is used to identify the priority of the requirement")
        ]
        complexity : Annotated[
            Literal['Complex','Medium','Simple'],
            Field(default='Medium',description="This field is used to identify the complexity of the requirement")
        ]
        requirement : Annotated[
            str,
            Field(description="This field is used to describe the requirement",max_length=300)
        ]
        confidence : Annotated[
            int,
            Field(default=0,description="This field is hold the confidence level of the LLM output")
        ]

        source: Annotated[
            Source,
            Field(description="Source information of the requirement")
        ]
        
        logging.info("Validating if the requirement id has 'REQ' as prefix")
        @field_validator('id')
        @classmethod
        def validate_req_prefix(cls,value: str):
            '''
                Validate that the requirement ID starts with 'REQ'
                Examples :
                    REQ-001 -> Valid
                    REQ001 -> Valid
                    BR001 -> Invalid
                    US001 -> Invalid
            '''
            pattern = r"^REQ"
            if not re.match(pattern,value):
                raise ValueError(
                    "Requirement ID must be in the format 'REQ-<number>'"
                )
            return value
        
        logger.log_separator("Creating the pydantic class for Requirement has been completed.")
    except Exception as e:
        logging.error(f'ERROR : {e}')
        raise CustomException(e,sys)
    