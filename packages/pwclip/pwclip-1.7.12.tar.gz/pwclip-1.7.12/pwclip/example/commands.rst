Usage
-----

    Although is was planed as GUI-Program it's also possible to be executed from
    terminals. For Windows, Linux and OSX there is an appropriate executable
    packed which might be executed like the following examples will show:

    **-GPG-Mode-**

    If there is an environment variable called GPGKEYS it will use those keys to
    encrypt on changes to the password file. To list the password file you may use
    the list switch followed by optional search pattern like:

    ``pwcli -l``

    or

    ``pwcli -l $PATTERN``

    as you can see the yaml format tends to be used for multiple user names to
    better manage large lists. By default the current users entrys will be listed
    only. To have them all listed (or searched for by the above pattern example)
    use:

    ``pwcli -A -l $PATTERN``

    To one-shot convert a key/cert pair in openssl x509 format, read passwords from
    passwords.yaml and list them:

    ``pwcli -Y passwords.yaml --cert ssl.crt --key ssl.key --ca-cert ca.crt -l``

    **-Yubikey-Mode-**

    The YKSERIAL environment variable is used if found to select the yubikey to use
    if more than one key is connected. Otherwise the first one found is chosen.
    Likewise it also accepts an option:

    ``pwcli -y $YKSERIAL``

    To have it wait for a specific time like 60 seconds (bevore resetting the paste
    buffer to the previously copied value) the PWCLIPTIME environment variable is
    used or also the command accepts it as input:

    ``pwcli -t 60 -l somename``

    Most of the options may be combined. For more information on possible options in
    cli mode please see:

    ``pwcli --help``

    **-GUI-Modes-**

    For the GUI-Mode just use one of the following commands, also accepting most of
    the commandline arguments:

    ``pwclip``

    ``ykclip``

