import subprocess

def test_no_artifact():
    noartifact = "Please include artifact file\n"
    result = subprocess.run(
        ['python3', 'main.py', '--inclusion', "129351"],
        capture_output=True,
        text=True
    )
    output = result.stdout
    assert output == noartifact

if __name__ == "__main__":
    test_no_artifact()