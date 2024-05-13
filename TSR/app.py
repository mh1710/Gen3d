import logging
import os
import shlex
import subprocess
import tempfile
import time

import gradio as gr
import numpy as np
import rembg
import spaces
import torch
from PIL import Image
from functools import partial

subprocess.run(shlex.split('pip install wheel/torchmcubes-0.1.0-cp310-cp310-linux_x86_64.whl'))

from tsr.system import TSR
from tsr.utils import remove_background, resize_foreground, to_gradio_3d_orientation


HEADER = """
# TSR
1. Se você achar que o resultado não é satisfatório, tente alterar a proporção do primeiro plano. Pode melhorar os resultados.
2. É melhor desabilitar "Remover plano de fundo" para os exemplos fornecidos, pois eles já foram pré-processados.
3. Caso contrário, desative a opção "Remover plano de fundo" somente se sua imagem de entrada for RGBA com fundo transparente, o conteúdo da imagem estiver centralizado e ocupar mais de 70% da largura ou altura da imagem.
"""


if torch.cuda.is_available():
    device = "cuda:0"
else:
    device = "cpu"

model = TSR.from_pretrained(
    "stabilityai/TripoSR",
    config_name="config.yaml",
    weight_name="model.ckpt",
)
model.renderer.set_chunk_size(131072)
model.to(device)

rembg_session = rembg.new_session()


def check_input_image(input_image):
    if input_image is None:
        raise gr.Error("Nenhuma imagem carregada!")


def preprocess(input_image, do_remove_background, foreground_ratio):
    def fill_background(image):
        image = np.array(image).astype(np.float32) / 255.0
        image = image[:, :, :3] * image[:, :, 3:4] + (1 - image[:, :, 3:4]) * 0.5
        image = Image.fromarray((image * 255.0).astype(np.uint8))
        return image

    if do_remove_background:
        image = input_image.convert("RGB")
        image = remove_background(image, rembg_session)
        image = resize_foreground(image, foreground_ratio)
        image = fill_background(image)
    else:
        image = input_image
        if image.mode == "RGBA":
            image = fill_background(image)
    return image


@spaces.GPU
def generate(image, mc_resolution, formats=["obj", "stl"]):
    scene_codes = model(image, device=device)
    mesh = model.extract_mesh(scene_codes, resolution=mc_resolution)[0]
    mesh = to_gradio_3d_orientation(mesh)

    mesh_path_glb = tempfile.NamedTemporaryFile(suffix=f".stl", delete=False)
    mesh.export(mesh_path_glb.name)

    mesh_path_obj = tempfile.NamedTemporaryFile(suffix=f".obj", delete=False)
    mesh.apply_scale([-1, 1, 1])  # Otherwise the visualized .obj will be flipped
    mesh.export(mesh_path_obj.name)
    
    return mesh_path_obj.name, mesh_path_glb.name

def run_example(image_pil):
    preprocessed = preprocess(image_pil, False, 0.9)
    mesh_name_obj, mesh_name_glb = generate(preprocessed, 256, ["obj", "stl"])
    return preprocessed, mesh_name_obj, mesh_name_glb

with gr.Blocks() as demo:
    gr.Markdown(HEADER)
    with gr.Row(variant="panel"):
        with gr.Column():
            with gr.Row():
                input_image = gr.Image(
                    label="Input Image",
                    image_mode="RGBA",
                    sources="upload",
                    type="pil",
                    elem_id="content_image",
                )
                processed_image = gr.Image(label="Imagem Processada", interactive=False)
            with gr.Row():
                with gr.Group():
                    do_remove_background = gr.Checkbox(
                        label="Remover Background", value=True
                    )
                    foreground_ratio = gr.Slider(
                        label="Proporção de Primeiro Plano",
                        minimum=0.5,
                        maximum=1.0,
                        value=0.85,
                        step=0.05,
                    )
                    mc_resolution = gr.Slider(
                        label="Marching Cubes Resolução",
                        minimum=32,
                        maximum=320,
                        value=256,
                        step=32
                     )
            with gr.Row():
                submit = gr.Button("Generate", elem_id="generate", variant="primary")
        with gr.Column():
            with gr.Tab("OBJ"):
                output_model_obj = gr.Model3D(
                    label="Output Model (OBJ Format)",
                    interactive=False,
                )
                gr.Markdown(".")
            with gr.Tab("STL"):
                output_model_glb = gr.Model3D(
                    label="Output Model (STL Format)",
                    interactive=False,
                )
                gr.Markdown("Nota: O modelo mostrado aqui tem uma aparência mais escura. Baixe para obter resultados corretos.")
    with gr.Row(variant="panel"):
        gr.Examples(
            examples=[
                os.path.join("examples", img_name) for img_name in sorted(os.listdir("examples"))
            ],
            inputs=[input_image],
            outputs=[processed_image, output_model_obj, output_model_glb],
            cache_examples=True,
            fn=partial(run_example),
            label="Examples",
            examples_per_page=20
        )
    submit.click(fn=check_input_image, inputs=[input_image]).success(
        fn=preprocess,
        inputs=[input_image, do_remove_background, foreground_ratio],
        outputs=[processed_image],
    ).success(
        fn=generate,
        inputs=[processed_image, mc_resolution],
        outputs=[output_model_obj, output_model_glb],
    )

demo.queue(max_size=10)
demo.launch()
