from huggingface_hub import snapshot_download
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model")
parser.add_argument("-t", "--token")
args = parser.parse_args()

snapshot_download(repo_id=args.model,
                token=args.token,
                local_dir=f"converted_models/{args.model}",
                cache_dir=f"converted_models/cache")
