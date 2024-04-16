from transformers import AutoImageProcessor, AutoModelForObjectDetection
from huggingface_hub import snapshot_download
from PIL import Image, ImageDraw
from fastapi import FastAPI
from pydantic import BaseModel
import torch
import base64
import os
import io
import shutil


app = FastAPI()
model = os.getenv("MODEL_PATH", default="/app/models/facebook/detr-resnet-101")
revision = os.getenv("MODEL_REVISION", default="no_timm")

if os.path.isfile(model):
    model_name = os.getenv("MODEL_NAME", default="facebook/detr-resnet-101")
    snapshot_download(repo_id=model_name,
                  revision=revision,
                local_dir=f"/tmp/{model}",
                local_dir_use_symlinks=False)
    shutil.copyfile(model, f"/tmp/{model}/pytorch_model.bin")
    processor = AutoImageProcessor.from_pretrained(f"/tmp/{model}", revision=revision)
    model = AutoModelForObjectDetection.from_pretrained(f"/tmp/{model}", revision=revision)
else:
    processor = AutoImageProcessor.from_pretrained(model, revision=revision)
    model = AutoModelForObjectDetection.from_pretrained(model, revision=revision)

class Item(BaseModel):
    image: bytes 

@app.get("/health")
def tests_alive():
    return {"alive": True}

@app.post("/detection")
def detection(item: Item):
    b64_image = item.image
    b64_image = base64.b64decode(b64_image)
    bytes_io = io.BytesIO(b64_image)    
    image = Image.open(bytes_io)
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
    draw = ImageDraw.Draw(image)
    scores = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        x, y, x2, y2 = tuple(box)
        draw.rectangle((x, y, x2, y2), outline="red", width=1)
        draw.text((x, y), model.config.id2label[label.item()], fill="white")
        label_confidence = f"Detected {model.config.id2label[label.item()]} with confidence {round(score.item(), 3)}"
        scores.append(label_confidence)
    
    bytes_io = io.BytesIO() 
    image.save(bytes_io, "JPEG")
    img_bytes = bytes_io.getvalue()
    img_bytes = base64.b64encode(img_bytes).decode('utf-8')
    return {'image': img_bytes, "boxes": scores}