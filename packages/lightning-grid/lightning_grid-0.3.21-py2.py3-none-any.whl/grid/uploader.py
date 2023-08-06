"""
Uploader that uploads files into Cloud storage
"""
import requests
from typing import Dict

from concurrent.futures import ThreadPoolExecutor, as_completed


class S3DatastoreUploader:
    """
    This class uploads directory into S3

    Attributes
    ----------
    source_file: str
        Source file to upload
    presigned_urls: Dict[int, str]
        Presigned urls dictionary, with key as part number and values as urls
    part_size: int
        Amount of data to send per part
    """
    workers: int = 4

    def __init__(self, source_file: str, presigned_urls: Dict[int, str],
                 part_size: int):
        self.source_file = source_file
        self.presigned_urls = presigned_urls
        self.part_size = part_size
        self.upload_etags = None

    @staticmethod
    def upload_s3_data(url: str, data: bytes) -> str:
        """
        Send data to s3 url

        Parameters
        ----------
        url: str
            S3 url string to send data to
        data: bytes
            Bytes of data to send to

        Returns
        -------
        str
            ETag from response
        """
        response = requests.put(url, data=data)
        if 'ETag' not in response.headers:
            raise ValueError("Unexpected response from S3, headers: " +
                             f"{response.headers}")

        return response.headers['ETag']

    def _upload_part(self, url: str, part: int) -> None:
        """
        Upload part of the data file with presigned url

        Parameters
        ----------
        url: str
            Presigned url to upload to S3
        part: int
            Part number to read from
        """
        with open(self.source_file, 'rb') as f:
            pos = self.part_size * (part - 1)
            f.seek(pos)
            data = f.read(self.part_size)
            self.upload_etags[part] = self.upload_s3_data(url, data)

    def upload(self) -> Dict[int, str]:
        """
        Upload files from source dir into target path in S3
        """
        self.upload_etags = {}
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            futures = []
            for part, url in self.presigned_urls.items():
                f = pool.submit(self._upload_part, url, part)
                futures.append(f)

            for future in as_completed(futures):
                future.result()

        return self.upload_etags
