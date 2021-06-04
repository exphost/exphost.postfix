connector = "nc localhost 25"
def setup_connector(host):
  host.ansible(
    "command",
    "yum install -y nc",
    become=True,
    check=False,
    )

