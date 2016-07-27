brightsign-kiddie-pool
======================

A utility for analyzing brightsign presentation `pool` folders :swimmer:

# Usage
`python3 brightsign-kiddie-pool.py <presentation_directory>`

Files in `<presentation_directory>/pool/<lots of sha1 hashes>` are moved to `<presentation_directory>/kiddie_pool/<original-file-name>`

# Purpose
Brightsign Presentations are organized as a directory. The most important components are `local-sync.xml`, which is a manifest of all the files included in the presentation, and a directory called `pool/`, which is are all the files necessary for that presentation.

# Known Issues
Only works for a `local-sync.xml` file, and not a `current-sync.xml` necessary for network mode.
