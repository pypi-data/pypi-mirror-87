import shutil
import unittest

from pathlib import Path
from grid.downloader import Downloader, DownloadableObject


class ArtifactCallbacksTestCase(unittest.TestCase):
    """Tests callbacks in grid artifacts."""
    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'tests/data/download_path/nested_dir'

    @classmethod
    def tearDown(cls):
        # Deletes test directory with all files.
        path = Path(cls.test_dir)
        shutil.rmtree(path, ignore_errors=True)

    def test_downloader_creates_dir(self):
        """Downloader.create_dir_tree creates dir structure in path."""
        Downloader.create_dir_tree(self.test_dir)
        assert Path(self.test_dir).exists()

    def test_downloader_downloads_data(self):
        """Downloader().download() downloads data in nested directories."""
        # Google logo
        # skipcq: FLK-E501
        url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
        directory_path = 'nested_0/nested_1'
        filename = 'test-filename.png'
        objects = [
            DownloadableObject(url=url,
                               download_path=directory_path,
                               filename=filename)
        ]

        # Download file
        D = Downloader(downloadable_objects=objects, base_dir=self.test_dir)
        D.download()

        # Test that file as been downloaded.
        assert Path(self.test_dir).joinpath(directory_path).joinpath(
            filename).exists()
