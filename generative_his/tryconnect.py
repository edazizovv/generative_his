# import gradio as gr
import torch
# from torch import autocast
from diffusers import StableDiffusionPipeline, DiffusionPipeline
# from datasets import load_dataset
from PIL import Image
# from io import BytesIO
# import base64
import re
import os
import requests

# from share_btn import community_icon_html, loading_icon_html, share_js

TOKEN = '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'

# If you are running this code locally, you need to either do a 'huggingface-cli login` or paste your User Access Token from here https://huggingface.co/settings/tokens into the use_auth_token field below.
# pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_token=True, revision="fp16", torch_dtype=torch.float16)
# pipe = pipe.to(device)
# torch.backends.cudnn.benchmark = True


def infer(prompt):
    global is_gpu_busy
    samples = 4
    steps = 50
    scale = 7.5

    # generator = torch.Generator(device=device).manual_seed(seed)
    # print("Is GPU busy? ", is_gpu_busy)
    images = []
    # if(not is_gpu_busy):
    #    is_gpu_busy = True
    #    images_list = pipe(
    #        [prompt] * samples,
    #        num_inference_steps=steps,
    #        guidance_scale=scale,
    # generator=generator,
    #    )
    #    is_gpu_busy = False
    #    safe_image = Image.open(r"unsafe.png")
    #    for i, image in enumerate(images_list["sample"]):
    #       if(images_list["nsfw_content_detected"][i]):
    #           images.append(safe_image)
    #       else:
    #           images.append(image)
    # else:
    url = os.getenv('JAX_BACKEND_URL')
    payload = {'prompt': prompt}
    images_request = requests.post(url, json=payload)
    for image in images_request.json()["images"]:
        image_b64 = (f"data:image/jpeg;base64,{image}")
        images.append(image_b64)

    return images


def none(prompt):

    model_id = "CompVis/stable-diffusion-v1-4"

    samples = 4
    steps = 50
    scale = 7.5

    """
    # pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_token=True, revision="fp16", torch_dtype=torch.float16)
    pipe = StableDiffusionPipeline.from_pretrained(model_id,
                                                   use_auth_token=TOKEN,
                                                   revision="fp16",
                                                   torch_dtype=torch.float16)
    """

    pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4",
                                             use_auth_token=TOKEN,
                                             # revision="fp16",
                                             )

    images_list = pipe(
    [prompt] * samples,
    num_inference_steps=steps,
    guidance_scale=scale,
    )

    return images_list

images = none("Big red apple")
