# Throwaway Key Project
### Super simple encryption keys for your project
---

The Throwaway Key Project is designed to solve the problem of having people crack your encryption methods.
For example, let's say you encrypt your data using a password. What's the problem? If someone cracks your code, they have the password you used, so if you used it on any other data it becomes easily accessible.

That's where this project comes in.

This module will create "throwaway keys" that you can use to encrypt your data that are:

**a) hard to crack** and **b) easy to fix if it does get cracked**

Meaning, if your throwaway key is cracked, you can regenerate one with the same strength in around a minute.

Since I haven't figured out how to make it a complete CLI yet, the basic syntax is as follows:
```
python3 -m throwaway_keys [options]
```

Some are of available options include: `rounds`, `use`, and `length` (only available for certain hashing algorithms).
For the round parameter, use it as so: `--rounds=<int>`.
For length, it's  the same thing: `--length=<int>`.

For the `use` parameter, it's a little more complicated:
`--use-<hash_method>`
The available hashing methods are:
  - `sha1`, `sha256`, `sha384`, and `sha512`
  - `shake128`, and `shake256`
  - `sha3-224`, `sha3-256`, `sha3-384`, and `sha3-512`
  - `blake2b`, and `blake2s`
  - `md5` is also available

Please note this list may not be updated every push.


## Installation
To install the latest version, it is recommended to use `python3 -m pip install throwaway-keys`.

You can also install directly from source using git:
```
git clone https://github.com/ii-Python/throwaway-keys.git && cd throwaway-keys
python3 setup.py install
```

## License
The Throwaway Keys Project is licensed under the MIT License, more information is in `LICENSE`.
