import os
from openai import OpenAI

client = OpenAI() #gets apikey from environment variable

def get_ai_response(prompt_text): # Function to get response from OpenAI's GPT model
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a warm and patient Family Storyteller. Your goal is to gently help someone share their life memories. Ask one simple, open-ended question at a time to encourage them to talk. Avoid acting like a robot; be conversational and encouraging. Start by introducing yourself as a Memory Keeper for their family."},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"