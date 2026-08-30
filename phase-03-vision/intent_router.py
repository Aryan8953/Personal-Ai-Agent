import ollama

from configure import MODEL


def needs_screen(question):

    prompt = f"""
You are an intent classifier for a desktop AI assistant.

Decide whether the user's question requires seeing the
current computer screen.

Return ONLY one word:

VISION
or
NORMAL

Use VISION when the user refers to:
- their screen
- an application currently open
- visible content
- an error currently displayed
- a button, window, file, or UI element they can see
- something happening visually on the computer

Use NORMAL for general questions that do not require
seeing the screen.

User question:
{question}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response["message"]["content"].strip().upper()

    return result == "VISION"


if __name__ == "__main__":

    print("================================")
    print("        Intent Router")
    print("================================")

    while True:

        question = input(
            "\nQuestion (type 'exit' to quit): "
        )

        if question.lower().strip() == "exit":
            break

        if needs_screen(question):
            print("→ VISION")
        else:
            print("→ NORMAL")