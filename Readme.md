passout -- keep credentials out of code
====================================

This is a very very simple utility package to help keep credentials out of other small scripts.

It uses YAML and expects file/directories thusly:

~/.passout/`<service>`.yml

With a contents such as:

    development:
        user: username
        pass: credentials
        somethingelse: other
    production:
        user: produser
        pass: etc

Where the toplevel keys, 'development' and 'production' are the "environments".

passout only supports one user entry per environment (dev/test, etc.) though, the environment names are arbitrary so
one could easily have numerous envs like 'prod1','prod2' and so on.

For the most part, this is a light structure with a thin layer over YAML. It's intended for user credentials but you
can stick any string data in the yaml files, as long as it doesn't go beyond the structure noted above.

There are basically four methods:

* get(key) - returns yaml[environment][key]
* user() - returns yaml[environment]['user']
* creds() - returns yaml[environment]['pass']
* setenv(env) - set the environment name a triggers a load of the corresponding yaml

It works like this:


    import passout

    po = passout.PassOut('okta','production)
    user = po.user()
    creds = po.creds()
    something_els = po.get('custom')

    # perhaps we've performed tests in a dev env and now can switch to prod
    po.setenv('production')
    user = po.user()
    creds = po.creds()

