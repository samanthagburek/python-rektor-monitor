import json
import os
import subprocess

def test_consistency():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_rekor_monitor'))
    correct_consistency = "Consistency verification successful.\n"
    checkpoint = subprocess.run(
        ['python3', 'main.py', '-c'],
        capture_output=True,
        text=True,
        cwd = root_dir
    )
    output = checkpoint.stdout
    data = json.loads(output)
    rootHash = data["rootHash"]
    treeID = data["treeID"]
    treeSize = str(data["treeSize"])

    consistency = subprocess.run(
        ['python3', 'main.py', '--consistency', '--tree-id', treeID, '--tree-size', treeSize, 
         '--root-hash', rootHash],
        capture_output=True,
        text=True,
        cwd = root_dir
    )
    consistency_output = consistency.stdout

    assert consistency_output == correct_consistency


if __name__ == "__main__":
    test_consistency()