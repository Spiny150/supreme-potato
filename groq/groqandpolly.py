import os
import pollytest
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

initContent = open("../init.txt", "r").read()

messages = []
messages.append(
    {
        "role": "system",
        "content": initContent
    }
)


def DoLLM(userInput):
    messages.append(
        {
            "role": "user",
            "content": userInput
        }
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )

    response = chat_completion.choices[0].message.content
    messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
    pollytest.ReadText(response)


