
from src.chat import Chat
 
if __name__ == "__main__":

    chat = Chat()
    print("\n Start Chatting with Llama2...")
    while True:
        query = input("\n User: ")
        response = chat.ask(query)
        print("\n Agent: " + response)
