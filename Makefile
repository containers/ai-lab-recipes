app_name = locallm


build:
	@podman build -t $(app_name) .

run: 
	@podman run -it -p 7860:7860 $(app_name):latest