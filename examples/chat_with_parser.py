import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from chat_base import Chat


def test_markdown_parser():
    """
    Test the Markdown parser
    """
    print("\n=== Testing Markdown Parser ===")
    chat = Chat("openai", parser_type="markdown")
    
    response = chat.get_response(
        "Please write a Python function to calculate fibonacci numbers "
        "and explain how it works with markdown formatting.",
        model="gpt-4o-mini"
    )
    
    # extract code blocks
    code_blocks = chat.extract_code(response)
    print("\nExtracted code blocks:")
    for block in code_blocks:
        print(f"\nLanguage: {block['language']}")
        print(f"Code:\n{block['content']}")

def test_json_parser():
    """
    Test the JSON parser
    """
    print("\n=== Testing JSON Parser ===")
    chat = Chat("openai", parser_type="json")
    
    response = chat.get_response(
        "Please provide a JSON response that includes: "
        "1) a greeting message, "
        "2) current year, "
        "3) a Python function to generate three random colors. "
        "The response should include both the function code and the color results. "
        "Format the generated code within a code key in the JSON response and give language type.",
        model="gpt-4o-mini"
    )

    # 提取JSON响应中的代码块
    code_blocks = chat.extract_code(response)
    print("\nExtracted code blocks:")
    for block in code_blocks:
        print(f"\nLanguage: {block['language']}")
        print(f"Code:\n{block['content']}")


def test_xml_parser():
    """
    Test the XML parser
    """
    print("\n=== Testing XML Parser ===")
    chat = Chat("openai", parser_type="xml")
    
    response = chat.get_response(
        "Please provide an XML document that includes: "
        "1) a book description with title, author, year, and genre elements, "
        "2) a Python function to count words in the book's title. "
        "The function should be wrapped in a CDATA section within a 'code' element. "
        "Also include the function's result for the given title.",
        model="gpt-4o-mini"
    )

    # 提取XML响应中的代码块
    code_blocks = chat.extract_code(response)
    print("\nExtracted code blocks:")
    for block in code_blocks:
        print(f"\nLanguage: {block['language']}")
        print(f"Code:\n{block['content']}")

def test_default_parser():
    """
    Test the default parser
    """
    print("\n=== Testing Default Parser ===")
    chat = Chat("openai", parser_type="default")
    
    response = chat.get_response(
        "Give me a simple greeting.",
        model="gpt-4o-mini"
    )
    
    try:
        # 这应该会引发错误，因为默认解析器不支持代码提取
        chat.extract_code(response)
    except ValueError as e:
        print(f"\nExpected error: {e}")

def test_parser_switching():
    """
    Test parser switching
    """
    print("\n=== Testing Parser Switching ===")
    chat = Chat("openai", parser_type="markdown")
    
    print(f"Current parser: {chat.get_current_parser()}")
    
    # switch to JSON parser
    chat.set_parser("json")
    print(f"After switching parser: {chat.get_current_parser()}")
    
    response = chat.get_response(
        "Return a simple JSON object with a greeting message.",
        model="gpt-4o-mini"
    )
    print(f"\nResponse with JSON parser:\n{response}")

def main():
    """
    Main function
    """
    # api key load from .env, you need to set it in your .env file first
    
    # test all parsers
    test_markdown_parser()
    test_json_parser()
    test_xml_parser()
    test_default_parser()
    test_parser_switching()

if __name__ == "__main__":
    main()
