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


