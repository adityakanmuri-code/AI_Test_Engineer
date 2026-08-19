import os
import sys
from src.utils.exceptions import CustomException
import src.utils.logger as logger
import logging
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

def __initiate_model():
    try:
        logger.log_separator('Initiating model')
        load_dotenv()
        model = os.getenv("OLLAMA_GEMMA_MODEL")
        base_url = os.getenv("OLLAMA_BASE_URL")
        temp = os.getenv("OLLAMA_TEMPERATURE")
        logger.log_separator('Model Initiation Completed')
        return(model,base_url,temp)
    except Exception as e:
        logging.info('ERROR: Model not initiated')
        raise CustomException(e,sys)
    

def get_llm() -> ChatOllama:
    try:
        model_name,_,temp = __initiate_model()
        logger.log_separator(f"Fetching the LLM : {model_name}")
        llm = ChatOllama(
            model=model_name,
            temperature=temp
        )
        logger.log_separator(f"Fetching the LLM : {model_name} has been completed")
    except Exception as e:
        logging.info('ERROR : Unable to fetch the LLM')
        raise CustomException(e,sys)
    return llm
