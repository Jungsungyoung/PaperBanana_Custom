#!/usr/bin/env python3
"""
PaperBananaBench Dataset Download Script
"""

import os
import json
from pathlib import Path
from huggingface_hub import hf_hub_download, list_repo_files


def download_dataset():
    """Download PaperBananaBench Dataset"""

    repo_id = "dwzhu/PaperBananaBench"
    local_dir = Path("data/PaperBananaBench")

    print("=" * 60)
    print("PaperBananaBench Dataset Download")
    print("=" * 60)

    # Create directories
    (local_dir / "diagram" / "images").mkdir(parents=True, exist_ok=True)
    (local_dir / "diagram" / "pdfs").mkdir(parents=True, exist_ok=True)
    (local_dir / "plot" / "images").mkdir(parents=True, exist_ok=True)
    (local_dir / "plot" / "pdfs").mkdir(parents=True, exist_ok=True)

    try:
        # Get repository file list
        print("\n[1/3] Checking repository file list...")
        files = list_repo_files(repo_id)
        print(f"   Total {len(files)} files found")

        # Download JSON files
        json_files = [f for f in files if f.endswith(".json")]
        print(f"\n[2/3] Downloading JSON files ({len(json_files)} files):")

        for file in json_files:
            try:
                downloaded_path = hf_hub_download(
                    repo_id=repo_id,
                    filename=file,
                    local_dir=str(local_dir),
                    local_dir_use_symlinks=False,
                )
                print(f"   [OK] {file}")
            except Exception as e:
                print(f"   [FAIL] {file} - {e}")

        # Download sample images
        image_files = [f for f in files if f.endswith((".png", ".jpg", ".jpeg"))][:10]
        print(f"\n[3/3] Downloading sample images ({len(image_files)} files):")

        for file in image_files:
            try:
                downloaded_path = hf_hub_download(
                    repo_id=repo_id,
                    filename=file,
                    local_dir=str(local_dir),
                    local_dir_use_symlinks=False,
                )
                print(f"   [OK] {file}")
            except Exception as e:
                print(f"   [FAIL] {file} - {e}")

        print("\n" + "=" * 60)
        print("Dataset download completed!")
        print("=" * 60)
        print(f"\nLocation: {local_dir.absolute()}")
        print("\nNext steps:")
        print("  1. Set API keys in configs/model_config.yaml")
        print("  2. Run: streamlit run demo.py")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\n[NOTE] PaperBanana works without dataset.")
        print("       But Retriever Agent few-shot learning will be limited.")


if __name__ == "__main__":
    download_dataset()
