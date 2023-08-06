import io
import os


class Service:
    __bucket_class__ = None

    requires_location = True

    def __init__(self, id, default_location=None):
        self.id = id
        self.default_location = default_location

    def __str__(self):
        return "{}://".format(self.id)

    def bucket(self, name, location=None):
        if self.requires_location and (location is None and self.default_location is None):
            raise Exception("No location or default location set!")

        if self.__bucket_class__ is None:
            raise Exception("No __bucket_class__ was set for {}".format(self))

        return self.__bucket_class__(self, name, location or self.default_location)

    def __eq__(self, other):
        if not isinstance(other, Service):
            return False

        return self.id == other.id


class Bucket:
    def __init__(self, service: Service, name: str, location: str):
        self.service = service
        self.name = name
        self.location = location

    def __repr__(self):
        return f'<{self.__class__.__name__} {str(self)}>'

    def __str__(self):
        return "{}{}/{}".format(self.service, self.location, self.name)

    def cubby(self, name):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def create(self):
        raise NotImplementedError()

    def list(self, prefix=None, max_keys=None):
        raise NotImplementedError()


class Cubby:
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

    def __repr__(self):
        return f'<{self.__class__.__name__} {str(self)}>'

    def __str__(self):
        return "{}/{}".format(self.bucket, self.key)

    def retrieve(self, filepath=None, file=None):
        if filepath is not None:
            if os.path.isdir(filepath):
                filepath = os.path.join(filepath, self.key)

            with open(filepath, 'wb') as file:
                return self.retrieve_filelike(file)
        elif file is not None:
            return self.retrieve_filelike(file)
        else:
            buffer = io.BytesIO()
            self.retrieve_filelike(buffer)
            buffer.seek(0)
            return buffer.read()

    def retrieve_filelike(self, file):
        raise NotImplementedError()

    def store(self, filepath=None, file=None, string=None, bytes=None, encoding='utf-8'):
        if filepath is not None:
            with open(filepath, 'rb') as file:
                return self.store_filelike(file)
        elif file is not None:
            self.store_filelike(file)
        elif string is not None:
            self.store_filelike(io.BytesIO(string.encode(encoding)))
        elif bytes is not None:
            self.store_filelike(io.BytesIO(bytes))
        else:
            raise Exception("One of [filepath, file, string, bytes] must be specified.")

        return self

    def store_filelike(self, filelike):
        raise NotImplementedError()

    DefaultUrlExpiration = None

    def url(self, expiration=DefaultUrlExpiration):
        raise NotImplementedError()

    def filesize(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def exists(self):
        raise NotImplementedError()

    def copy_to_native_cubby(self, cubby=None):
        """Copies from a Cubby of this type to another cubby of this type."""
        raise NotImplementedError()

    def copy_to(self, key=None, cubby=None):
        if key:
            cubby = self.bucket.cubby(key)

        if isinstance(cubby, self.__class__):
            self.copy_to_native_cubby(cubby)
            return cubby

        cubby.store_filelike(self.retrieve_filelike())
        return cubby

    def move_to(self, key=None, cubby=None):
        copy = self.copy_to(key=key, cubby=cubby)
        self.delete()
        return copy

    @property
    def extension(self):
        return os.path.splitext(self.key)[1]

    @property
    def service(self):
        return self.bucket.service
