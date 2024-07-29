import os
import pollytest
from groq import Groq
import time
import re
import ast

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
    context  = "{"
    context += str(time.strftime("%H:%M", time.localtime()))
    context += "} "
    messages.append(
        {
            "role": "user",
            "content": context + userInput
        }
    )
    print(messages)
    print("starting llm")
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
    )

    response = chat_completion.choices[0].message.content
    print(response)
    print("finished llm")
    
    match = re.match(r"\{.*?\}", response)
    
    
    chatFinished = True
    browserWindow = None
    realMessage = response

    if match:
        rawMessageData = match.group(0)  # La partie entre accolades
        realMessage = response[match.end():].strip()  # Le message sans la partie entre accolades

        
        extracted_dict = ast.literal_eval(rawMessageData)
        chatFinished = extracted_dict.get('chat_finished')
        browserWindow = extracted_dict.get('browser_open')

    if browserWindow != None:
        import webbrowser
        print(browserWindow)
        webbrowser.open(browserWindow)
    
    messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
    pollytest.ReadText(realMessage)
    
    return chatFinished


#DoLLM("coucouuu")