

## Install python package locally from pypi:

    import python_lnd_grpc

 
## Initiate the connector class

    lightning = python_lnd_grpc.LNDMethods()
    walletunlocker = python_lnd_grpc.WalletUnlocker()

## Use methods

    info = lightning.get_info()
    print(info)

## Custom connector object

User can modify connector object in cases when connection to remote lnd node is needed (instead of local one), specifying custom parameters, like paths and file names:

    lightning = python_lnd_grpc.LNDMethods(
        tls_file_path = "~/.lnd/",
        tls_file_name = "remote.cert",
        macaroon_filename = "remote.macaroon",
        macaroon_path = "~/.lnd/data/chain/bitcoin/",
        grpc_host = "192.168.0.199",
        grpc_port = "10009",
        network = "mainnet",
    )
In case of connecting to remote lnd node, the grpc setting in `lnd.conf` has to be set to listening:

    rpclisten=0.0.0.0:10009
