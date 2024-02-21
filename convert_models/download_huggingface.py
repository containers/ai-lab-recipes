from huggingface_hub import snapshot_download
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model")
args = parser.parse_args()

snapshot_download(repo_id=args.model,
                local_dir=f"converted_models/{args.model}",
                local_dir_use_symlinks=True,
                cache_dir=f"converted_models/cache")