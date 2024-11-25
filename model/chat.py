# auto use difenrent model to chat
from model.openai.OpenAiChat import OpenAiChat
from model.ollama.OllamaChat import OllamaChat
from model.groq.GroqChat import GroqChat
from model.claude.ClaudeChat import ClaudeChat


class Chat():

    def __init__(self, key: str = None, service_provider: str = "openai") -> None:
        '''
        Initialize the chat client
        '''
        self.service_provider = service_provider
        if service_provider == "openai":
            self.chat = OpenAiChat(local_key=key)
        if service_provider == "ollama":
            self.chat = OllamaChat() # OllamaChat does not require any key
        if service_provider == "groq":
            self.chat = GroqChat(local_key=key)
        if service_provider == "claude":
            self.chat = ClaudeChat(local_key=key)
        
    def get_response(self, message: list, model: str):
        '''
        Get the response from the chat api
        '''
        return self.chat.get_response(message, model)
    
    def extract_code(self, response: str) -> list :
        '''
        Extract the code from the response,
        if the repsonse contains multiple code snippets, return all of them as a dict
        '''
        pass
        
    def evaluate_code_with_error_message(self, code: str, error: str):
        '''
        build the code and error pair with context and send to llm for fixing the 
        issue and plan the next step
        '''
        pass
        
    def set_system_prompt(self, prompt: str):
        '''
        Set the system prompt
        '''
        self.chat.set_system_prompt(prompt)

    def clear_history(self):
        '''
        Clear the history
        '''
        self.chat.clear_history()

    def get_messages_queue(self):
        '''
        Get the messages queue
        '''
        return self.chat.messages_queue
    
    def get_session_id(self):
        '''
        Get the session id
        '''
        return self.chat.get_session_id()
    