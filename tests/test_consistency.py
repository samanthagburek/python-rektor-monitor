import json
import subprocess

def test_consistency():
    correct_consistency = "Consistency verification successful.\n"
    checkpoint = subprocess.run(
        ['python3', 'main.py', '-c'],
        capture_output=True,
        text=True
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
        text=True
    )
    consistency_output = consistency.stdout

    assert consistency_output == correct_consistency


if __name__ == "__main__":
    test_consistency()