brightsign-kiddie-pool
======================

A utility for analyzing brightsign presentation `pool` folders

# Usage
`python3 brightsign-kiddie-pool.py <brightsign_presentation_folder>`

Files in `<brightsign_presentation_folder>/pool/<lots of sha1 hashes>` are moved to `<brightsign_presentation_folder>/kiddie_pool/<original-file-name>`

# Purpose
Brightsign Presentations are organized as a directory. The most important components are `local-sync.xml`, which is a manifest of all the files included in the presentation, and a directory called `pool/`, which is are all the files necessary for that presentation. `pool/` 
