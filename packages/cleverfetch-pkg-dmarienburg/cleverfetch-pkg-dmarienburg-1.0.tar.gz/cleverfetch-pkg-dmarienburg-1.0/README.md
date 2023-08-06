# CleverFetch

A simple script for automating your downloads of data from the Clever sftp site.

Author: David Marienburg  
Version: 1.0  
Last Update: 2020-12-03

***

## Requirements

* Paramiko - [https://pypi.org/project/paramiko/](https://pypi.org/project/paramiko/)

***

## Usage

Using the script is simple, just import the `get_files` method, passing it a username and a password.

```python
>>> from CleverFetch import get_files
>>> get_files(username="ThisisanSFTPUsername", password="ThisIsAnSFTPPassword")
```

The program will then automatically download any files that you don't already have into the scripts Data folder

CleverFetch will then return a list of the new files downloaded, as file paths, Data that can be used by any secondary scripts like a database loader.

Since storing passwords in plain text is unsafe, it would be best practice to run this script from a commandline using python's getpass library.  This will prompt the user to enter their password when the script runs and the password they type will not be visible in the command line.

```python
>>> from CleverFetch import get_files
>>> from getpass import getpass
>>> get_files(username="ThisIsanSFTPUsername", password=getpass("Password: "))
```

If you want the downloaded .csv files to be saved in a specific folder simply provide this files complete filepath to the save_path parameter.  If you do not provide a path the files will be saved in the CleverFetch library's on folder structure.

```python
>>> from CleverFetch import get_files
>>> from getpass import getpass
>>> get_files(username="ThisIsanSFTPUsername", password="ThisIsAnSFTPPassword", save_path=r"C:\\users\me\desktop")
```
