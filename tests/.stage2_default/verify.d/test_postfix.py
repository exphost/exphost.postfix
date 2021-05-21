import re
def install_nc(host):
    host.ansible(
      "command",
      "yum install -y nc",
      become=True,
      check=False,
    )

def test_postfix_running(host):
  assert host.service("postfix").is_running

def test_postfix_hello_text(host):
    install_nc(host)
    re_postfix_hello = re.compile("220 test-0.* ESMTP Postfix.*")
    output = host.check_output("""sh -c 'echo -e "quit\n"|nc localhost 25'""")
    assert re_postfix_hello.match(output.split("\n")[0])

def test_postfix_local_email_delivery(host):
    install_nc(host)
    resp = host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: krzys@domena1.ru\nDATA\nhejo\n.\nquit\n" | nc localhost 25""")
    assert "queued as" in resp
    mail_id = resp.split()[-1]
    assert host.run("""grep "with SMTP id {}$" /var/lib/vmail/domena1.ru/krzys/ -r -q""".format(mail_id))


def test_postfix_vmail_dir_permissions(host):
    f = host.file("/var/lib/vmail")
    assert f.mode == 0o700
    assert f.user == "postfix"

def test_postfix_alias_delivery(host):
    install_nc(host)
    resp = host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: krzysiek@domena1.ru\nDATA\nhejo\n.\nquit\n" | nc localhost 25""")
    assert "queued as" in resp
    mail_id = resp.split()[-1]
    assert host.run("""grep "with SMTP id {}$" /var/lib/vmail/domena1.ru/krzys/ -r -q""".format(mail_id))

def test_postfix_catch_all_alias_delivery(host):
    install_nc(host)
    resp = host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: catch-all-random@domena1.ru\nDATA\nhejo\n.\nquit\n" | nc localhost 25""")
    assert "queued as" in resp
    mail_id = resp.split()[-1]
    assert host.run("""grep "with SMTP id {}$" /var/lib/vmail/domena1.ru/bartek/ -r -q""".format(mail_id))


#def test_local_email_send(host):
#    assert False
#
def test_postfix_local_email_delivery_nonexistance_account(host):
    install_nc(host)          
    assert "User unknow" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: kasia@domena2.ru\nquit\n" | nc localhost 25""")
