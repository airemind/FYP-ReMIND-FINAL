import subprocess
import os


def run_realesrgan(input_folder="inputs", output_folder="results"):

    # Absolute path to realesrgan directory
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../ai_models/realesrgan")
    )

    script_path = os.path.join(BASE_DIR, "inference_realesrgan.py")
    command = [
        "python3",
        script_path,
        "-n",
        "RealESRGAN_x2plus",
        "-i",
        input_folder,
        "-o",
        output_folder,
        "--outscale",
        "2",
        "--fp32",
        "--tile",
        "400",
        "--tile_pad",
        "10",
    ]
    try:
        print("Running RealESRGAN...")
        subprocess.run(command, cwd=BASE_DIR, check=True)
        print("Enhancement Completed")
    except subprocess.CalledProcessError as e:
        print("Error running RealESRGAN:", e)
        raise Exception("RealESRGAN enhancement failed")


if __name__ == "__main__":
    run_realesrgan()
