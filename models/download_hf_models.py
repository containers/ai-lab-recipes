from huggingface_hub import snapshot_download, hf_hub_download ,HfFileSystem
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model")
parser.add_argument("-o", "--output", default="./models")
parser.add_argument("-q", "--quantization", default="Q4_K_M")
args = parser.parse_args()

gguf = False
safetensor = False
ignore_patterns = ["*.md", ".gitattributes"]

fs = HfFileSystem()
files = fs.ls(args.model, detail=False)

for f in files:
    if ".gguf" in f:
        gguf = True
        break
    if ".safetensor" in f:
        safetensor = True
        break

if gguf:
    file_name = [x for x in files if args.quantization in x][0]
    file_name_parts = file_name.split("/")
    local_dir = f"{args.output}/{file_name_parts[1]}"
    hf_hub_download(repo_id=f"{file_name_parts[0]}/{file_name_parts[1]}", 
                    filename=file_name_parts[2],
                    local_dir=local_dir,
                    local_dir_use_symlinks=False
                    )
else:
    if  safetensor:
        ignore_patterns.append("*.bin")
    
    file_name_parts = args.model.split("/")
    local_dir = f"{args.output}/{file_name_parts[1]}"
    snapshot_download(repo_id=args.model,
                      local_dir=local_dir,
                      local_dir_use_symlinks=False,
                      ignore_patterns=ignore_patterns,
                      )