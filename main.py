import subprocess
import sys
import os
import shutil

INSTALL_URL = "https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh"
REQUIRED_BINARIES = ["bash", "curl", "systemctl"]


def check_requirements() -> bool:
    if os.geteuid() != 0:
        print("[ERROR] Root privileges are required.")
        return False
    for binary in REQUIRED_BINARIES:
        if shutil.which(binary) is None:
            print(f"[ERROR] Required binary not found: {binary}")
            return False
    return True


def fetch_installer(target_path: str = "/tmp/3xui_install.sh") -> bool:
    try:
        subprocess.run(
            ["curl", "-Ls", INSTALL_URL, "-o", target_path],
            check=True,
            capture_output=True,
            text=True,
        )
        os.chmod(target_path, 0o700)
        return True
    except subprocess.CalledProcessError as exc:
        print(f"[ERROR] Failed to download installer: {exc.stderr}")
        return False


def run_installer(script_path: str = "/tmp/3xui_install.sh") -> bool:
    try:
        process = subprocess.Popen(
            ["bash", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
        process.wait()
        return process.returncode == 0
    except Exception as exc:
        print(f"[ERROR] Installer execution failed: {exc}")
        return False


def cleanup(script_path: str = "/tmp/3xui_install.sh") -> None:
    if os.path.exists(script_path):
        os.remove(script_path)


def main() -> int:
    if not check_requirements():
        return 1
    if not fetch_installer():
        return 1
    success = run_installer()
    cleanup()
    if success:
        print("[INFO] 3X-UI installation completed successfully.")
        return 0
    print("[ERROR] 3X-UI installation failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
