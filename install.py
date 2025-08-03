import os
import sys
import subprocess

home = os.path.expanduser("~")
os.chdir(home)

spark_dir = os.path.join(home, ".spark")

if not os.path.exists(spark_dir):
    print("Cloning spark repository...")
    subprocess.run(["git", "clone", "https://github.com/kleo-dev/spark.git", ".spark"], check=True)
else:
    print(".spark directory exists, updating.")
    subprocess.run(["git", "-C", spark_dir, "pull"], check=True)

bin_dir = os.path.join(spark_dir, "bin")
os.makedirs(bin_dir, exist_ok=True)

spark_script = os.path.join(bin_dir, "spark")

with open(spark_script, 'w') as f:
    f.write(f"#!/bin/bash\npython3 {os.path.join(spark_dir, 'main.py')} \"$@\"\n")

os.chmod(spark_script, 0o755)  # Make executable

path_line = 'export PATH="$HOME/.spark/bin:$PATH"\n'

# Append PATH to rc files if not already there
for rc in os.listdir(home):
    if rc.startswith('.') and rc.endswith('rc') and os.path.isfile(os.path.join(home, rc)):
        rc_path = os.path.join(home, rc)
        with open(rc_path, 'r') as f:
            content = f.read()
        if path_line.strip() not in content:
            with open(rc_path, 'a') as f:
                f.write('\n' + path_line)
            print(f"Added PATH export to {rc_path}")
        else:
            print(f"PATH export already present in {rc_path}")

print("Installation complete. Restart your shell or run 'source ~/.bashrc' (or equivalent) to update PATH.")
