import subprocess

def test_artifact_correct():
    validsignature = "Signature is valid"
    validinclusion = "Offline root hash calculation for inclusion verified."
    result = subprocess.run(
        ['python3', 'main.py', '--inclusion', "129593524", "--artifact", "artifact.md"],
        capture_output=True,
        text=True
    )
    output = result.stdout.split('\n')
    signatureoutput = output[0]
    inclusionoutput = output[1]

    assert signatureoutput == validsignature
    assert validinclusion == inclusionoutput
    assert len(output) == 2

if __name__ == "__main__":
    test_artifact_correct()