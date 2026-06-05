from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "Salesforce/blip-image-captioning-large"

processor = BlipProcessor.from_pretrained(MODEL_NAME)
model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
model.to(DEVICE)
model.eval()


def generate_caption(image_path: str) -> str:
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(image, return_tensors="pt")
        inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=50,
                num_beams=5,
                early_stopping=True,
                repetition_penalty=1.2,
            )
        caption = processor.decode(output_ids[0], skip_special_tokens=True)
        return caption.strip()
    except Exception as e:
        print(f"Caption generation failed: {str(e)}")
        return "Unable to generate image caption."
