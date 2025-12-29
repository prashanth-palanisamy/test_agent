# import requests
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# api_key = os.environ.get("GROQ_API_KEY")
# url = "https://api.groq.com/openai/v1/models"
#
# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }
#
# response = requests.get(url, headers=headers)
#
# model_json = response.json()
# print(response.json())
# print(type(response))
#
# for model in model_json['data']:
#     owner = model.get('owned_by')
#     model_id = model.get('id')
#
#     # To get the short name (e.g., gpt-oss-120b)
#     short_name = model_id.split('/')[-1]
#
#     print(f"Owner: {owner}")
#     print(f"Model Name: {short_name}")
#     print("-" * 20)
#

# agent/modelsearch.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")

headers = {"Authorization": f"Bearer {api_key}",
          "Content-Type": "application/json"
          }

def get_model_list():
    url = "https://api.groq.com/openai/v1/models"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data_dict = response.json()
        # Return the list of dictionaries
        return data_dict.get('data', [])
    return []