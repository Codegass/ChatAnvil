from model.chat import Chat

chat = Chat(service_provider="openai")
response = chat.get_response("Hello, how are you?", "gpt-4o-mini")
print(response)