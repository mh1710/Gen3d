import gradio as gr
import requests
import io
import random
import os
from PIL import Image

# Lista de Modelos Disponiveis

list_models = [
    "FunkoPOP", "Funko",
]

# Função para gerar imagem a partir de texto
def generate_txt2img(current_model, prompt, is_negative=False, image_style="None style", steps=50, cfg_scale=7, seed=None):

    if current_model == "FunkoPOP":
        API_URL = "https://api-inference.huggingface.co/models/ProomptEngineer/pe-funko-pop-diffusion-style"
    elif current_model == "Funko":
        API_URL = "https://api-inference.huggingface.co/models/ProomptEngineer/pe-funko-pop-diffusion-style"   
    API_TOKEN = os.environ.get("HF_READ_TOKEN")
    headers = {"Authorization": f"Bearer {API_TOKEN}"}


    if image_style == "None style":
        payload = {
            "inputs": prompt + ", PEPopFigure, funko pop big head, big head mode, gigantic head, small body, no background, 8k",
            "is_negative": is_negative + ", Toy Box",
            "steps": steps,
            "cfg_scale": cfg_scale,
            "seed": seed if seed is not None else random.randint(-1, 2147483647)
        }
    elif image_style == "Cinematic":
        payload = {
            "inputs": prompt + ", realistic, detailed, textured, skin, hair, eyes, by Alex Huguet, Mike Hill, Ian Spriggs, JaeCheol Park, Marek Denko",
            "is_negative": is_negative + ", abstract, cartoon, stylized",
            "steps": steps,
            "cfg_scale": cfg_scale,
            "seed": seed if seed is not None else random.randint(-1, 2147483647)
        }
    elif image_style == "Digital Art":
        payload = {
            "inputs": prompt + ", faded , vintage , nostalgic , by Jose Villa , Elizabeth Messina , Ryan Brenizer , Jonas Peterson , Jasmine Star",
            "is_negative": is_negative + ", sharp , modern , bright",
            "steps": steps,
            "cfg_scale": cfg_scale,
            "seed": seed if seed is not None else random.randint(-1, 2147483647)
        }
    elif image_style == "Portrait":
        payload = {
            "inputs": prompt + ", soft light, sharp, exposure blend, medium shot, bokeh, (hdr:1.4), high contrast, (cinematic, teal and orange:0.85), (muted colors, dim colors, soothing tones:1.3), low saturation, (hyperdetailed:1.2), (noir:0.4), (natural skin texture, hyperrealism, soft light, sharp:1.2)",
            "is_negative": is_negative,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "seed": seed if seed is not None else random.randint(-1, 2147483647)
        }

    image_bytes = requests.post(API_URL, headers=headers, json=payload).content
    image = Image.open(io.BytesIO(image_bytes))
    return image

css = """
/* General Container Styles */
.gradio-container {
    font-family: 'IBM Plex Sans', sans-serif;
    max-width: 730px !important;
    margin: auto;
    padding-top: 1.5rem;
    text-align: center; /* Center the content horizontally */
}

/* Button Styles */
.gr-button {
    color: white;
    background: #007bff; /* Use a primary color for the background */
    white-space: nowrap;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
}

.gr-button:hover {
    background-color: #0056b3; /* Darken the background color on hover */
}

/* Share Button Styles */
#share-btn-container {
    padding: 0.5rem !important;
    background-color: #007bff; /* Use a primary color for the background */
    justify-content: center;
    align-items: center;
    border-radius: 9999px !important;
    max-width: 13rem;
    margin: 0 auto; /* Center the container horizontally */
    transition: background-color 0.3s;
}

#share-btn-container:hover {
    background-color: #0056b3; /* Darken the background color on hover */
}

#share-btn {
    all: initial;
    color: #ffffff;
    font-weight: 600;
    cursor: pointer;
    font-family: 'IBM Plex Sans', sans-serif;
    margin: 0.5rem !important;
    padding: 0.5rem !important;
}

/* Other Styles */
#gallery {
    min-height: 22rem;
    margin: auto; /* Center the gallery horizontally */
    border-bottom-right-radius: 0.5rem !important;
    border-bottom-left-radius: 0.5rem !important;
}

/* Centered Container for the Image */
.image-container {
    max-width: 100%; /* Set the maximum width for the container */
    margin: auto; /* Center the container horizontally */
    padding: 20px; /* Add padding for spacing */
    border: 1px solid #ccc; /* Add a subtle border to the container */
    border-radius: 10px;
    overflow: hidden; /* Hide overflow if the image is larger */
    max-height: 22rem; /* Set a maximum height for the container */
}

/* Set a fixed size for the image */
.image-container img {
    max-width: 100%; /* Ensure the image fills the container */
    height: auto; /* Maintain aspect ratio */
    max-height: 100%; /* Set a maximum height for the image */
    border-radius: 10px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
}
"""

# Interface Gradio
with gr.Blocks(css=css) as demo:
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("<h1>AI Diffusion</h1>")
            current_model = gr.Dropdown(label="Select Model", choices=list_models, value=list_models[1])
            text_prompt = gr.Textbox(label="Enter Prompt", placeholder="Example: a cute dog", lines=2)
            generate_button = gr.Button("Generate Image", variant='primary')

        with gr.Column():
            gr.Markdown("<h4>Advanced Settings</h4>")
            with gr.Accordion("Advanced Customizations", open=False):
                negative_prompt = gr.Textbox(label="Negative Prompt (Optional)", placeholder="Example: blurry, unfocused", lines=2)
                image_style = gr.Dropdown(label="Select Style", choices=["None style", "Cinematic", "Digital Art", "Portrait"], value="None style")
                # Add more options if needed

    with gr.Row():
        image_output = gr.Image(type="pil", label="Output Image")

    generate_button.click(generate_txt2img, inputs=[current_model, text_prompt, negative_prompt, image_style], outputs=image_output)

# Launch the app
demo.launch()