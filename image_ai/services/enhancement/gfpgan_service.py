import subprocess
import os


def run_gfpgan(input_folder="inputs", output_folder="results"):

    # Absolute path to GFPGAN directory
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../ai_models/gfpgan")
    )

    script_path = os.path.join(BASE_DIR, "inference_gfpgan.py")
    command = [
        "python3",
        script_path,
        "-i",
        input_folder,
        "-o",
        output_folder,
        "-v",
        "1.3",
        "--bg_upsampler",
        "realesrgan",
    ]
    try:
        print("Running GFPGAN (Face Enhancement)...")
        subprocess.run(command, cwd=BASE_DIR, check=True)
        print("Face Enhancement Completed")
    except subprocess.CalledProcessError as e:
        print("Error running GFPGAN:", e)
        raise Exception("GFPGAN enhancement failed")


if __name__ == "__main__":
    run_gfpgan()
