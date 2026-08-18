import os
import sys
from src.utils.exceptions import CustomException
import src.utils.logger as logger
import logging

from pydantic import BaseModel,Field,field_validator
from typing import Annotated,Literal
from models.req_source import Source

class Input_System(BaseModel):
    try:
        logger.log_separator("Creating the pydantic class for Input_System")
        id : Annotated[
            str,
            Field(decription="Unique Identifier for the input system")
        ]
        source_name : Annotated[
            str,
            Field(description="Name of the system from which the data is ingested.")
        ]
        description : Annotated[
            str,
            Field(description="Short Description about the nature of the source system.",max_length=300)
        ]
        input_type : Annotated[
            Literal['Database','Flat Files','Intraday Files','File Stream'],
            Field(default = "Flat Files",description="Type of the source system")
        ]
        confidence : Annotated[
            int,
            Field(description="Confidence of the LLM output")
        ]
        source : Annotated[
            Source,
            Field(description="Information about the source from where the information has been extracted")
        ]

        @field_validator('id')
        @classmethod
        def validate_input_prefix(cls,value : str):
            '''
                Validating if the Input has prefix 'INP'
                INP001 -> Valid
                INP-001 -> Valid
                OUT001 -> Invalid
            '''
            if not value.startswith('INP'):
                raise ValueError("Input System should have the prefix INP")
            return value

        logger.log_separator("Creating the pydantic class for Input_System has been completed")
    except Exception as e:
        logging.info(f'ERROR : {e}')
        raise CustomException(e,sys)
