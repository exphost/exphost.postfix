import re
from connector import connector

def install_nc(host):
    host.ansible(
      "command",
      "yum install -y nc",
      become=True,
      check=False,
    )

def test_test_resolve(host):
    test = host.addr("test.some.example.domain.xyz")
    assert test.is_resolvable

def test_postfix_hello_text(host):
    install_nc(host)
    assert "250 test-0.localdomain" in host.check_output("""sh -c 'echo -e "helo ja\nquit\n"|{connector}'""".format(connector=connector))

def test_postfix_not_open_relay(host):
    install_nc(host)
    assert "Relay access denied" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: test@exphost.pl\nquit\n" | {connector}""".format(connector=connector))

def test_postfix_local_email_delivery(host):
    install_nc(host)
    assert "queued as" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: krzys@domena1.ru\nDATA\nhejo\n.\nquit\n" | {connector}""".format(connector=connector))

def test_postfix_local_email_delivery_nonexistance_account(host):
    install_nc(host)
    assert "User unknow" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: kasia@domena2.ru\nquit\n" | {connector}""".format(connector=connector))

def test_postfix_alias_delivery(host):
    install_nc(host)
    assert "queued as" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: krzysiek@domena1.ru\nDATA\nhejo\n.\nquit\n" | {connector}""".format(connector=connector))

def test_postfix_catch_all_alias_delivery(host):
    install_nc(host)
    assert "queued as" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: catch-all-random@domena1.ru\nDATA\nhejo\n.\nquit\n" | {connector}""".format(connector=connector))

def test_postfix_auth(host):
    install_nc(host)
    assert "Authentication successful" in host.check_output("""echo -e "ehlo ja\nAUTH LOGIN\na3J6eXNAZG9tZW5hMS5ydQ==\na3J6eXNwYXNz\nquit\n\n" | {connector}""".format(connector=connector))

def test_postfix_auth_invalid_pass(host):
    install_nc(host)
    assert "authentication failed" in host.check_output("""echo -e "ehlo ja\nAUTH LOGIN\na3J6eXNAZG9tZW5hMS5ydQ==\na3J6eXNwYXNzMg==\nquit\n\n" | {connector}""".format(connector=connector))

def test_postfix_send_email(host):
    install_nc(host)
    assert "queued as" in host.check_output("""echo -e "ehlo ja\nAUTH LOGIN\na3J6eXNAZG9tZW5hMS5ydQ==\na3J6eXNwYXNz\nMAIL FROM: krzys@domena1.ru\nRCPT TO: basia@client.some.example.domain.xyz\nDATA\nhejo\n.\nquit\n\n" | {connector}""".format(connector=connector))

#def test_postfix_send_email_different_mail_from(host):
#    install_nc(host)
#    assert "Sender address rejected" in host.check_output("""echo -e "ehlo ja\nAUTH LOGIN\na3J6eXNAZG9tZW5hMS5ydQ==\na3J6eXNwYXNz\nMAIL FROM: bartek@domena1.ru\nRCPT TO: basia@client.some.example.domain.xyz\nDATA\nhejo\n.\nquit\n\n" | nc test.some.example.domain.xyz 25""")
#
#def test_postfix_send_email_different_mail_from_but_allowed(host):
#    install_nc(host)
#    assert "queued as" in host.check_output("""echo -e "ehlo ja\nAUTH LOGIN\na3J6eXNAZG9tZW5hMS5ydQ==\na3J6eXNwYXNz\nMAIL FROM: sales@domena1.ru\nRCPT TO: basia@client.some.example.domain.xyz\nDATA\nhejo\n.\nquit\n\n" | nc test.some.example.domain.xyz 25""")

#def test_postfix_send_email_auth(host):
#    # Install another postfix on client vm
#    # add domain to named
#    # check email delivery on client vm
#    assert False
