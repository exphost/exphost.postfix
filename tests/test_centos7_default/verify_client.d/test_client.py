import re

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
    re_postfix_hello = re.compile("220 test-0.* ESMTP Postfix.*")
    output = host.check_output("""sh -c 'echo -e "quit\n"|nc test.some.example.domain.xyz 25'""")
    assert re_postfix_hello.match(output.split("\n")[0])

def test_postfix_not_open_relay(host):
    install_nc(host)          
    assert "Relay access denied" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: test@exphost.pl\nquit\n" | nc test.some.example.domain.xyz 25""")

def test_postfix_local_email_delivery(host):
    install_nc(host)          
    assert "queued as" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: krzys@domena1.ru\nDATA\nhejo\n.\nquit\n" | nc test.some.example.domain.xyz 25""")

def test_postfix_local_email_delivery_nonexistance_account(host):
    install_nc(host)          
    assert "User unknow" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: kasia@domena2.ru\nquit\n" | nc test.some.example.domain.xyz 25""")

def test_postfix_alias_delivery(host):
    install_nc(host)          
    assert "queued as" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: krzysiek@domena1.ru\nDATA\nhejo\n.\nquit\n" | nc test.some.example.domain.xyz 25""")

def test_postfix_catch_all_alias_delivery(host):
    install_nc(host)          
    assert "queued as" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: catch-all-random@domena1.ru\nDATA\nhejo\n.\nquit\n" | nc test.some.example.domain.xyz 25""")

#def test_postfix_send_email_auth(host):
#    # Install another postfix on client vm
#    # add domain to named
#    # check email delivery on client vm
#    assert False