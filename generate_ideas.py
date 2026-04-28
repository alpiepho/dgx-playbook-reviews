
import subprocess
import os
from datetime import datetime

def get_git_logs(root_dir):
    logs = []
    # Find all .git directories
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            repo_path = root
            # The repo name is the name of the parent directory of .git
            repo_name = os.path.basename(root)
            
            try:
                # Run git log
                cmd = [
                    'git', '-C', repo_path, 
                    'log', 
                    '--since=2026-01-01', 
                    '--format=%ad | %s', 
                    '--date=short'
                ]
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
                
                for line in output.splitlines():
                    if '|' in line:
                        date_str, message = line.split('|', 1)
                        logs.append({
                            'date': date_str.strip(),
                            'repo': repo_name,
                            'message': message.strip()
                        })
            except subprocess.CalledProcessError:
                # Might not be a git repo or error in command
                pass
            except Exception as e:
                print(f"Error processing {repo_path}: {e}")
                
    return logs

def main():
    root_dir = os.path.expanduser('~/Projects/all_github')
    if not os.path.exists(root_dir):
        print(f"Error: {root_dir} does not exist.")
        return

    all_logs = get_git_logs(root_dir)
    
    # Sort by date
    all_logs.sort(key=lambda x: x['date'])
    
    # Group by date to make it look like a timeline
    timeline = []
    if not all_logs:
        print("No logs found for 2026.")
        return

    current_date = None
    current_entries = []

    for entry in all_logs:
        if entry['date'] != current_date:
            if current_date is not None:
                timeline.append((current_date, current_entries))
            current_date = entry['date']
            current_entries = []
        current_entries.append(f"- **{entry['repo']}**: {entry['message']}")

    if current_date is not None:
        timeline.append((current_date, current_entries))

    # Write to IDEAS.md in the current directory
    with open('IDEAS.md', 'w') as f:
        f.write("# Project Timeline - 2026\n\n")
        f.write("A chronological list of work performed across all repositories in 2026.\n\n")
        for date, entries in timeline:
            f.write(f"## {date}\n")
            for entry in entries:
                f.write(f"{entry}\n")
            f.write("\n")

if __name__ == "__main__":
    main()
