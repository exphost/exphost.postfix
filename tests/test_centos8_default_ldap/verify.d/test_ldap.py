from test_postfix import check_mail_existance
connector_installed = False
def install_connector(host):
    global connector_installed
    if connector_installed:
        return
    setup_connector(host)
    connector_installed = True
def test_postfix_ldap_local_email_delivery(host):
    install_connector(host)
    resp = host.check_output("""echo -e "helo ja\nMAIL FROM: test@exphost.pl\nRCPT TO: mariola@domena6.ru\nDATA\nhejo\n.\nquit\n" | nc localhost 25""")
    assert "queued as" in resp
    mail_id = resp.split()[-4] #Hardcoded message id
    check_mail_existance(host, "/var/lib/vmail/domena6.ru/mariola/", mail_id)

