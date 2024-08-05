import aria2p
from Helpers.getValue import RPC_PORT


def download(url, path):
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=RPC_PORT,
            secret=""
        )
    )
    event = aria2.add_uris([url], options={"dir": path})
    return event
