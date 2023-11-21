app_name = locallm


build:
	@podman build -t $(app_name) .

run: 
	@podman run -it $(app_name):latest 