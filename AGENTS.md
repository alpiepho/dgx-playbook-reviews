# AGENTS.md

## Overview
This repository contains personal reviews, notes, and implementation details for NVIDIA DGX Spark Playbook tutorials and related projects (e.g., llama.cpp, summary_stuff). It serves as a knowledge base for maintaining and extending local AI deployments on DGX Spark.

## Core Projects & Context
- **DGX Spark Playbooks**: Reviews of NVIDIA tutorials (Dashboard, Open WebUI, Tailscale, etc.).
- **llama.cpp**: Tracking updates, particularly regarding multimodal (mtmd), Vulkan, and Metal backends, and specific model support (Gemma 4, Qwen 3).
- **summary_stuff**: A project involving text processing/summarization (often involving Python/bash scripts).
- **stacked_graph_claude**: A PWA project using Chart.js for CSV data visualization.
- **gh-repo-inspector**: A tool for inspecting GitHub repositories.

## Key Learnings (High Signal)
- **DGX GPU Monitoring**: `nvidia-smi` or `nvtop` are more responsive than the DGX-Dashboard tool.
- **Open WebUI + Ollama**: For better control, use separate Docker Compose services for Ollama and Open WebUI instead of the combined container.
- **Docker Model Runner (DMR)**: A solid alternative to Ollama; requires manual context window adjustment via `docker model configure --context-size=<size>`.
- **VS Code Integration**: `Continue.dev` has known issues with file access and agent mode in remote SSH environments. Use **VS Code Insiders with GitHub Copilot** for more stable local/remote model integration.
- **Tailscale**: Excellent for secure remote access to DGX Spark.

## Development Environment & Tools
- **Preferred IDEs**: VS Code, VS Code Insiders, Cursor.
- **Remote Access**: Tailscale is used for secure SSH/WebUI access to the DGX Spark.
- **Infrastructure**: Proxmox VMs are used to isolate services (e.g., Immich) from the main DGX Spark to keep GPU resources free.

## Command Reference
### GPU Monitoring
```bash
watch -n 1 nvidia-smi
# or
nvtop
```

### Docker Model Runner (DMR)
```bash
# Update context size
docker model configure --context-size=131000 ai/smollm2

# Run model
docker model run ai/qwen3-coder
```

### System Updates (DGX)
```bash
sudo apt update && sudo apt dist-upgrade
sudo fwupdmgr refresh && sudo fwupdm0 upgrade
```
