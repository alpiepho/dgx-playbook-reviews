This is a collection of personal reviews of many of the NVIDIA DGX Spark Playbook tutorials that can be found at
https://build.nvidia.com/spark.

Why do this? As I have found, if you follow the tutorials to the letter, they work pretty well.  However, if you stray or try variants, there can be unexpected behavior and issues. 

Each review will likely be shorter, more to the point, with less spin on how wonderful it is :). 

## Playbook: DGX-Dashboard

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

https://build.nvidia.com/spark/open-webui

- docker install
- how to update open web ui is nice
- manual docker and hooks into sync with scripts
- prefer docker compose (add below for ollama and open web ui)
- use docker exec to get into ollama and add models



## Bonus: Docker Model Runner

TODO

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
- [ ] finish Playbook: Open WebUI with Ollama
- [ ] finish Bonus: Docker Model Runner
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


