import os
import sys
from src.utils.exceptions import CustomException
import src.utils.logger as logger
import logging

from pydantic import BaseModel,Field,field_validator
from typing import Annotated
from models.req_source import Source

class Output_System(BaseModel):
    try:
        logger.log_separator("Creating the pydantic class for Output_System")
        id : Annotated[
            str,
            Field(description= "Unique Identifier for the Output System")
        ]
        output_name : Annotated[
            str,
            Field(description="Name of the output system")
        ]
        description : Annotated[
            str,
            Field(description="Description about the output system",max_length=300)
        ]
        output_type : Annotated[
            str,
            Field(description='Type of the system that will be consuming the data')
        ]
        confidence : Annotated[
            int,
            Field(description="Confidence level of the output given by the LLM")
        ]
        source : Annotated[
            Source,
            Field(description="Information of the cource from where the information has been extracted")
        ]
        @field_validator('id')
        @classmethod
        def validate_output_prefix(cls,value : str):
            '''
                Validating if the Output System has prefix 'OUT'
                Examples : 
                    OUT001 -> Valid
                    OUT-001 -> Valid
                    BR001 -> Invalid
            '''
            if not value.startswith('OUT'):
                raise ValueError("Output System should have prefix 'OUT'")
            return value
        logger.log_separator("Creating the pydantic class for Output_System has been completed")
    except Exception as e:
        logging.info(f'ERROR : {e}')
        raise CustomException(e,sys)