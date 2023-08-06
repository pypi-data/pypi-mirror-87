from io import BytesIO
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile


class ZipPackage:
    def __init__(self, path: str = None, data: bytes = None, mode: str = None) -> None:
        if path is not None:
            with open(path, "rb") as source_fp:
                self.stream = BytesIO(source_fp.read())
        else:
            self.stream = BytesIO(data)
        self.package = ZipFile(self.stream, mode)

    def read_file(self, arcname: str) -> bytes:
        return self.package.read(arcname)

    def write_file(self, arcname: str, path: str = None, data: bytes = None) -> None:
        if path is not None:
            self.package.write(path, arcname, compress_type=ZIP_DEFLATED)
        elif data is not None:
            self.package.writestr(arcname, data, compress_type=ZIP_DEFLATED)
        else:
            raise Exception("need input file path or bytes data ")

    def close(self, save_to: str = None) -> bytes:
        self.package.close()
        self.package = None
        compressed_bytes = self.stream.getvalue()
        if save_to is not None:
            with open(save_to, "wb") as save_fp:
                save_fp.write(compressed_bytes)
        self.stream.close()
        self.stream = None
        return compressed_bytes
