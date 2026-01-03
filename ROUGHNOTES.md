# Playbook Review Notes

## DGX Playbook Status

### Issues & Learnings
- First setup works
- Works for chat use cases
- Agent functionality not working well
- Spent significant time configuring local file access
- Model runners tested:
  - Doctor model runner (less stable than Llama)
  - Llama (more stable)
- SSH integration with S3 code had poor behavior

### Documentation Improvements Needed
- [ ] Add sample configuration files
- [ ] Take screenshots for documentation
- [ ] Create detailed documentation page
- [ ] Add references with links
- [ ] Consider publishing on GitHub

## Local Development & Tools

### Current Preference
- Using Copilot, Cursor, or VS Code (rather than local alternatives)
- Keeping local GPU for data processing

### Tools to Explore
- [ ] VS Code Insiders
- [ ] Other local code tools
- [ ] Continue CoI (evaluation pending)
- [ ] NotebookLM integration with Continue documents

## Tailscale Playbook

### Status
- Followed example - works well

### Documentation Improvements
- [ ] Add links to Tailscale documentation
- [ ] Link to Proxmox box documentation
- [ ] Document VM separation strategy (Doctor vs Spark)
