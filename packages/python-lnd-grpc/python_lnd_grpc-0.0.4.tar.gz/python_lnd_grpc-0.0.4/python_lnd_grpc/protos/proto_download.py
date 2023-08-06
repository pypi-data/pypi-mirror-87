import python_lnd_grpc 
import os
import requests
import subprocess
import sys

SERVICES = {
    "autopilot": "autopilotrpc/autopilot.proto",
    "chainnotifier": "chainrpc/chainnotifier.proto", 
    "invoices": "invoicesrpc/invoices.proto",
    "lncli": "lnclipb/lncli.proto",
    "rpc": "rpc.proto",
    "signer": "signrpc/signer.proto",
    "versioner": "verrpc/verrpc.proto",
    "walletkit": "walletrpc/walletkit.proto",
    "walletunlocker": "walletunlocker.proto",
    "watchtower": "watchtowerrpc/watchtower.proto",
    "wtclient": "wtclientrpc/wtclient.proto"
}
URL = "https://raw.githubusercontent.com/lightningnetwork/lnd/v"
CWD = os.getcwd()
PROTOS = []

def get_version(obj):
    info = obj.get_info()
    version = info.version.split()
    return version[0]

obj = python_lnd_grpc.LNDMethods(network="mainnet")
version = get_version(obj)
version = "0.11.1-beta"

# download protos
for service in SERVICES:
    final_url = URL + version + "/lnrpc/{}".format(SERVICES[service])
    print(final_url)
    try:
        proto = requests.get(final_url)
    except Exception as e:
        print(e)
        sys.exit()

    f = CWD + "/" + service + ".proto"
    proto_file = open(f, "w")
    proto_file.write(proto.text)
    proto_file.close
    PROTOS.append(service + ".proto")

# generate metaclass:
for proto in PROTOS:
    command = "python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. " + proto
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

# TODO: change line 5 i n rpc_pb2_grpc:
# from python_lnd_grpc.protos import rpc_pb2 as rpc__pb2

# walletunlocker_pb2.py change 
# import rpc_pb2 as rpc__pb2
# to
# from python_lnd_grpc.protos import rpc_pb2 as rpc__pb2


# walletunlocker_pb2_grpc change
# import walletunlocker_pb2 as walletunlocker__pb2
# to
# from python_lnd_grpc.protos import walletunlocker_pb2 as walletunlocker__pb2

