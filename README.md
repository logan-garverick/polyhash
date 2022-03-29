# PolyHash

## Description
An x86-64 binary analyzer for ELF and PE file types used to generate a list of hot-swappable bytes used to alter the signature of a file without affecting execution.
## Installation
To build a single binary file of the Polyhash tool using PyInstaller, follow these steps:
1. Clone the repository.
   ```
   git clone https://github.com/logan-garverick/polyhash.git
   ```
2. Ensure that your system is up-to-date.
   ```
   sudo apt-get -y update && sudo apt-get -y upgrade
   ```
3. Install Python3 package installer (pip).
   ```
   sudo apt install python3-pip
   ```
4. Install PyInstaller.
   ```
   sudo pip3 install --upgrade --no-deps --force-reinstall pyinstaller
   ```
5. Run the `build.sh` bash script.
   ```
   ./build.sh
   ```
6. The `polyhash` binary is now found in the parent directory of the project folder.

## Example
To demonstrate the functionality of the tool example files have been provided in the `examples` subfolder.  From the command line simply execute:
```
./polyhash -v examples/hello_<desired file format>
```