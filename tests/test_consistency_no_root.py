import subprocess
import os

def test_consistency_no_tree_id():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_rekor_monitor'))
    no_tree_output = "please specify root hash for prev checkpoint\n"

    consistency = subprocess.run(
        ['python3', 'main.py', '--consistency', '--tree-id', '344567', '--tree-size', '3545567'],
        capture_output=True,
        text=True,
        cwd = root_dir
    )
    consistency_output = consistency.stdout

    assert no_tree_output == consistency_output


if __name__ == "__main__":
    test_consistency_no_tree_id()