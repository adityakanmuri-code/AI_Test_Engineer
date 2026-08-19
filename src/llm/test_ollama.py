import os
import sys
from src.utils.exceptions import CustomException
import src.utils.logger as logger
import logging

from src.llm.ollama_client import get_llm

def get_response(prompt:str):
    try:
        logger.log_separator(
            f'Generating the response for the prompt : {prompt}'
        )
        llm = get_llm()
        response = llm.invoke(prompt)
        logger.log_separator(
            f'Generated response for the prompt : {prompt} is {response.content}'
        )
        return response.content
    except Exception as e:
        logging.info('ERROR : Unable to generate response for the prompt.')
        raise CustomException(e,sys)