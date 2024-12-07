import subprocess

def test_debug():
    debugmode = "enabled debug mode\n"
    result = subprocess.run(
        ['python3', 'main.py', "--debug"],
        capture_output=True,
        text=True
    )
    output = result.stdout

    assert debugmode == output

if __name__ == "__main__":
    test_debug()