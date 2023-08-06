# CONFINI

Configuration parser that process all sections and values in all `ini` files in a directory.

## Usage

``` 
import confini

c = confini.Config('/path/to/config/dir')
c.process()

print(c.get('FOO_BAR_BAZ'))

```

### Value storage

The values are stored in a single key/value dictionary, with section and name separated by _underscore_ and all letters transformed to uppercase.

Consider this value in an ini section:

```
[foO]
bar_baz = 42
```

This will be stored in the `confini` store with `FOO_BAR_BAZ` as the key.

### Environment overrides

By default, the value of any environment variable matching a store key will overwrite the corresponding value in the store.

A prefix can be provided on instantiation to define a separate namespace for environment variable overrides:

```
>>> os.environ.set('FOO_BAZ_BAZ', 666)
>>> c = config.Config('/path/to/config/dir')
>>> c.process()
>>> print(c.get('FOO_BAR_BAZ'))
666
>>> c = config.Config('/path/to/config/dir', 'XXX')
>>> c.process()
>>> print(c.get('FOO_BAR_BAZ'))
42
>>> os.environ.set('XXX_FOO_BAZ_BAZ', 13)
>>> c = config.Config('/path/to/config/dir', 'XXX')
>>> c.process()
>>> print(c.get('FOO_BAR_BAZ'))
13
```

### Required values

Keys can be set as required, and after processing independently validated:

```
>>> c = config.Config('/path/to/config/dir')
>>> c.require('BAR_BAZ', 'FOO')
>>> c.process()
>>> c.validate()
True
>>> c = config.Config('/path/to/config/dir')
>>> c.require('BAR_BAZ_BAZ', 'FOO')
>>> c.process()
>>> c.validate()
False
```

### Censoring logs

The string representation of the confini object is a list of all stored values, one on each line.

Display of individual values can be suppressed:

```
>>> c = config.Config('/path/to/config/dir')
>>> c.process()
>>> print(c)
FOO_BAR_BAZ = 666
>>> c.censor('BAR_BAZ', 'FOO')
>>> print(c)
***
```

### Encryption

Values can be **GNUPG** encrypted by saving them in individual encrypted files providing the filename as value argument wrapped in a gpg directve:

```
[foo]
BAR_BAZ = !gpg(foo_bar_baz.asc)
```

Decryption mode is on by default, and can be deactivated on instantiation:

```
>>> c = config.Config('/path/to/config/dir')
>>> c.process()
>>> c.get()
666
>>> c = config.Config('/path/to/config/dir', decrypt=False)
>>> c.process()
>>> c.get()
!gpg(foo_bar_baz.asc)
```

The user keyring in the default location is used for decryption, which may be overridden as usual with the `GNUPGHOME` environment variable.


