brightsign-lifeguard
======================

A set of tools for analyzing brightsign presentation `pool` folders :swimmer:

`lifeguard-out` is used for pulling all assets out of a sharded Brightsign presentation pool

`lifeguard-in` is used to repack a brightsign presentation pool and create a new `current-sync.xml`

# Usage
`python3 brightsign-kiddie-pool.py <presentation_directory>`

Files in `<presentation_directory>/pool/<lots of sha1 hashes>` are moved to `<presentation_directory>/kiddie_pool/<original-file-name>`

# Purpose
Brightsign Simple Network Presentations are organized across a series of directories. The most important components are `current-sync.xml`, which is a manifest of all the files included in the presentation, and a directory called `pool/`, which is are all the files necessary for that presentation are sharded.

However, the files in `pool/` are not readable by their normal filename. Instead, the original filename is kept within the `current-sync.xml` manifest, which then points to the location in the pool where the actual file is stored (named by the file's SHA-1 hash).

`lifeguard-out` reads the `current-sync.xml` file, then moves all files from `pool/` to a new folder `kiddie_pool`, where the files have their original file names.

`lifeguard-in` reads from a `kiddie-pool` directory and repacks the `pool`. It then adds all these files to the existing `current-sync.xml`, replacing all the previous files listed there. It uses the `baseURL` from `current-sync.xml` (URL where the presentation will be hosted) to set the URL for the repacked files. This allows you to reuse a presentation, but saved at a different location, using this utility.

# Known Issues
Only works for a `local-sync.xml` file, and not a `current-sync.xml` necessary for network mode.
