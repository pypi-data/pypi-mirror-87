import os
import pytest
import tempfile

from grid.uploader import S3DatastoreUploader, requests


def test_s3_uploader():
    with tempfile.NamedTemporaryFile() as f:
        p1 = os.urandom(256)
        p2 = os.urandom(256)
        p3 = os.urandom(256)
        p4 = os.urandom(256)
        for p in [p1, p2, p3, p4]:
            f.write(p)
        f.flush()

        urls = {
            1: "http://grid.ai/1",
            2: "http://grid.ai/2",
            3: "http://grid.ai/3",
            4: "http://grid.ai/4"
        }

        parts = {
            "http://grid.ai/1": p1,
            "http://grid.ai/2": p2,
            "http://grid.ai/3": p3,
            "http://grid.ai/4": p4
        }

        def mock_upload_data(url, data):
            assert parts[url] == data

            return url[-1]

        uploader = S3DatastoreUploader(source_file=f.name,
                                       presigned_urls=urls,
                                       part_size=int(1024 / 4))
        uploader.upload_s3_data = mock_upload_data

        etags = uploader.upload()
        assert etags == {1: "1", 2: "2", 3: "3", 4: "4"}


def test_upload_s3_data(monkeypatch):
    class Response:
        headers = {'ETag': 'test-e-tag'}

    def mp_put(*args, **kwargs):
        return Response

    monkeypatch.setattr(requests, 'put', mp_put)
    result = S3DatastoreUploader.upload_s3_data(url='test-url', data=b'test')
    assert result == 'test-e-tag'


def test_upload_s3_data_raises_exception(monkeypatch):
    """upload_s3_data() if no ETag in headers"""
    class Response:
        headers = {}

    def mp_put(*args, **kwargs):
        return Response

    monkeypatch.setattr(requests, 'put', mp_put)
    with pytest.raises(ValueError):
        S3DatastoreUploader.upload_s3_data(url='test-url', data=b'test')
