'''import ollama

response=ollama.chat(
    model="llama3.2:3b",
    messages=[
      {  "role": "user",
        "content": "explain artificial intelligence in simple terms"
    }
    ]
)
print(response["message"]["content"])'''

# Taking input from user

'''import ollama


print("Personal AI Assistant")
print("Type 'exit' to quit.\n")


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("AI:", response["message"]["content"])

#Adding coservation memory

import ollama


MODEL = "llama3.2:3b"

messages = []

print("Personal AI Assistant")
print("Type 'exit' to quit.\n")


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Add user's message to conversation history
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Send the entire conversation to the model
    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    # Extract AI response
    assistant_message = response["message"]["content"]

    # Add AI response to conversation history
    messages.append(
        {
            "role": "assistant",
            "content": assistant_message
        }
    )

    print("AI:", assistant_message)


import ollama


MODEL = "llama3.2:3b"

messages = [
    {
        "role": "system",
        "content": (
            "You are my personal desktop AI assistant named ETERNITY. "
            "Be helpful, clear, and concise. "
            "Explain technical concepts in simple language. "
            "Do not claim that you performed a computer action "
            "unless a real tool actually performed it."
        )
    }
]


print("Personal AI Assistant")
print("Type 'exit' to quit.\n")


while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Add the user's message to the conversation
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    try:
        # Send the complete conversation to Ollama
        response = ollama.chat(
            model=MODEL,
            messages=messages
        )

        # Extract the AI response
        assistant_message = response["message"]["content"]

        # Store the AI response in the conversation
        messages.append(
            {
                "role": "assistant",
                "content": assistant_message
            }
        )

        print(f"AI: {assistant_message}\n")

    except Exception as error:
        print(f"Error: {error}\n")



import ollama

MODEL = "llama3.2:3b"

messages = [
    {
        "role": "system",
        "content": (
            "You are my personal desktop AI assistant named ETERNITY. "
            "Be helpful, clear, and concise. "
            "Explain technical concepts in simple language. "
            "Do not claim that you performed a computer action "
            "unless a real tool actually performed it."
        )
    }
]


print("HI! I am ETERNITY, your personal AI assistant.")
print("Type 'exit' to quit.\n")


while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    try:
        print("AI: ", end="", flush=True)

        response_stream = ollama.chat(
            model=MODEL,
            messages=messages,
            stream=True
        )

        full_response = ""

        for chunk in response_stream:
            text = chunk["message"]["content"]

            print(text, end="", flush=True)

            full_response += text

        print("\n")

        messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )

    except Exception as error:
        print(f"\nError: {error}\n")


    
import ollama


MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """
You are a personal desktop AI assistant.

Your responsibilities:
- Answer the user's questions clearly.
- Help the user understand technical concepts.
- Be concise unless more detail is requested.
- Remember the conversation context provided to you.
- Never claim that you performed an action unless the application
  actually performed that action.
- If you do not know something, say that you do not know.
"""


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


print("Personal AI Assistant")
print("Type 'exit' to quit.\n")


while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    try:
        print("AI: ", end="", flush=True)

        response_stream = ollama.chat(
            model=MODEL,
            messages=messages,
            stream=True
        )

        full_response = ""

        for chunk in response_stream:
            text = chunk["message"]["content"]

            print(text, end="", flush=True)

            full_response += text

        print("\n")

        messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )

    except Exception as error:
        print(f"\nError: {error}\n")

        

import ollama


MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """
You are a personal desktop AI assistant.

Your responsibilities:
- Answer the user's questions clearly.
- Help the user understand technical concepts.
- Be concise unless more detail is requested.
- Remember the conversation context provided to you.
- Never claim that you performed an action unless the application
  actually performed that action.
- If you do not know something, say that you do not know.
"""


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def get_ai_response(conversation):
    """
    Send the conversation to Ollama and return the complete response.
    """

    full_response = ""

    try:
        response_stream = ollama.chat(
            model=MODEL,
            messages=conversation,
            stream=True
        )

        for chunk in response_stream:
            text = chunk["message"]["content"]

            print(text, end="", flush=True)

            full_response += text

        return full_response

    except Exception as error:
        print(f"\n[ERROR] {error}")
        return None


def main():
    print("================================")
    print("      Personal AI Assistant")
    print("================================")
    print("Type 'exit' to quit.\n")

    while True:

        try:
            user_input = input("You: ").strip()

        except KeyboardInterrupt:
            print("\n\nExiting Personal AI...")
            break

        except EOFError:
            print("\n\nInput closed. Exiting...")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        print("AI: ", end="", flush=True)

        assistant_response = get_ai_response(messages)

        if assistant_response is None:
            # Remove the user message because the model
            # did not successfully process it.
            messages.pop()

            print("AI: I couldn't connect to the local AI model.\n")
            print("Check that Ollama is running and the model exists.\n")

            continue

        print("\n")

        messages.append(
            {
                "role": "assistant",
                "content": assistant_response
            }
        )


if __name__ == "__main__":
    main()'''

from brain import AIBrain


def main():

    brain = AIBrain()

    print("================================")
    print("      Personal AI Assistant")
    print("================================")
    print("Type 'exit' to quit.\n")

    while True:

        try:
            user_input = input("You: ").strip()

        except KeyboardInterrupt:
            print("\n\nExiting Personal AI...")
            break

        except EOFError:
            print("\n\nInput closed. Exiting...")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        print("AI: ", end="", flush=True)

        response = brain.chat(user_input)

        if response is None:
            print(
                "AI: I couldn't connect to the local AI model.\n"
            )
        else:
            print("\n")


if __name__ == "__main__":
    main()
    


    





