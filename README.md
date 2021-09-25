# Remove duplicates

## Remove safely and automatically duplicates files.

The workflow is:
- Launch fdupes which output a text file with a list of duplicates candidates
- Launch **hash_dupes** which does a hash of each file listed in the fdupes text file and then output the result in a CSV
- Launch **delete_dupes** which deletes all duplicates (except one) from the previous CSV file

## fdupes
[fdupes](https://github.com/adrianlopezroche/fdupes) is a separated, well-known, project

Example usage of fdupes, recursive mode. 

Runs in background (see active background tasks with `jobs`)
```
fdupes -r /my_folder &> /path/to/fdupes.txt &
```

*I know fdupes has a delete option but I like to check, cross-check and check again if gathered duplicates are really duplicates. 
This is why I've initially written theses little scripts. 
Before deleting I can simulate what will be deleted and check with file hashes.*


*I use theses scripts in conjuction of fdupes on my whole familly data. There are 8+ input sources (phone, pc, etc..) sync on a NAS and backed on a cloud storage.*


## hash_dupes
Take a list of files, then output CSV file with file & hash for each found file

### Options
```
	-i or --input, Input file (list of full file paths separated by line feed)

	-o or --output, Output CSV file full path

	-l or --log, Add --log=INFO or --log=DEBUG for logging details (default to sysout)
```

#### Basic
```
python hash_dupes.py -i /path/to/fdupes.txt -o csv_dupes.csv
```

#### Debug mode
```
python hash_dupes.py -i /path/to/fdupes.txt -o csv_dupes.csv --log=DEBUG
```


## delete_dupes

Delete all duplicates occurences (except one) from a CSV


CSV format needs to be /filepath/;hash <LF>

### Options
```
	"-i", "--input", Input CSV file

	"-s", "--simulate", Does nothing, just simulate actions

	"-c", "--check-hash", Should check the hash of the input file with the hash of the real file. The execution will be longer

	"-l", "--log", Set the log level. Add --log=INFO or --log=DEBUG for logging. The logging file will be in the same directory as delete_dupes.py and called delete_dupes.log.
```

### Usages

#### Basic
```
python delete_dupes.py -i /path/to/csv_dupes.csv
```

#### Simulation mode
```
python delete_dupes.py -i /path/to/csv_dupes.csv -s
```

#### Advanced mode (confront hash from the CSV file to real file)
```
python delete_dupes.py -i /path/to/csv_dupes.csv -s -c
```

#### Debug mode
```
python delete_dupes.py -i /path/to/csv_dupes.csv -s -c --log=DEBUG
```

### Possible new features:
- Push deleted files to a different directory with keeping the same structure (recycle bin mode)
- Output report to a CSV file
- Include/Exclude pattern


Tested with a CSV of 90K files


Written & tested with python 2.7
