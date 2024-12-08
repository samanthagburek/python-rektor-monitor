import subprocess
import os

def test_artifact_correct():
    validsignature = "Signature is valid"
    validinclusion = "Offline root hash calculation for inclusion verified."
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_rekor_monitor'))
    print(root_dir)
    result = subprocess.run(
        ['python3', 'main.py', '--inclusion', "129593524", "--artifact", "../artifact.md"],
        capture_output=True,
        text=True,
        cwd=root_dir
    )
    output = result.stdout.split('\n')
    signatureoutput = output[0]
    inclusionoutput = output[1]

    assert signatureoutput == validsignature
    assert validinclusion == inclusionoutput
    assert len(output) == 2

if __name__ == "__main__":
    test_artifact_correct()