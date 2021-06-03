import re
import time
from connector import connector, setup_connector
connector_installed = False
def install_connector(host):
    global connector_installed
    if connector_installed:
        return
    setup_connector(host)
    connector_installed = True

def check_mail_existance(host, path, msg_id):
    delivered = False
    retries = 10
    while not delivered:
        retries -= 1
        try:
            assert host.ansible(
              "command",
              """grep "with SMTP id {}$" {} -r -q""".format(msg_id, path),
              become=True,
              check=False,
            )['rc'] == 0
            delivered = True
        except:
            if retries < 0:
                raise
            time.sleep(1)

def test_postfix_running(host):
  assert host.service("postfix").is_running

def test_postfix_hello_text(host):
    install_connector(host)
    re_postfix_hello = re.compile("220 test-0.* ESMTP Postfix.*")
    output = host.check_output("""sh -c 'echo -e "quit\n"|nc localhost 25'""")
    assert re_postfix_hello.match(output.split("\n")[0])

def test_postfix_local_email_delivery(host):
    install_connector(host)
    resp = host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: krzys@domena1.ru\nDATA\nhejo\n.\nquit\n" | nc localhost 25""")
    assert "queued as" in resp
    mail_id = resp.split()[-4] #Hardcoded message id
    check_mail_existance(host, "/var/lib/vmail/domena1.ru/krzys/", mail_id)

def test_postfix_vmail_dir_permissions(host):
    f = host.file("/var/lib/vmail")
    assert f.mode == 0o700
    assert f.user == "postfix"

def test_postfix_alias_delivery(host):
    install_connector(host)
    resp = host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: krzysiek@domena1.ru\nDATA\nhejo\n.\nquit\n" | nc localhost 25""")
    assert "queued as" in resp
    mail_id = resp.split()[-4]
    check_mail_existance(host, "/var/lib/vmail/domena1.ru/krzys/", mail_id)

def test_postfix_catch_all_alias_delivery(host):
    install_connector(host)
    resp = host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: catch-all-random@domena1.ru\nDATA\nhejo\n.\nquit\n" | nc localhost 25""")
    assert "queued as" in resp
    mail_id = resp.split()[-4]
    check_mail_existance(host, "/var/lib/vmail/domena1.ru/bartek/", mail_id)


#def test_local_email_send(host):
#    assert False
#
def test_postfix_local_email_delivery_nonexistance_account(host):
    install_connector(host)
    assert "User unknow" in host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: kasia@domena2.ru\nquit\n" | nc localhost 25""")
