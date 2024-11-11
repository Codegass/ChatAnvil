# auto use difenrent model to chat
from model.openai.OpenAiChat import OpenAiChat
from model.ollama.OllamaChat import OllamaChat
from model.groq.GroqChat import GroqChat
from model.claude.ClaudeChat import ClaudeChat


class Chat():

    def __init__(self, service_provider: str = "openai") -> None:
        '''
        Initialize the chat client
        '''
        self.service_provider = service_provider
        if service_provider == "openai":
            self.chat = OpenAiChat()
        if service_provider == "ollama":
            self.chat = OllamaChat()
        if service_provider == "groq":
            self.chat = GroqChat()
        if service_provider == "claude":
            self.chat = ClaudeChat()
        
    def get_response(self, message: list, model: str):
        '''
        Get the response from the chat api
        '''
        return self.chat.get_response(message, model)
    
    def extract_code(self, response: str) -> list :
        '''
        Extract the code from the response
        '''
        code_with_lang_tag = response.split('```')[1]
        code = code_with_lang_tag.split("\n")[1:]
        return code
    
    def evaluate_code_with_error_message(self, code: str, error: str):
        '''
        build the code and error pair with context and send to llm for fixing the 
        issue and plan the next step
        '''
        pass
        
    