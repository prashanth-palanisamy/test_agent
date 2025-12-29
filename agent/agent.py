import os
from groq import Groq

def calling_groq(message, model_id):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages= message,
        model=model_id,
    )

    return(chat_completion.choices[0].message.content)