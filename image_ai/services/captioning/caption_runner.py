import sys
from blip_service import generate_caption

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No image path provided")
        sys.exit(1)
    image_path = sys.argv[1]
    caption = generate_caption(image_path)
    print(caption)
