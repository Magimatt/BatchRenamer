# BatchRenamer
 Batch rename files in folder.
 
 <p>options:<br>
 -h, --help<br>
 show this help message and exit<br>
 <br>
 -d DIRECTORY, --directory DIRECTORY\n<br>
 [Optional: default=current directory] Full path to directory in quotes. (e.g. "c:\temp")<br>
 <br>
 -s SELECT, --select SELECT<br>
 Pattern selection to determine what files to rename (e.g. *.doc)<br>
 <br>
 -i INCREMENT, --increment INCREMENT<br>
 [Optional: default=None] Add a number that will increment after each file is renamed. This will overwrite characters to the left in the old string when the incrementor increases in digits (e.g. 138)<br>
 <br>
 -m MULTIPLIER, --multiplier MULTIPLIER<br>
 [Optional default=1] Increments files in groups of the given number. I.e if given -m 3 with an incrementor of 1, will name 3 files "01", then the next 3 files "02", etc. (e.g. -m 2)<br>
 <br>
 -n [NAME ...], --name [NAME ...]<br>
 Renaming pattern. Each argument should be surrounded in quotes and separated by a space. (e.g. -n "new name s1e0" "%s" "%s")<br>
 <br>
 --test<br>
 [Optional] Runs the program in test mode. Does not rename any files. Only prints renamed files to console.
