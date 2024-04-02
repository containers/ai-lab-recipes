from huggingface_hub import snapshot_download
snapshot_download(repo_id="BAAI/bge-base-en-v1.5",
    cache_dir="../../../models/",
    local_files_only=False)