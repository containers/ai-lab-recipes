app_name = locallm

ifdef arch_type
arch_command = --arch=$(arch_type)
endif

build:
	@podman build -t $(app_name) . $(arch_command)
	
run: 
	@podman run -it -p 7860:7860 $(app_name):latest