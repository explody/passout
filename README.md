passout -- keep credentials out of code
====================================

This is a very simple utility to help keep credentials out of other small scripts.

This data this utility exposes is intended to be read-only. It does not create files or write YAML for you, you must set up the directory and files yourself.

It expects file/directory structure thusly:

`~/.passout/<service>.yml` e.g. `~/.passout/okta.yml`

With a contents such as:

    development:
        username: username
        password: credentials
        somethingelse: other
    production:
        username: produser
        password: etc

Where the toplevel keys, 'development' and 'production' are the "environments".

passout only supports one user entry per environment (dev/test, etc.) though, the environment names are arbitrary so
one could easily have numerous envs like 'prod1','prod2' and so on.

For the most part, this is a light structure with a thin layer over the YAML. It's intended for user credentials but you
can stick any string data in the yaml files, as long as it doesn't go beyond the structure noted above.

There are a few predefined properties:

* username - returns yaml[environment]['username'] (read-only)
* password - returns yaml[environment]['password'] (read-only)
* env - returns the environment name, or if assigned a value, sets the environment name 
and triggers a load of the corresponding yaml section
* svc - returns the service name, or if set, loads the specified service file

There are only a few methods:

* get(key) - returns yaml[environment][key]
* setenv(env) - set the environment name a triggers a load of the corresponding yaml section
* setsvc(svc) - switch apps and load the corresponding yaml file

It works like this:

```python
import passout

po = passout.PassOut('okta','production')
login_to_something(username=po.username, password=po.password)
some_other_value = po.get('custom')

# perhaps we've performed tests in a dev env and now can switch to prod
po.env = 'production'
login_to_other_env(username=po.username, password=po.password)
```

Service and environment names may also be passed as environment variables

* PASSOUT_SVC - service name
* PASSOUT_ENV - environment name
* PASSOUT_PATH - directory path to the passout YAML files (default: ~/.passout)

```shell script
# export PASSOUT_SVC='myservice'
# export PASSOUT_ENV='development'
# export PASSOUT_PATH='/alternate/path/to/files'
```

```python
import passout

# no explicit arguments, as they come from the shell environment
po = passout.PassOut()
po.svc  # "myservice"
po.env  # 'development'

```