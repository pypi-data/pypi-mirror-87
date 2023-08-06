import os
import tempfile
import tarfile
import unittest

from grid.tar import tar_directory_unix


class TarTestCase(unittest.TestCase):
    """
    Test tar
    """
    @staticmethod
    def test_tar_directory():
        with tempfile.TemporaryDirectory() as temp_dir:
            inner_dir = os.path.join(temp_dir, "dir")
            os.makedirs(inner_dir)
            staging_dir = os.path.join(temp_dir, "staging_dir")
            os.makedirs(staging_dir)
            with open(os.path.join(temp_dir, "f1"), 'w') as f:
                f.write("f1")

            with open(os.path.join(inner_dir, "f2"), 'w') as f:
                f.write("f2")

            with open(os.path.join(staging_dir, "f3"), 'w') as f:
                f.write("f3")

            target_file = os.path.join(staging_dir, "target.tar.gz")
            tar_directory_unix(source_dir=temp_dir,
                               temp_dir="staging_dir",
                               target_file=target_file)

            verify_dir = os.path.join(temp_dir, "verify")
            os.makedirs(verify_dir)
            with tarfile.open(target_file) as target_tar:
                target_tar.extractall(verify_dir)

            assert os.path.exists(os.path.join(verify_dir, "f1"))
            assert os.path.exists(os.path.join(verify_dir, "dir", "f2"))
            assert not os.path.exists(os.path.join(verify_dir, "staging_dir"))
