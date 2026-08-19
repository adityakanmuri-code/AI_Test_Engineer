from src.llm.test_ollama import get_response

def main():
    response = get_response(
        "What is software testing.Explain in 200 words excluding spaces and special characters."
    )
    print(response)


if __name__ == "__main__":
    main()
