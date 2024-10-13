import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")  # Uncomment if using a custom base URL
)

# Function to get GPT-4o Mini response
def get_code_review_response(prompt, max_tokens=1000):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI assistant who helps users in code reviews by deep thinking in points max 5-6 point shortly."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Sorry, an error occurred while generating your idea. Please try again later."
