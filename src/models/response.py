import os 
import sys 
from src.utils.exceptions import CustomException
import src.utils.logger as logger
import logging

from src.models.requirement import Requirement
from src.models.business_rules import Business_Rules
from src.models.actor import Actors
from src.models.input_system import Input_System
from src.models.output_system import Output_System
from pydantic import BaseModel,Field
from typing import Annotated,List

class Response(BaseModel):

    try:
        logger.log_separator("Creating the pydantic class for Response which combines all the models")
        requirement : Annotated[
            List[Requirement],
            Field(description="Collection of all the extracted Requirement")
        ]
        business_rules : Annotated[
            List[Business_Rules],
            Field(description="Collection of all the extracted Business Rules")
        ]
        actor : Annotated[
            List[Actors],
            Field(description="Collection of all the extracted Actors")
        ]
        input_system : Annotated[
            List[Input_System],
            Field(description="Collection of all the extracted Input System")
        ]
        output_system : Annotated[
            List[Output_System],
            Field(description="Collection of all the extracted Output System")
        ]
        logger.log_separator("Creating the pydantic class for Response has been completed")
    except Exception as e:
        logging.info(f"ERROR : {e}")
        raise CustomException(e,sys)
