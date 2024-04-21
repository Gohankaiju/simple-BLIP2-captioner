import gradio as gr
import os
import torch
from lavis.models import load_model_and_preprocess
from PIL import Image
from tqdm import tqdm  

def process_image(img_path, model, vis_processors, device):
    raw_image = Image.open(img_path).convert('RGB')
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    result = model.generate({"image": image})
    return result

def save_caption(caption, img_path):
    # save caption file
    caption_file = os.path.splitext(img_path)[0] + '.txt'
    with open(caption_file, 'w') as f:
        f.write('\n'.join(map(str, caption)))

def generate_captions(folder_path, model_choice):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # mapping
    model_mapping = {
        "pretrain_opt2.7b": ("blip2_opt", "pretrain_opt2.7b"),
        "pretrain_opt6.7b": ("blip2_opt", "pretrain_opt6.7b"),
        "caption_coco_opt2.7b": ("blip2_opt", "caption_coco_opt2.7b"),
        "caption_coco_opt6.7b": ("blip2_opt", "caption_coco_opt6.7b"),
        "pretrain_flant5xl": ("blip2_t5", "pretrain_flant5xl"),
        "caption_coco_flant5xl": ("blip2_t5", "caption_coco_flant5xl"),
        "pretrain_flant5xxl": ("blip2_t5", "pretrain_flant5xxl")
    }

    model_name, model_type = model_mapping[model_choice]
    model, vis_processors, _ = load_model_and_preprocess(
        name=model_name, model_type=model_type, is_eval=True, device=device
    )
    
    captions = []
    file_list = os.listdir(folder_path)
    image_files = [f for f in file_list if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for img_file in tqdm(image_files, desc="Processing images", unit="image"):     
        img_path = os.path.join(folder_path, img_file)
        caption = process_image(img_path, model, vis_processors, device)
        save_caption(caption, img_path)
        captions.append((img_file, caption))
    return captions

# Gradio app interface
iface = gr.Interface(
    fn=generate_captions,
    inputs=[
        gr.Textbox(label="Image Folder Path"),
        gr.Dropdown(label="Model", choices=[
            "pretrain_opt2.7b", "pretrain_opt6.7b",
            "caption_coco_opt2.7b", "caption_coco_opt6.7b",
            "pretrain_flant5xl", "caption_coco_flant5xl",
            "pretrain_flant5xxl"
        ])
    ],
    outputs=gr.Dataframe(),
    allow_flagging='never',
    title="BLIP2-Easy-Captioner"
)

iface.launch()
