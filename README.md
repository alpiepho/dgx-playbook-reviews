This is a collection of personal reviews of many of the NVIDIA DGX Spark Playbook tutorials that can be found at
https://build.nvidia.com/spark.

Why do this? As I have found, if you follow the tutorials to the letter, they work pretty well.  However, if you stray or try variants, there can be unexpected behavior and issues. 

Each review will likely be shorter, more to the point, with less spin on how wonderful it is :). 

## Table of Contents

- [Quick Summary](#quick-summary)
- [Playbook: DGX-Dashboard](#playbook-dgx-dashboard)
- [Playbook: Open WebUI with Ollama](#playbook-open-webui-with-ollama)
- [Bonus: Docker Model Runner](#bonus-docker-model-runner)
- [Playbook: Vibe Coding in VS Code](#playbook-vibe-coding-in-vs-code)
- [Playbook: Set up Tailscale on Your Spark](#playbook-set-up-tailscale-on-your-spark)
- [Bonus: Immich photo Server](#bonus-immich-photo-server)
- [Playbook: Text to Knowledge Graph](#playbook-text-to-knowledge-graph)
- [Follow up Tasks](#follow-up-tasks)
- [REFERENCES](#references)
- [(PRIVATE) REFERENCES](#private-references)

## Quick Summary

| Playbook | Status | Recommendation |
|----------|--------|----------------|
| DGX-Dashboard | ✅ Works | Use `nvidia-smi` or `nvtop` instead for better GPU monitoring |
| Open WebUI with Ollama | ✅ Works | Recommended; separate Ollama/WebUI for better control |
| Docker Model Runner | ✅ Works | Good alternative to Ollama; requires context window adjustment |
| Vibe Coding in VS Code | ⚠️ Partial | Use VS Code Insiders with Copilot (free); Continue.dev not recommended |
| Tailscale | ✅ Works | Excellent; perfect for secure remote access |
| Text to Knowledge Graph | ⏳ TODO | In progress |

## Playbook: DGX-Dashboard

11/30/2025

https://build.nvidia.com/spark/dgx-dashboard

Really simple install.  The dashboard is basically a tool tray app (OS independant) that uses ssh to connect to your Spark.  It launches a Webpage to show a simple Dashboard.  I found the GPU and memory usage to be less responsive that other tools.  Hard to determine if 

The first alternative to watch for GPU usage is to ssh into the Spark and use "nvidia-smi".

```bash
watch -n 1 nvidia-smi
```

Another alternative for watching GPU usage is "nvtop".  This is more responsive to GPU usage, say by using OpenWebUI connected to an Ollama docker container on the Spark.  Cannot get the memory tracking working.  Read about running as sudo, but that seems to lock up the Spark.  Adding a Follow up task.

The one click "update" is nice, but you can do this from ssh/command line:

```bash
sudo apt update
sudo apt dist-upgrade
sudo fwupdmgr refresh
sudo fwupdmgr upgrade
sudo reboot
```

## Playbook: Open WebUI with Ollama

12/10/2025

https://build.nvidia.com/spark/open-webui

The first steps for installing Docker on Ubuntu are good. 

The instructions try to make it easier by using a combined OpenWebUI + Ollama docker container.  I wanted to separate them so I followed other options suggested by Copilot (sorry, no references).

**Separated Docker Compose setup** - Created two separate services for better control:

Ollama service (`ollama_stuff/docker-compose.yaml`):

```yaml
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

Open WebUI service (`openwebui_stuff/docker-compose.yaml`):

```yaml
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

**Starting and stopping services:**

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

```bash
docker exec -it ollama bash
ollama ls
ollama pull smollm2 # or other model
```

**Summary:** Works well when following instructions. The separated Ollama/WebUI approach provides better flexibility than the combined container.


## Bonus: Docker Model Runner

12/15/2025

Docker has created an extension to help with local models, similar to Ollama.  

### Key Features

- Uses both llama.cpp and vllm inference engines
- Automatic selection of inference engine based on model
- Uses familiar `ls`, `pull`, `run` commands
- Don't need to use `-exec` into container to update models like Ollama
- Docker Model Runner (DMR) provides OpenAI-compatible API, but at port 12434

### Installation and Usage

Basic setup:

```bash
https://docs.docker.com/engine/install/ubuntu/
sudo apt-get update
sudo apt-get install docker-model-plugin
docker model version
```

Pull and run models:

```bash
docker model pull ai/qwen3-coder
docker model run ai/qwen3-coder
docker model pull ai/gpt-oss:120B-MXFP4
docker model run ai/gpt-oss:120B-MXFP4
docker model run ai/gpt-oss:120B-MXFP4 "What is the capital of France?"
```

OpenAI-compatible API endpoint (accessible at `http://localhost:12434/engines/v1`):

```bash
curl http://10.0.0.111:12434/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "ai/smollm2",
  "messages": [{"role": "user", "content": "What is Docker?"}]
}'
```

Useful management commands:

```bash
# Clear GPU memory
sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'

# Change context size
docker model configure --context-size=131000 ai/smollm2
```

### Summary

Docker Model Runner is a solid alternative to Ollama with a cleaner approach to model management. Key takeaways:
- Must adjust context window for models with DMR using `configure` command
- May need to increase context window for models within OpenWebUI as well
- Works well for direct API access but integration with VS Code Insiders had mixed results


## Playbook: Vibe Coding in VS Code

1/2/2026

https://build.nvidia.com/spark/vibe-coding

### Continue.dev Issues

After trying this setup, I am disappointed with the Continue.dev VS Code plugin. While the instructions were clear, significant features didn't work:

- Could never configure Continue.dev to access local files or directories
- Agent mode failed with timeouts or struggles accessing files
- Workaround: Use Ask mode and manually copy/paste code
- Completely failed with VS Code remote SSH connections

### VS Code Insiders Alternative

Discovered a better approach using VS Code Insiders with Copilot and local model integration ([Alex Ziskind's tutorial](https://youtu.be/IsJcjrQwgF4?si=sCUnsqCBQ3GeF9K4))

### Custom Model Configuration

User settings for integrating local models:

```json
{
    "github.copilot.chat.customOAIModels": {
        "gpt-oss:20b": {
            "name": "gpt-oss:20b",
            "url": "http://10.0.0.111:11434",
            "toolCalling": true,
            "vision": false,
            "thinking": true,
            "maxInputTokens": 128000,
            "maxOutputTokens": 4096,
            "requiresAPIKey": false
        },
        "gpt-oss:120b": {
            "name": "gpt-oss:120b",
            "url": "http://10.0.0.111:11434",
            "toolCalling": true,
            "vision": false,
            "thinking": true,
            "maxInputTokens": 128000,
            "maxOutputTokens": 4096,
            "requiresAPIKey": false
        },
        "gpt-oss:120B-MXFP4": {
            "name": "gpt-oss:120B-MXFP4",
            "url": "http://10.0.0.111:12434",
            "toolCalling": true,
            "vision": false,
            "thinking": true,
            "maxInputTokens": 128000,
            "maxOutputTokens": 4096,
            "requiresAPIKey": false
        },
        "smollm2": {
            "name": "smollm2",
            "url": "http://10.0.0.111:12434",
            "toolCalling": false,
            "vision": false,
            "thinking": true,
            "maxInputTokens": 128000,
            "maxOutputTokens": 4096,
            "requiresAPIKey": false
        }
    }
}
```

**Current Status:** Partially working. Chat mode functions well, but agent mode often times out or reverts to "can we help". Issues found with tool parameter passing and Copilot integration.

**Recommendation:** For production use, recommend free Copilot tier (Claude Haiku 4.5) or the $10/month paid plan. Works both locally and via remote SSH. Be mindful not to share private code with Copilot services.

**Summary:** Despite high expectations, Continue.dev lacks file access capabilities and agent features are unreliable. VS Code Insiders with Copilot offers better stability and is worth the cost for professional development work.

## Playbook: Set up Tailscale on Your Spark

12/20/2025

https://build.nvidia.com/spark/tailscale

The instructions for Tailscale worked perfectly. The hardest part is understanding the concept and authentication flow. These resources help:

- https://www.youtube.com/@Tailscale/videos
- https://youtu.be/zngSuqCM4d8?si=QTEoXT9aVvCUU4-G
- https://youtu.be/guHoZ68N3XM?si=nI2l-Qo-O7y1K5DP

**Security & Access Control:** Being cautious about exposing internal servers, I spent time planning how to limit Tailscale access. The VM separation strategy (discussed in Immich section below) helps isolate services on a per-VM basis within the Tailnet.

**Summary:** Excellent solution for secure remote access to DGX Spark. Highly recommended once you understand the networking concepts. Security controls are well-designed and flexible.


## Bonus: Immich photo Server

1/2/2026

Described as "local alternative to Google Photos". I previously installed this as a Docker container and am adding it here because of its integration with Tailscale for secure remote photo access.

### Installation & Import

Installation is straightforward, but bulk photo import requires some care. Use the CLI for better control:

```bash
docker run -it -v "/home/user/Photos:/import:ro" --env-file .env ghcr.io/immich-app/immich-cli:latest upload --recursive /import
```

### EXIF Tag Challenges

Older photos and Google Takeout exports lack proper EXIF metadata. Photos without tags end up in the "Today" category. Created custom tools to extract metadata from Google Takeout JSON files and apply it to photos—still a work in progress.

### Architecture & Tailscale Integration

Rather than run Immich on the DGX Spark (which doesn't need GPU), I migrated it to a separate Proxmox VM running Ubuntu with Docker. This approach:
- Keeps GPU resources free for DGX workloads
- Isolates the 500GB+ photo library from the Spark
- Allows Tailscale access to be configured at the VM level
- Provides better service separation and security

**Summary:** Solid local photo management solution. The architecture decisions around VMs and Tailscale access make it production-ready for home deployment.


## Playbook: Text to Knowledge Graph

TODO

https://build.nvidia.com/spark/txt2kg

- from code inspection, script checks if local
- seems to require local ollama
- derailed looking for local replacement for Copilot with Continue.dev or VS Code Insiders


## Follow up Tasks

**Completed:**
- [x] Open WebUI with Ollama
- [x] Docker Model Runner
- [x] Vibe Coding in VS Code
- [x] Immich photo Server
- [x] Tailscale on DGX Spark

**Deferred (Not Pursuing):**
- [-] DMR setup for OpenWebUI (Ollama sufficient)
- [-] Continue.dev integration (plugin unreliable, using Copilot instead)

**In Progress:**
- [ ] Text to Knowledge Graph
- [ ] Immich EXIF metadata tools
- [ ] Tailscale access patterns & security best practices

**Future Investigation:**
- [ ] Updates for "nvtop" memory tracking
- [ ] Evaluate VS Code Insiders with alternative models
- [ ] Explore NotebookLM integration with Continue documentation


## REFERENCES

**NVIDIA DGX Spark Playbooks:**
- https://build.nvidia.com/spark
- https://build.nvidia.com/spark/dgx-dashboard
- https://build.nvidia.com/spark/open-webui
- https://build.nvidia.com/spark/vibe-coding
- https://build.nvidia.com/spark/tailscale
- https://build.nvidia.com/spark/txt2kg
- https://github.com/NVIDIA/dgx-spark-playbooks/tree/main

**GPU Monitoring Tools:**
- nvidia-smi
- nvtop

**VS Code & Copilot:**
- [Using VS Code Insiders with Local Models](https://youtu.be/IsJcjrQwgF4?si=sCUnsqCBQ3GeF9K4) (Alex Ziskind, YouTube)
- [Copilot Supported Models](https://docs.github.com/en/copilot/reference/ai-models/supported-models)
- [Copilot Plans & Pricing](https://docs.github.com/en/copilot/get-started/plans)

**Docker & Local Models:**
- [Docker Engine Installation](https://docs.docker.com/engine/install/ubuntu/)
- [Docker Model Runner](https://docs.docker.com/ai/model-runner/)

**Network & Remote Access:**
- [Tailscale Official Channel](https://www.youtube.com/@Tailscale/videos)
- [Tailscale Tutorial](https://youtu.be/zngSuqCM4d8?si=QTEoXT9aVvCUU4-G)

**Photo Management:**
- [Immich Documentation](https://immich.app/)
- [Google Takeout Export](https://takeout.google.com/)


## (PRIVATE) REFERENCES

Mostly links to private repos for my own reference.

- https://github.com/alpiepho/ollama_stuff
- https://github.com/alpiepho/openwebui_stuff
- https://github.com/alpiepho/docker_model_stuff
- https://github.com/alpiepho/immich_stuff
- https://github.com/alpiepho/imich_exif_fixer
- https://github.com/alpiepho/immich_takeout_fixer




