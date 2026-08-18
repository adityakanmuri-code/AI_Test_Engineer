import os
import sys
from src.utils.exceptions import CustomException
import src.utils.logger as logger
import logging

from pydantic import BaseModel,Field,field_validator
from models.req_source import Source
from typing import Annotated

class Actors(BaseModel):
    try:
        logger.log_separator("Creating the pydantic class for Actors")
        id : Annotated[
            str,
            Field(description="Unique Identfier for Actor")
        ]
        name : Annotated[
            str,
            Field(description="Name of the Actor(Entity or individual who interacts with the application)")
        ]
        description : Annotated[
            str,
            Field(description="Description about how the actor interacts with the system")
        ]
        confidence : Annotated[
            int,
            Field(description="Confidence of the response giving by LLM")
        ]
        source : Annotated[
            Source,
            Field(description="Source information of the extracted information")
        ]
        @field_validator('id')
        @classmethod
        def validate_actor_prefix(cls,value:str):
            '''
                Validating if the Actor ID has the prefix 'ACT'
                Examples:
                ACT001 -> Valid
                ACT-001 -> Valid
                BR001 -> Invalid
            '''
            if not value.startswith('ACT'):
                raise ValueError("Actor should start with the prefix ACT")
            return value
        logger.log_separator("Creating the pydantic class for Actors has been completed.")
    except Exception as e:
        logging.info(f'ERROR : {e}')
        raise CustomException(e,sys)
        