import os, io, uuid, time, socket
import paramiko
import redis


class SaveLocalPipeline:
    """
    Saves the request body in a local file and updates the item
    with the path to the saved file.
    """

    def __init__(self):
        self.dir = os.environ.get("RESPONSE_DIR")

    # Create the output directory if it doesn't already exist
    def open_spider(self, spider):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    # Write the file to the specified location
    # The filename should be a combination of the current timestamp and a uuid
    def process_item(self, item, spider):
        filename = f"{str(time.time_ns())}-{str(uuid.uuid4())}"

        with open(os.path.join(self.dir, filename), "wb+") as f:
            f.write(item['response'].body)

        item["file"] = filename
        return item


class SFTPPipeline:
    """
    Uploads the response body to a file server. The file's
    location is saved on the item. Uses the filename pattern
    {timestamp}-{uuid}.
    Uses private key authentication.
    """

    def __init__(self):
        self.host = "192.168.1.103"  # os.environ.get("SFTP_HOST")
        self.port = 22  # os.environ.get("SFTP_PORT")
        self.dir = f"/data/scrape/{socket.gethostname()}/{time.time_ns()}"  # os.environ.get("RESPONSE_DIR")
        self.username = "scrapeuser"  # os.environ.get("SFTP_USERNAME")
        self.keyfile = "/Users/davidwiles/.ssh/scrapeuser"  # os.environ.get("SFTP_KEYFILE")
        self.client = None

    def open_spider(self, spider):
        self._connect()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        filename = str(uuid.uuid4())

        # Create bytes buffer to use as file to upload
        with io.BytesIO(item['response'].body) as f:
            self.client.putfo(f, filename)

        item['file'] = os.path.join(self.host, self.dir, filename)
        return item

    def _connect(self):
        # Connect to the server and store the connection
        tr = paramiko.Transport((self.host, self.port))
        with open(self.keyfile, "r") as key:
            pk = paramiko.Ed25519Key.from_private_key(key)
            tr.connect(username=self.username, pkey=pk)
            self.client = paramiko.SFTPClient.from_transport(tr)
        # Make sure that the directory exists
        self._mkdirs()
        # Move to the desired directory
        self.client.chdir(self.dir)

    def _mkdirs(self):
        # Create all directories used by this spider
        dirs = os.path.split(self.dir)
        tmp = ""
        for p in dirs:
            tmp += "/" + p
            try:
                self.client.lstat(tmp)
            except IOError:
                self.client.mkdir(tmp)


class RedisPipeline:
    """
    Saves the response in Redis, using the url as the key and
    the json-stringified item as the value. The key will be queried to
    ensure that duplicate urls are not downloaded.
    """

    def __init__(self):
        pass

    def open_spider(self, spider):
        # Open connection pool
        pass

    def close_spider(self, spider):
        # Close connection
        pass

    def process_item(self, item, spider):
        # Store item in redis
        pass
