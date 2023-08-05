# Perseus RESTful API Client Python Library

Repository of classes that provide Pythonic interfaces to connect to a RESTful API server developed with Perseus RESTful API server framework.

## Python Library `Poster 0.8.1`

Note: this library includes a modified version of `poster 0.8.1`, which original version provides a set of classes and functions to facilitate making HTTP POST (or PUT) requests using the standard multipart/form-data encoding.

The original library `poster 0.8.1` cannot be used to upload file uploaded into memory (i.e., stream-to-memory), like for instance django `InMemoryUploadedFile`. The reason is that such file-like object doesn't support the method `fileno()` used by the `poster 0.8.1` to determine the size of the file-like object to upload in Python module `poster.encode`:

```python
if fileobj is not None and filesize is None:
    # Try and determine the file size
    try:
        self.filesize = os.fstat(fileobj.fileno()).st_size
    except (OSError, AttributeError):
        try:
            fileobj.seek(0, 2)
            self.filesize = fileobj.tell()
            fileobj.seek(0)
        except:
            raise ValueError("Could not determine filesize")
```

This code raises the exception `io.UnsupportedOperation` that `poster 0.8.1` doesn't catch. Chris AtLee included Alon Hammerman's patch in the tag `tip` of the library ``poster`, for catching the`io.UnsupportedOperation for fileno` on 2013-03-12:

```python
try:
    from io import UnsupportedOperation
except ImportError:
    UnsupportedOperation = None

(...)

if fileobj is not None and filesize is None:
    # Try and determine the file size
    try:
        self.filesize = os.fstat(fileobj.fileno()).st_size
    except (OSError, AttributeError, UnsupportedOperation):
        try:
            fileobj.seek(0, 2)
            self.filesize = fileobj.tell()
            fileobj.seek(0)
        except:
            raise ValueError("Could not determine filesize")
```

However, the latest version of `poster` installable with `pip` is still `0.8.1`.
