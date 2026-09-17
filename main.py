import os
from src.config.settings import Config
from src.pipeline.ingestion_pipeline import PreFormattingPipeline

def main():
    config = Config()
    brd_path = os.path.join(config.get("project","base_dir"),config.get("ingest","brd_path"))

    ingestion_pipeline = PreFormattingPipeline()
    chunks = ingestion_pipeline.preformat_pipeline(brd_path)
    
    for chunk in chunks:
        if chunk.section_id == "9":
                print("="*50)
                print(f"CHUNK_ID : {chunk.chunk_id} SECTION_ID : {chunk.section_id}")
                print(f"CHUNK_TITLE : {chunk.section_title}")
                print(f"CHUNK_CONTENT : {chunk.content}")
                print(f"TOKEN_COUNT : {chunk.token_count}")
    print("="*50)
if __name__ == "__main__":
    main()
