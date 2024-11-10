import sys
import json
from jsonschema import validate
import subprocess
import requests

def test_consistency_no_tree_size():
    no_tree_output = "please specify tree size for prev checkpoint\n"

    consistency = subprocess.run(
        ['python3', 'main.py', '--consistency', '--tree-id', '344567'],
        capture_output=True,
        text=True
    )
    consistency_output = consistency.stdout

    assert no_tree_output == consistency_output


if __name__ == "__main__":
    test_consistency_no_tree_size()