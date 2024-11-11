import sys
import os
import pytest
import subprocess
from merkle_proof import RootMismatchError
from main import main

def test_consistency_wrong():
    consistency = subprocess.run(
        ['python3', 'main.py', '--consistency', '--tree-id', "119305095991665606", '--tree-size', '26302632', 
         '--root-hash', "1c6e7655044c6e3e475e038edc9d54af62d0ba7de898b6ae06f31d4067769830"],
        capture_output=True,
        text=True
    )
    output = consistency.stdout
    #Should raise a Root Mismatch Error 
    assert "does not match expected root:" in output

if __name__ == "__main__":
    test_consistency_wrong()