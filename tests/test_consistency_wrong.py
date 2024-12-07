import sys
import os
import pytest
from python_rekor_monitor.main import main
from python_rekor_monitor.merkle_proof import RootMismatchError
from unittest import mock


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_artifact_wrong(mocker):
    mocker.patch("sys.argv",['main.py', '--consistency', '--tree-id', "119305095991665606", '--tree-size', '26302632', 
         '--root-hash', "1c6e7655044c6e3e475e038edc9d54af62d0ba7de898b6ae06f31d4067769830"])
    with pytest.raises(RootMismatchError):
        main()

if __name__ == "__main__":
    mocker = mock.MagicMock()
    test_artifact_wrong(mocker)