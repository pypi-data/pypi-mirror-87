# wic
winIDEA Command Line Interface

# Installation
isystem.connect is only available for manual installation for Windows.
The library must be downloaded and installed into your Python 3.8 directory.
https://www.isystem.com/downloads/isystem-connect-sdk.html

`pip install wic`

# Usage

### Manage download files
Add ELF without loading code  
`wic files add -f <path-to-elf> --no-code`

Add s19 without loading symbols  
`wic files add -f <path-to-s19> --no-symbols`

List downoad files  
`wic files list`

Clear download list  
`wic files clear`

### Manage static options
Get a value  
`wic options get -o <option-name>`

Set a value  
`wic options set -o <option-name> -v <value>`

Add a new entry in a list  
`wic options add -o <option-list>`

Clear option list  
`wic options clear -o <option-list>`

### Manage Workspace
`wic ws save`  
`wic ws close`

### Actions
Downloads the files to target  
`wic download` 

# Changelog
## v0.1
- Initial version with basic features