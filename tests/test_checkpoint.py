import json
import jsonschema
import subprocess
import os 

checkpoint_schema = {
    "type": "object",
    "properties": {
        "inactiveShards": {"type": "array"},
        "rootHash": {"type": "string"},
        "signedTreeHead": {"type": "string"},
        "treeID": {"type": "string"},
        "treeSize": {"type": "integer"}
    },
    "required": ["inactiveShards", "rootHash", "signedTreeHead", "treeID", "treeSize"]
}

def test_checkpoint():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_rekor_monitor'))
    result = subprocess.run(
        ['python3', 'main.py', '-c'],
        capture_output=True,
        text=True,
        cwd = root_dir
    )
    output = result.stdout
    data = json.loads(output)

    jsonschema.validate(instance=data, schema=checkpoint_schema)

if __name__ == "__main__":
    test_checkpoint()