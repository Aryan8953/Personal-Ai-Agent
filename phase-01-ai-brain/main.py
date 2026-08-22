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

    print("AI:", response["message"]["content"])'''

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