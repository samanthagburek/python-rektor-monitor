import subprocess

def test_consistency_no_tree_id():
    no_tree_output = "please specify tree id for prev checkpoint\n"

    consistency = subprocess.run(
        ['python3', 'main.py', '--consistency'],
        capture_output=True,
        text=True
    )
    consistency_output = consistency.stdout

    assert no_tree_output == consistency_output


if __name__ == "__main__":
    test_consistency_no_tree_id()