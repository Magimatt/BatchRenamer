# BatchRenamer
 Batch rename files in folder.

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        [Optional: default=current directory] Full path to directory in quotes. (e.g. "c:    
                        emp")
  -s SELECT, --select SELECT
                        Pattern selection to determine what files to rename (e.g. *.doc)
  -i INCREMENT, --increment INCREMENT
                        Add a number that will increment after each file is renamed. This will overwrite     
                        characters to the left in the old string when the incrementor increases in digits    
                        (e.g. 138)
  -m MULTIPLIER, --multiplier MULTIPLIER
                        Increments files in groups of the given number. I.e if given -m 3 with an
                        incrementor of 1, will name 3 files "01", then the next 3 files "02", etc. (e.g. -m  
                        2)
  -n [NAME ...], --name [NAME ...]
                        Renaming pattern. Each argument should be surrounded in quotes and separated by a    
                        space. (e.g. -n "new name s1e0" "%s" "%s")
  --test                Runs the program in test mode. Does not rename any files. Only prints renamed files  
                        to console.
