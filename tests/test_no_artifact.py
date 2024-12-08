import subprocess
import os


def test_no_artifact():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_rekor_monitor'))
    noartifact = "Please include artifact file\n"
    result = subprocess.run(
        ['python3', 'main.py', '--inclusion', "129351"],
        capture_output = True,
        text = True,
        cwd = root_dir
    )
    output = result.stdout
    assert output == noartifact

if __name__ == "__main__":
    test_no_artifact()