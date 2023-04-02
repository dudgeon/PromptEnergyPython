import openai
import os
from quart import Quart, render_template, request, jsonify, Response
import asyncio

app = Quart(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

async def generate_text_async(prompt, context=None):
    model_engine = "gpt-3.5-turbo"

    # Prepare the messages for the Chat API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    if context:
        messages.append({"role": "user", "content": context})
    messages.append({"role": "user", "content": prompt})

    async for chunk in await openai.ChatCompletion.acreate(
        model=model_engine,
        messages=messages,
        max_tokens=750,
        n=1,
        temperature=0.7,
        top_p=1,
        stop=None,
        stream=True,
    ):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            yield content

@app.route("/")
async def home():
    return await render_template("index.html")

@app.route("/generate_async", methods=["POST"])
async def generate_async():
    input_text = (await request.form)["input_text"]
    context = (await request.form)["context"]

    return Response(generate_text_async(input_text, context), mimetype='text/plain')

app.run(host="0.0.0.0", port=8080)
