# 1. Import Flask modules in addition to your Gemini imports
import os
from flask import Flask, render_template, request
from google import genai
from google.genai import types

# 2. Create a Flask app
app = Flask(__name__)

# 3. Initialize Gemini client once (outside function)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 4. Modify your generate function to accept input and return output
def generate_response(user_input):
    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],  # <- replace hardcoded text
        )
    ]
    config = types.GenerateContentConfig(
        system_instruction=[types.Part.from_text(
            text="Simple chatbot to answer simple chat queries as a demonstration"
        )]
    )

    # 5. Accumulate response text instead of printing
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        response_text += chunk.text
    return response_text  # <- return instead of printing

# 6. Add a route for the frontend
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]  # <- get input from web form
        bot_response = generate_response(user_input)  # <- call your modified function
        return render_template("index.html", user_input=user_input, bot_response=bot_response)
    return render_template("index.html", user_input=None, bot_response=None)

# 7. Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT, default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)