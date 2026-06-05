import os
import uuid
import shutil
import time

from datetime import datetime
from image_ai.config import TEMP_DIR
from image_ai.services.utils.logger import log_info, log_error, log_separator
from image_ai.services.utils.cacher import (
    generate_image_hash,
    is_cached,
    save_to_cache,
    load_from_cache,
)

from image_ai.services.decision.decision_engine import decision_engine
from image_ai.services.enhancement.gfpgan_service import run_gfpgan
from image_ai.services.enhancement.esrgan_service import run_realesrgan
from image_ai.services.evaluation.evaluation import save_evaluation

print("USING ENHANCEMENT:", __file__)


def enhance_image(input_image_path: str):
    unique_id = str(uuid.uuid4())
    pipeline_start_time = time.time()
    log_info("enhancement session started", unique_id)
    try:
        image_hash = generate_image_hash(input_image_path)
        # CACHE CHECK
        if is_cached(image_hash):
            cached_result = load_from_cache(image_hash)
            total_time = round(time.time() - pipeline_start_time, 2)
            evaluation_data = {
                "session_id": unique_id,
                "timestamp": str(datetime.now()),
                "selected_pipeline": "cached_result",
                "cache_used": True,
                "status": "success",
                "total_pipeline_time_seconds": total_time,
            }
            save_evaluation(evaluation_data, unique_id)
            log_info("cached result returned", unique_id)
            log_separator()

            return {
                "success": True,
                "session_id": unique_id,
                "enhanced_image": cached_result["enhanced_image"],
                "pipeline_used": ["CACHE"],
                "cache_used": True,
                "metrics": {"processing_time": total_time},
            }

        # SESSION DIRECTORIES
        session_dir = os.path.join(TEMP_DIR, unique_id)
        input_dir = os.path.join(session_dir, "input")
        gfpgan_dir = os.path.join(session_dir, "gfpgan")
        esrgan_dir = os.path.join(session_dir, "esrgan")
        final_dir = os.path.join(session_dir, "final")

        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(gfpgan_dir, exist_ok=True)
        os.makedirs(esrgan_dir, exist_ok=True)
        os.makedirs(final_dir, exist_ok=True)

        # COPY INPUT IMAGE
        input_filename = os.path.basename(input_image_path)
        pipeline_input_path = os.path.join(input_dir, input_filename)
        shutil.copy(input_image_path, pipeline_input_path)
        # DECISION ENGINE
        decision = decision_engine(input_image_path)
        pipeline_used = decision["pipeline"]

        log_info(f"selected pipeline: {pipeline_used}", unique_id)
        current_image_path = pipeline_input_path

        # GFPGAN
        if "GFPGAN" in pipeline_used:
            log_info("gfpgan started", unique_id)
            run_gfpgan(input_folder=input_dir, output_folder=gfpgan_dir)
            restored_folder = os.path.join(gfpgan_dir, "restored_imgs")
            restored_images = os.listdir(restored_folder)
            if not restored_images:
                raise Exception("GFPGAN failed")
            current_image_path = os.path.join(restored_folder, restored_images[0])
            log_info("gfpgan completed", unique_id)

        # ESRGAN
        if "ESRGAN" in pipeline_used:
            log_info("realesrgan started", unique_id)
            esrgan_input_path = os.path.join(
                esrgan_dir, os.path.basename(current_image_path)
            )
            shutil.copy(current_image_path, esrgan_input_path)
            run_realesrgan(input_folder=esrgan_dir, output_folder=esrgan_dir)

            # SEARCH RECURSIVELY FOR ESRGAN OUTPUT
            enhanced_image_path = None
            for root, dirs, files in os.walk(esrgan_dir):
                for file in files:
                    if "_out" in file and file.lower().endswith(
                        (".png", ".jpg", ".jpeg", ".webp")
                    ):
                        enhanced_image_path = os.path.join(root, file)
                        break
                if enhanced_image_path:
                    break
            if not enhanced_image_path:
                raise Exception("Enhanced ESRGAN output not found")
            current_image_path = enhanced_image_path

            log_info(f"enhanced image selected: {current_image_path}", unique_id)
            log_info("realesrgan completed", unique_id)

        # FINAL OUTPUT
        final_output_path = os.path.join(
            final_dir, os.path.basename(current_image_path)
        )
        shutil.copy(current_image_path, final_output_path)
        print("ABOUT TO SAVE CACHE")

        # CACHE SAVE
        save_to_cache(image_hash=image_hash, image_path=final_output_path, caption="")
        print("CACHE SAVED")

        # METRICS
        total_time = round(time.time() - pipeline_start_time, 2)
        evaluation_data = {
            "session_id": unique_id,
            "timestamp": str(datetime.now()),
            "selected_pipeline": pipeline_used,
            "cache_used": False,
            "status": "success",
            "total_pipeline_time_seconds": total_time,
        }
        save_evaluation(evaluation_data, unique_id)
        log_info("pipeline completed", unique_id)
        log_separator()

        return {
            "success": True,
            "session_id": unique_id,
            "enhanced_image": final_output_path,
            "pipeline_used": pipeline_used,
            "cache_used": False,
            "metrics": {"processing_time": total_time},
        }
    except Exception as e:
        log_error(str(e), unique_id)
        log_separator()
        return {"success": False, "session_id": unique_id, "error": str(e)}
