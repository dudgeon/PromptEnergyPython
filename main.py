import openai
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_text(prompt):
    model_engine = "text-davinci-002"
    prompt = f"{prompt}{{{{response}}}}"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=150,
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
    generated_text = generate_text(input_text)
    return jsonify({"result": generated_text})

app.run(host="0.0.0.0", port=8080)
