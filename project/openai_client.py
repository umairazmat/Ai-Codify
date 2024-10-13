import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),  # Uncomment if using a custom base URL
)


# Function to get GPT-4o Mini response
def get_code_review_response(prompt, max_tokens=1000):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant who helps users in code reviews by deep thinking in points max 5-6 point shortly.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Sorry, an error occurred while generating your idea. Please try again later."


# Function to refactor code
def refactor_code(code_snippet):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert code refactoring assistant.",
                },
                {
                    "role": "user",
                    "content": f"Refactor the following code. Do not provide any explanation or comments, just return the refactored code.\n{code_snippet}",
                },
            ],
        )
        refactored_code = response.choices[0].message.content
        return refactored_code
    except Exception as e:
        return "Sorry, an error occurred while refactoring your code. Please try again later."


# Initialize the Anthropic client
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# Function to get feedback on code using Anthropic
def code_feedback(code_snippet):
    try:
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Please provide feedback on the given code, don't refactor the code:\n{code_snippet}",
                },
            ],
        )

        # Extract feedback text from the response
        feedback = response.text if hasattr(response, "text") else str(response)

        # Check if feedback is a Message object and extract text if necessary
        if hasattr(response, "content") and isinstance(response.content, list):
            feedback = "\n\n".join(
                [
                    text_block.text
                    for text_block in response.content
                    if hasattr(text_block, "text")
                ]
            )

        return feedback

    except Exception as e:
        return "Sorry, an error occurred while getting feedback on your code. Please try again later."
