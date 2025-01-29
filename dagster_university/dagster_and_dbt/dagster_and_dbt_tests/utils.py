import subprocess


def run_dbt_command(command: str, dir: str):
    cmd = ["dbt", command, "--project-dir", dir, "--profiles-dir", dir]
    subprocess.run(cmd, capture_output=True, text=True)
