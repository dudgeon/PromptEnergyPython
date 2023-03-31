import openai
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_text(prompt, context=None):
    model_engine = "text-davinci-002"
    full_prompt = f"{context} {prompt}{{{{response}}}}" if context else f"{prompt}{{{{response}}}}"
    
    # Calculate tokens in the input prompt
    input_tokens = len(full_prompt.split())
    
    # Set max_tokens based on the input_tokens
    # max_response_tokens = max(150, min(input_tokens * 5, 4096))
    min_tokens = 150
    max_tokens = input_tokens * 5
    max_response_tokens = min(max_tokens, 4096) if max_tokens > min_tokens else min_tokens

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=full_prompt,
        max_tokens=max_response_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = completions.choices[0].text.strip()
    return message

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_async", methods=["POST"])
def generate_async():
    input_text = request.form["input_text"]
    context = request.form["context"]
    generated_text = generate_text(input_text, context)
    return jsonify({"result": generated_text})

app.run(host="0.0.0.0", port=8080)
