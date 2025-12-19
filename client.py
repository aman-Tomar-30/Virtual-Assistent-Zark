from openai import OpenAI

OPENAI_API_KEY = ""

client = OpenAI(
    api_key = OPENAI_API_KEY
)

# Call the Chat Completions API
response = client.chat.completions.create(
    model="gpt-4o-mini",   # or "gpt-4o", "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis, capable of doing tasks like alexa and google cloud"},
        {"role": "user", "content": "what is coding"}
    ],
    max_tokens=100
)

# Print the response
print(response.choices[0].message.content)