import ollama 
from configure import MODEL
from prompts import SYSTEM_PROMPT

class AIBrain:

    def __init__(self):
        self.messages=[
            {
            "role":"system",
            "content": SYSTEM_PROMPT
        }
      ]
    def chat(self,user_input):
        self.messages.append(
            {
                "role":"user",
                "content": user_input
            }
        )
        full_response=""

        try:
            response_stream=ollama.chat(
                model=MODEL,
                messages=self.messages,
                stream=True
            )

            for chunk in response_stream:
                text=chunk["message"]["content"]
                print(text,end="",flush=True)
                full_response+=text

            self.messages.append(
                  {
                        "role":"assistant",
                        "content":full_response
                  }
                  
            )
            return full_response

        except Exception as error:
            print(f"ERROR: {error}\n")
            self.messages.pop()
            return None
