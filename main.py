import openai
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

import openai

import openai

def generate_text(prompt, context=None):
    model_engine = "gpt-3.5-turbo"

    # Prepare the messages for the Chat API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    if context:
        messages.append({"role": "user", "content": context})
    messages.append({"role": "user", "content": prompt})

    # Calculate tokens in the input messages
    input_tokens = sum([len(message['content'].split()) for message in messages])
    
    # Set max_tokens based on the input_tokens
    min_tokens = 150
    max_tokens = input_tokens * 5
    max_response_tokens = min(max_tokens, 4096) if max_tokens > min_tokens else min_tokens

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
        max_tokens=max_response_tokens,
        n=1,
        temperature=0.7,
        top_p=1,
        stop=None,
    )
    message = response.choices[0].message['content'].strip()
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
