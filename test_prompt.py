import google.generativeai as genai

genai.configure(api_key="")

model = genai.GenerativeModel("models/gemini-flash-latest")

response = model.generate_content("Say hello")

print(response.text)