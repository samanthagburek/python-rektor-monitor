# Python Rekor Monitor Template

## Prerequisite:
- Install cosign: https://docs.sigstore.dev/cosign/system_config/installation/

## Steps:
1. Sign an artifact using cosign tool with your identity using:
```bash
    cosign sign-blob <file> --bundle cosign.bundle
  ```
More info on signing blobs is here: https://docs.sigstore.dev/cosign/signing/signing_with_blobs/

2. Fetch latest checkpoints from Rekor log using:
```bash
    rekor-monitor -c
  ```

3. Verify that the artifact signature in the transparency log is correct and verify that the log entry is included in the latest checkpoint of the transparency log by verifying the inclusion Proof merkle proof
```bash
    rekor-monitor --inclusion <logIndex of signed artifact> --artifact <artifact file>
  ```

4. Verify that the checkpoint which had our entry added is consistent with the latest checkpoint using the checkpoint details obtained in step 2.
```bash
    rekor-monitor --consistency --tree-id <treeid in latest checkpoint> --tree-size <treesize in latest checkpoint> --root-hash <roothash in latest checkpoint>
  ```


Notes:
Hw 4
Install all dependencies and build poetry with 
```bash
    poetry add ($cat requirements.txt)
    poetry build
  ```
Test with 
```bash
    pip install dist/python_rektor_monitor-0.1.0-py3-none-any.whl
    rekor-monitor -c
  ```
SBOM Attestation  
- need to verify the type of predicate given
- using OIDC as a key is the default if no key argument given
```bash
    cosign attest-blob dist/python_rektor_monitor-0.1.0-py3-none-any.whl --predicate cyclonedx-sbom.json --type cyclonedx --bundle sbom.bundle
    cosign verify-blob-attestation --bundle sbom.bundle dist/python_rektor_monitor-0.1.0-py3-none-any.whl --certificate-identity samanthagburek --certificate-oidc-issuer https://github.com --type cyclonedx --check-claims
  ```

