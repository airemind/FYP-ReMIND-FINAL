import cv2

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_face(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces) > 0


def get_resolution(image_path):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    return width, height


def decision_engine(image_path):
    has_face = detect_face(image_path)
    width, height = get_resolution(image_path)

    # Resolution threshold
    MIN_WIDTH = 1440
    MIN_HEIGHT = 900

    pipeline = []
    is_low_resolution = width < MIN_WIDTH or height < MIN_HEIGHT
    print("Resolution:", width, "x", height)

    # Face enhancement if face exists
    if has_face:
        pipeline.append("GFPGAN")

    # Upscaling if image is low resolution
    if is_low_resolution:
        pipeline.append("ESRGAN")

    return {
        "has_face": has_face,
        "resolution": f"{width}x{height}",
        "pipeline": pipeline,
    }
