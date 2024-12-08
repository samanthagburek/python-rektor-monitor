import subprocess
import os 

def test_artifact_wrong():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_rekor_monitor'))
    invalidsignature = "Signature is invalid"
    validinclusion = "Offline root hash calculation for inclusion verified."
    
    result = subprocess.run(
        ['python3', 'main.py', '--inclusion', "129593524", "--artifact", "../artifact2.md"],
        capture_output=True,
        text=True,
        cwd=root_dir
    )
    output = result.stdout
    output = result.stdout.split('\n')
    signatureoutput = output[0]
    inclusionoutput = output[1]

    assert signatureoutput == invalidsignature
    assert validinclusion == inclusionoutput
    assert len(output) == 2

if __name__ == "__main__":
    test_artifact_wrong()