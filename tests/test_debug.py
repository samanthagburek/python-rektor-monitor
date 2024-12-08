import subprocess
import os

def test_debug():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_rekor_monitor'))
    debugmode = "enabled debug mode\n"
    result = subprocess.run(
        ['python3', 'main.py', "--debug"],
        capture_output=True,
        text=True,
        cwd = root_dir
    )
    output = result.stdout

    assert debugmode == output

if __name__ == "__main__":
    test_debug()