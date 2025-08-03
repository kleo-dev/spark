import os
import sys
import subprocess
import getpass
import venv

home = os.path.expanduser("~")
os.chdir(home)

spark_dir = os.path.join(home, ".spark")

# Clone or update spark repo
if not os.path.exists(spark_dir):
    print("Cloning spark repository...")
    subprocess.run(["git", "clone", "https://github.com/kleo-dev/spark.git", ".spark"], check=True)
else:
    print(".spark directory exists, updating.")
    subprocess.run(["git", "-C", spark_dir, "pull"], check=True)

# Create bin and venv directories
bin_dir = os.path.join(spark_dir, "bin")
venv_dir = os.path.join(spark_dir, "venv")
os.makedirs(bin_dir, exist_ok=True)

# Create virtual environment
if not os.path.exists(os.path.join(venv_dir, "bin", "activate")):
    print("Creating virtual environment...")
    venv.create(venv_dir, with_pip=True)
else:
    print("Virtual environment already exists.")

# Install dependencies into venv
print("Installing google-generativeai into virtual environment...")
subprocess.run([os.path.join(venv_dir, "bin", "pip"), "install", "--upgrade", "pip"], check=True)
subprocess.run([os.path.join(venv_dir, "bin", "pip"), "install", "google-generativeai"], check=True)

# Write executable wrapper script
spark_script = os.path.join(bin_dir, "spark")
with open(spark_script, 'w') as f:
    f.write(f"""#!/bin/bash
source "{venv_dir}/bin/activate"
python3 "{os.path.join(spark_dir, 'main.py')}" "$@"
""")
os.chmod(spark_script, 0o755)

# Ensure PATH includes spark/bin
path_line = 'export PATH="$HOME/.spark/bin:$PATH"\n'
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

# Prompt for API key
gemini_key = getpass.getpass('Enter your Google Gemini API key: ')
with open(os.path.join(spark_dir, 'keys.py'), 'w') as f:
    f.write(f'API_KEY: str = "{gemini_key}"\n')

print("✅ Installation complete.")
print("👉 Restart your shell or run 'source ~/.bashrc' (or equivalent) to update your PATH.")
