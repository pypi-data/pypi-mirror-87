# Python password vault.

Python password vault to keep track of password either locally or centralized in your own cloud.
As this is a hobby project I cannot guarantee any functionality or that no data loss will occur, but as I use it personally I will do my best to avoid it.
Currently development is done on Python 3.9 and the client runs on Win10 while the cloud is run on Raspbian on a Raspberry Pi 2.

**Prerequisites**
- cryptography
- paramiko
- pillow

**Setup**
- Install prerequisites
- Clone repo or pip install acid_vault
- Run VaultGui.pyw (For GUI)
- Setup your vault in file menu (Only necessary for Cloud and/or Steganography)
  - Setup SSH for cloud (For remote storage of vault)
    - Host - URL to host
    - Port - Port to use on host
    - Username - Username to login with at host
    - Password - Password to login with at host, will not be saved and has to be entered each time program is started. Recomended usage is through key exchange, see below
  - Setup Steganography (For hiding the vault in an image)
    - File location - path to vault storage E.g. images/picture.png
    - Original file - path to local file with the original png picture to compare against (Important that its a png and not jpeg as jpeg compression is not stable)
- Check [Steganography](https://en.wikipedia.org/wiki/Steganography) (If Steganography is to be used)
- Chose Local/Remote (Where to store vault)

**Basic usage**
- Add passwords by pressing "Add Password" button.
- Chose a password in password box.
- Press Save passwords to save passwords in vault.
- Press Load passwords to load passwords into vault (Will clear any unsaved data).
- Lock/Unlock - Will lock/unlock the data kept by program while its running to avoid overhead of getting data from the cloud.

If vault detect that the user has not used the UI for 5 minutes it will lock itself.

The file menu has options to save/load backups both as encrypted and unencrypted locally where the user chose.
