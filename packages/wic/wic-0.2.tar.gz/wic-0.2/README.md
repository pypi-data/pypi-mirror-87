# wic
winIDEA Command Line Interface

# Installation
isystem.connect is only available for manual installation for Windows.
The library must be downloaded and installed into your Python 3.8 directory.
https://www.isystem.com/downloads/isystem-connect-sdk.html

`pip install wic`

# Usage
```
Usage: wic [OPTIONS] COMMAND [ARGS]...

  Command line interface for winIDEA

Options:
  -ws, --workspace FILENAME  Path to winIDEA workspace
  -id TEXT                   Connect to winIDEA instance ID
  --version                  Show the version and exit.
  -h, --help                 Show this message and exit.

Commands:
  download  Download files to target
  files     Manage download files
  list      List winIDEA instances
  options   Manage options
  start     Start winIDEA
  ws        Manage workspace
```


### Manage download files
```
Add ELF without loading code  
$ wic files add -f <path-to-elf> --no-code

Add s19 without loading symbols  
$ wic files add -f <path-to-s19> --no-symbols

List downoad files  
$ wic files list

Clear download list  
$ wic files clear
```

### Manage static options
```
Get a value  
$ wic options get -o <option-name>

Set a value  
$ wic options set -o <option-name> -v <value>

Add a new entry in a list  
$ wic options add -o <option-list>

Clear option list  
$ wic options clear -o <option-list>
```

### Manage Workspace
```
$ wic ws save
$ wic ws close
```

### Actions
```
Download the files to target  
$ wic download

If only one workspace is always used workspace or ID is not needed
This starts the most recent workspace used
$ wic start

Start winIDEA instance and provide an ID  
$ wic -ws <workspace-path> -id <custom-ID> start

Now the ID can be used for new connections
$ wic -id <custom-ID> files list

List all winIDEA instances  
$ wic list


# Changelog
## v0.2
- Add instance Id support
- List instances

## v0.1
- Initial version with basic features