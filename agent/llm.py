import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GROQ_API")
print(token)

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"
                           ),
)
chat_completion	=	client.chat.completions.create(
    messages = [{
        "role":	"user",
        "content":	"Generate	terraform	code	for	iam	user	creation	with	name	as	devops",
    }
    ],

model="openai/gpt-oss-120b",
)
print(chat_completion.choices[0].message.content)