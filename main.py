import os
from src.ingestion.file_ingestor import File_Ingestion
from src.config.settings import Config
from src.parser.section_parser import SectionParser

def main():
    config = Config()
    ingest = File_Ingestion()
    brd_path = os.path.join(config.get("project","base_dir"),config.get("ingest","brd_path"))
    text = ingest.file_ingestor(brd_path)

    #Parsing Sections
    parser = SectionParser()
    sections = parser.document_parser(text)

    for section in sections:
        if section.section_id == "8":
            print(f"SECTION CONTENT : {section.content}")
if __name__ == "__main__":
    main()
