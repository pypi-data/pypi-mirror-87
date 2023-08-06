# safeIO  

>  Safely make I/O operations to files in Python even from multiple threads... and more!  

# Table of Content  

1. [safeIO](#safeio)
2. [Table of Content](#table-of-content)
3. [What is it?](#what-is-it)
4. [Installation](#installation)
5. [Objects](#objects)
    - [TextFile()](#textfile)
        - [isfile](#isfile)
        - [delete](#delete)
        - [rename](#rename)
        - [move](#move)
        - [name](#name)
        - [fileno](#fileno)
        - [read](#read)
        - [write](#write)
        - [append](#append)
        - [readline](#readline)
        - [readlines](#readlines)
        - [writelines](#writelines)
        - [appendlines](#appendlines)
        - [detach](#detach)
    - [BinaryFile()](#binaryfile)
        - [isfile](#isfile-1)
        - [delete](#delete-1)
        - [rename](#rename-1)
        - [move](#move-1)
        - [name](#name-1)
        - [fileno](#fileno-1)
        - [read](#read-1)
        - [write](#write-1)
        - [append](#append-1)
        - [readline](#readline-1)
        - [readlines](#readlines-1)
        - [writelines](#writelines-1)
        - [appendlines](#appendlines-1)
        - [detach](#detach-1)
    - [JSONFile()](#jsonfile)
        - [isfile](#isfile-1-2)
        - [delete](#delete-1-2)
        - [rename](#rename-1-2)
        - [move](#move-1-2)
        - [name](#name-1-2)
        - [fileno](#fileno-1-2)
        - [read](#read-1-2)
        - [write](#write-1-2)
        - [append](#append-1-2)
        - [detach](#detach-1-2)


# What is it?
It's a module which lets you manage your files (most of the time, Input/Output operations) without worrying about accessing the file from two simultaneously.

Some functions may help you managing your files more easily as they are intuitive and things like substractions (TextFile object - TextFile Object returns the Cosine Similarity of the two files), equality (Object == Object), iteration (for line in TextFile object), the rename/move/delete methods are made easier!.

# Installation
**From PIP**
```sh
pip install safeIO --upgrade
```


# Objects
## TextFile()  

> A Text File object  


### isfile  

*isfile(callback=None)*  

> Wether the file exists on the disk or not  

### delete  

*delete(callback=None)*  

> Deletes the file  

### rename  

*rename(newName,overwrite=False,callback=None)*  

> Renames the file and returns its new path  

### move  

*move(newPath,overwrite=False,callback=None)*  

> Moves the file and returns its new path  

### name  

*name(callback=None)*  

> Returns the file name  

### fileno  

*fileno(callback=None)*  

> Returns the file descriptor (int) used by Python to request I/O operations from the operating system.  

### read  

*read(position=0,callback=None)*  

> Reads the entire file and returns its content  

### write  

*write(data,position=0,callback=None)*  

> Writes (or overwrites) to the file and returns the number of characters written  

### append  

*append(data,callback=None)*  

> Appends to the file and returns the number of characters written  

### readline  

*readline(position=0,callback=None)*  

> Returns the line of the current position (from the position to the linebreak)  

### readlines  

*readlines(position=0,callback=None)*  

> Reads the whole file and returns the lines (separated by a line break)  

### writelines  

*writelines(data,position=0,callback=None)*  

> Writes (or overwrites) the given list of lines to the file  

### appendlines  

*appendlines(data,callback=None)*  

> Appends the given list of lines to the file  

### detach  

*detach(mode="r",callback=None)*  

> Returns the opened IO (TextIOWrapper)  

>   

**Warning: Make sure to close the file correctly after using the file with detach**

---  

## BinaryFile()  

> A Binary File object  

### isfile  

*isfile(callback=None)*  

> Wether the file exists on the disk or not  

### delete  

*delete(callback=None)*  

> Deletes the file  

### rename  

*rename(newName,overwrite=False,callback=None)*  

> Renames the file and returns its new path  

### move  

*move(newPath,overwrite=False,callback=None)*  

> Moves the file and returns its new path  

### name  

*name(callback=None)*  

> Returns the file name  

### fileno  

*fileno(callback=None)*  

> Returns the file descriptor (int) used by Python to request I/O operations from the operating system.  

### read  

*read(position=0,callback=None)*  

> Reads the entire file and returns its content  

### write  

*write(data,position=0,callback=None)*  

> Writes (or overwrites) to the file and returns the number of bytes written  

### append  

*append(data,callback=None)*  

> Appends to the file and returns the number of bytes written  

### readline  

*readline(position=0,callback=None)*  

> Returns the line of the current position (from the position to the linebreak)  

### readlines  

*readlines(position=0,callback=None)*  

> Reads the whole file and returns the lines (separated by a line break)  

### writelines  

*writelines(data,position=0,callback=None)*  

> Writes (or overwrites) the given list of lines to the file  

### appendlines  

*appendlines(data,callback=None)*  

> Appends the given list of lines to the file  

### detach  

*detach(mode="rb",callback=None)*  

> Returns the opened IO (TextIOWrapper)  

>   

> Tips: Make sure to include the "b" access mode in the mode\n  

**Warning: Make sure to close the file correctly after using the file with detach**

---  

## JSONFile()  

> A JSON File object  

### isfile  

*isfile(callback=None)*  

> Wether the file exists on the disk or not  

### delete  

*delete(callback=None)*  

> Deletes the file  

### rename  

*rename(newName,overwrite=False,callback=None)*  

> Renames the file and returns its new path  

### move  

*move(newPath,overwrite=False,callback=None)*  

> Moves the file and returns its new path  

### name  

*name(callback=None)*  

> Returns the file name  

### fileno  

*fileno(callback=None)*  

> Returns the file descriptor (int) used by Python to request I/O operations from the operating system.  

### read  

*read(position=0,callback=None)*  

> Reads the entire file and returns its content  

### write  

*write(data,position=0,callback=None)*  

> Writes (or overwrites) to the file and returns the number of characters written  

### append  

*append(data,callback=None)*  

> Appends to the file and returns the number of characters written  

### detach  

*detach(mode="r",callback=None)*  

> Returns the opened IO (TextIOWrapper)  

**Warning: Make sure to close the file correctly after using the file with detach**

Markdown File | 325 lines