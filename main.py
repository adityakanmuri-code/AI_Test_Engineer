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
        print("="*60)
        print(f"SECTION_ID: {section.section_id}")
        print(f"TITLE: {section.title}")
        print(f"SECTION_LENGTH : {len(section.content)}")
        print(section.content[:100])
        print(f"="*60)
if __name__ == "__main__":
    main()
