from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


def prompt_llm(messages, 
               model="gemini-2.0-flash", 
               base_url=None, 
               api_key=""):
    if base_url:
        #Azure or local LLM deployment
        client = OpenAI(base_url=base_url, api_key=api_key)
    else:
        #OpenAI deployment, api key set in environment variable
        client = OpenAI()
        
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,                
        )       
    
    return response.choices[0].message.content