from connector import connector, setup_connector
connector_installed = False
def install_connector(host):
    global connector_installed
    if connector_installed:
        return
    setup_connector(host)
    connector_installed = True

def test_postfix_ldap_send_email(host):
    install_connector(host)
    assert "queued as" in host.check_output("""echo -e "ehlo ja\nAUTH LOGIN\nbWFyaW9sYUBkb21lbmE2LnJ1\nbWFyaW9sYXBhc3M=\nMAIL FROM: mariola@domena6.ru\nRCPT TO: basia@client.some.example.domain.xyz\nDATA\nhejo\n.\nquit\n\n" | {connector}""".format(connector=connector))

def test_postfix_ldap_local_email_delivery(host):
    install_connector(host)
    assert "queued as" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: mariola@domena6.ru\nDATA\nhejo\n.\nquit\n" | {connector}""".format(connector=connector))
