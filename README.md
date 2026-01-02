This is a collection of personal reviews of many of the NVIDIA DGX Spark Playbook tutorials that can be found at
https://build.nvidia.com/spark.

Why do this? As I have found, if you follow the tutorials to the letter, they work pretty well.  However, if you stray or try variants, there can be unexpected behavior and issues. 

Each review will likely be shorter, more to the point, with less spin on how wonderful it is :). 

## Playbook: DGX-Dashboard

11/30/2025

https://build.nvidia.com/spark/dgx-dashboard

Really simple install.  The dashboard is basically a tool tray app (OS independant) that uses ssh to connect to your Spark.  It launches a Webpage to show a simple Dashboard.  I found the GPU and memory usage to be less responsive that other tools.  Hard to determine if 

The first alternative to watch for GPU usage is to ssh into the Spark and use "nvidia-smi".

```
watch -n 1 nvidia-smi
```

Another alternative for watching GPU usage is "nvtop".  This is more responsive to GPU usage, say by using OpenWebUI connected to an Ollama docker container on the Spark.  Cannot get the memory tracking working.  Read about running as sudo, but that seems to lock up the Spark.  Adding a Follow up task.

The one click "update" is nice, but you can do this from ssh/command line:

```
sudo apt update
sudo apt dist-upgrade
sudo fwupdmgr refresh
sudo fwupdmgr upgrade
sudo reboot
```

## Playbook: Open WebUI with Ollama

TODO
12/10/2025

https://build.nvidia.com/spark/open-webui

The first steps for installing Docker on Ubuntu are good. 

The instructions try to make it easier by using a combined OpenWebUI + Ollama docker container.  I wanted to separate them so I followed other options suggested by Copilot (sorry, no references).

Ended up with a couple docker compose files:

```
ollama_stuff/docker-compose.yaml:
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama:/root/.ollama
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

volumes:
  ollama:
    external: true
```

```
openwebui_stuff/docker-compose.yaml:
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data
    restart: always

volumes:
  open-webui:
```

Each can be started by:
- cd <directory>
- docker compose start -d

And stopped by:
- cd <directory>
- docker compose stop

The instrunctions do describe nicely how to update OpenWebUI when it shows an update.  It's even simpler with docker compose:
- cd <directory>
- docker compose stop
- docker compose pull
- docker compose start -d

The instructions describe updating models within Ollama by using the OpenWebUI UI.  An alternative is to use docker to attach to the running container, and use ollama commands:
```
docker exec -it ollama bash
ollama ls
ollama pull smollm2 # or other model
```


## Bonus: Docker Model Runner

12/15/2025

The group behind Docker (Canonical?) have created an extension of Docker to help with local models, similar to Ollama.  

Some key features:
- uses both llama.cpp and vllm inference engines
- automatic selection inf inference engine based on model
- uses ls, pull etc.
- don't need to use -exec into container like ollama update models
- docker model runner (DMR) provides OpenAI API like Ollama, but at port 12434

### from Google search:

Docker Model Runner (DMR) is a feature that simplifies the process for developers to run, test, and manage Large Language Models (LLMs) and other AI models locally using the same commands and workflows they use for containers. [1, 2]  
Key Features and Summary 

• Simplified Local Development: DMR eliminates the need to set up complex, model-specific Python environments or inference servers. Developers can use familiar  commands (like , , ) to manage models. 
• OCI-Compliant Packaging: Models are packaged and distributed as standard OCI (Open Container Initiative) artifacts on Docker Hub or from HuggingFace (if in GGUF format), allowing them to be versioned and shared using existing container registry infrastructure. 
• OpenAI-Compatible API: Models run by DMR are exposed through an OpenAI-compatible API, making it easy to integrate them into existing AI applications or switch between local and cloud-based services with minimal code changes. 
• Performance and Privacy: By running models locally, developers benefit from data privacy, reduced latency, and no recurring API costs. DMR uses host-installed inference engines (like  and vLLM) with GPU acceleration (on Apple Silicon, NVIDIA, AMD, and Intel hardware) to maximize performance. 
• Integration with the Docker Ecosystem: DMR integrates seamlessly with Docker Desktop's UI, Docker Compose for multi-service applications, and Testcontainers for automated testing. 
• Architecture: Unlike typical Docker commands, running a model does not spin up a new container. Instead, DMR runs an inference server as a host process (or a highly integrated container in Docker Engine environments) that loads models on demand, abstracting the complexity from the user. [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  

AI responses may include mistakes.

[1] https://www.docker.com/blog/announcing-docker-model-runner-ga/
[2] https://www.docker.com/products/model-runner/
[3] https://www.docker.com/blog/docker-model-runner-universal-blue/
[4] https://docs.docker.com/ai/model-runner/
[5] https://www.docker.com/blog/introducing-docker-model-runner/
[6] https://www.ajeetraina.com/docker-model-runner-tutorial-and-cheatsheet-mac-windows-and-linux-support/
[7] https://www.docker.com/blog/how-we-designed-model-runner-and-whats-next/
[8] https://dev.to/docker/from-zero-to-local-llm-a-developers-guide-to-docker-model-runner-4oi2
[9] https://www.docker.com/blog/docker-model-runner-integrates-vllm/
[10] https://www.docker.com/blog/how-to-build-run-and-package-ai-models-locally-with-docker-model-runner/
[11] https://dev.to/docker/think-fast-code-faster-local-ai-development-with-docker-model-runner-2878
[12] https://www.docker.com/blog/docker-model-runner-on-hugging-face/


### Some quick notes from my private stuff README

```
- https://docs.docker.com/engine/install/ubuntu/
- sudo apt-get update
- sudo apt-get install docker-model-plugin
- docker model version
- docker model pull ai/qwen3-coder
- docker model run ai/qwen3-coder
- http://localhost:12434/engines/v1
- docker model pull ai/gpt-oss:120B-MXFP4
- docker model run ai/gpt-oss:120B-MXFP4
- docker model run ai/gpt-oss:120B-MXFP4 "What is the capital of France?"

curl http://10.0.0.111:12434/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "ai/smollm2",
  "messages": [{"role": "user", "content": "What is Docker?"}]
}'

- clear GPU memory?:
- sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
- change context size
- docker model configure --context-size=131000 ai/smollm2

```

### Overall Status of DMR

I have been try to use DMR for other tasks like Vibe Coding (next section), with limited luck.

A couple take-aways:
- need to adjust context window for models with DMR using "configure" above
- may need to increase the context window for a given model within OpenWebUI also


## Playbook: Vibe Coding in VS Code

TODO

https://build.nvidia.com/spark/vibe-coding

- about setup
- struggle with continue.dev
- insiders
- dmr
- still stuck

## Bonus: Immich photo Server

TODO

Described as "local alternative to Google Photos"


## Playbook: Set up Tailscale on Your Spark

TODO

https://build.nvidia.com/spark/tailscale

## Playbook: Text to Knowledge Graph

TODO

https://build.nvidia.com/spark/txt2kg

- from code inspection, script checks if local
- seems to require local ollama
- derailed looking for local replacement for Copilot with Continue.dev or VS Code Insiders


## Follow up Tasks
- [x] finish Playbook: Open WebUI with Ollama
- [x] finish Bonus: Docker Model Runner
- [ ] describe DMR setup for OpenWebUI
- [ ] describe DMR setup for Continue.dev?
- [ ] finish Playbook: Vibe Coding in VS Code
- [ ] finish Bonus: Immich photo Server
- [ ] finish Playbook: Set up Tailscale on Your Spark
- [ ] complete and finish Playbook: Text to Knowledge Graph

- [ ] look for updates or fixes for "nvtop" lack of memory tracking
- [ ] back to Tailscale, describe how to use, and use it for immich, others


## REFERENCES
- https://build.nvidia.com/spark
- https://build.nvidia.com/spark/dgx-dashboard
- "nvidia-smi"
- "nvtop"
- https://build.nvidia.com/spark/open-webui
-
- https://build.nvidia.com/spark/vibe-coding
- 
- https://build.nvidia.com/spark/tailscale
- 
- https://build.nvidia.com/spark/txt2kg
-
- https://github.com/NVIDIA/dgx-spark-playbooks/tree/main


## (PRIVATE) REFERENCES

Mostly links to private repos for my own reference.

- https://github.com/alpiepho/ollama_stuff
- https://github.com/alpiepho/openwebui_stuff
- https://github.com/alpiepho/docker_model_stuff



