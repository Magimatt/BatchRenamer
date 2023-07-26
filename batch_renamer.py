import argparse, glob, os, sys, re

# argparse setup
parser = argparse.ArgumentParser(prog="batch_renamer.py",
                                 description='Batch rename files in folder.')
parser.add_argument('-d', '--directory',
                    help='[Optional: default=current directory]\n' +
                    'Full path to directory in quotes. (e.g. "c:\temp")',
                    default=os.getcwd())
parser.add_argument('-s', '--select',
                    help="Pattern selection to determine what files to " +
                         "rename (e.g. *.doc)",
                    required=True)
parser.add_argument('-i', '--increment',
                    help="Add a number that will increment after each file " +
                         "is renamed. This will overwrite characters to the" +
                         " left in the old string when the incrementor " +
                         "increases in digits (e.g. 138)",
                    type=int, default=None)
parser.add_argument('-m', '--multiplier',
                    help='Increments files in groups of the given number.\n' +
                         'I.e if given -m 3 with an incrementor of 1, will ' +
                         'name 3 files "01", then the next 3 files "02", ' +
                         'etc. (e.g. -m 2)',
                    type=int, default=1)
parser.add_argument('-n', '--name', nargs='*',
                    help='Renaming pattern. Each argument should be ' +
                         'surrounded in quotes and separated by a space. ' +
                         r'(e.g. -n "new name s1e0" "%d" "%s")',
                    required=True)
parser.add_argument('--test', action='store_const', const=True, default=None,
                    help="Runs the program in test mode. Does not rename any " +
                         "files. Only prints renamed files to console.")
args = parser.parse_args()


def main(args):
    # Test flag conditional
    if args.test is not None:
        test_rename(args.directory, args.select, args.name, args.increment, args.multiplier)
    else:
        rename(args.directory, args.select, args.name, args.increment, args.multiplier)


''' function to rename file names
- break up the filepath in to directory(dir), filename(title), and extention(ext)
- if increment argument is given, then the title and ext is passed to
    name_recombobulator(). The modified filename is returned.
- if the is no increment argument given then the file is renamed simply and returned
'''
def rename(dir, pattern, titlePattern, incrementor, multiplier):
    initIncrementorLength = len(str(incrementor))
    fileCount = 0
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        if incrementor is not None:
            newFilename = name_recombobulator(dir, titlePattern[:],
                                              int(fileCount // multiplier + incrementor),
                                              title, ext,
                                              initIncrementorLength)
            
            # try except block catches if the filename already exists
            try:
                os.rename(pathAndFilename, newFilename)
            except FileExistsError:
                print(f"ERROR: The file name '{newFilename}' already exists " +
                      "and cannot be created.")
                isBadInput = True
                while isBadInput:
                    userInput = input("Do you wish to continue renaming? " +
                                      "Y or N\n").upper()
                    if userInput == 'Y':
                        isBadInput = False
                        continue
                    elif userInput == 'N':
                        isBadInput = False
                        exit()
                    else:
                        print("Please type 'Y' or 'N'.")
                        continue
            # increment the fileCount to do 'multiplier' math
            fileCount += 1

        else:
            titlePattern = "".join(titlePattern)
            os.rename(pathAndFilename,
                  os.path.join(dir, titlePattern % title + ext))


# everything that the Rename() function does, but outputs to console instead.
def test_rename(dir, pattern, titlePattern, incrementor, multiplier):
    initIncrementorLength = len(str(incrementor))
    fileCount = 0
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        if incrementor is not None:
            newFilename = name_recombobulator(dir, titlePattern[:],
                                              int(fileCount // multiplier + incrementor),
                                              title, ext, initIncrementorLength)
            print(newFilename)

            fileCount += 1
        else:
            titlePattern = "".join(titlePattern)
            print(os.path.join(dir, titlePattern % title + ext))


'''
- Take the pattern and remove the length of the incrementor plus any newly
    renamed characters.
- That length is removed from the front of the original title.
- The new filename path is then constructed out of the new pattern with the
    correct characters substituted.
'''
def name_recombobulator(dir, titlePattern, incrementor, title, ext,
               initIncrementorLength):
    ''' if the incrementor increases in digits we need to slice the
    titlePattern if that happens, but only from the previous argument
    (e.g. "new%d%s" splits to prefix="new", suffix="%d%s") '''
    # these two list comps gets the index of the incrementor and the old
    # filename arguments
    incrementorIndex = [titlePattern.index(x) for x in titlePattern if re.match("%d", x)][0]
    oldTitleIndex = [titlePattern.index(x) for x in titlePattern if re.match("%s", x)][0]

    incrementorLengthDelta = len(str(incrementor)) - initIncrementorLength

    '''modifiy the argument before the incrementor argument if the incrementor
    increase digits '''
    if (incrementorLengthDelta > 0):
        modifiedPrefix = titlePattern[incrementorIndex - 1]
        modifiedPrefix = modifiedPrefix[0:incrementorLengthDelta * -1]
        titlePattern[incrementorIndex - 1] = modifiedPrefix
    
    # insert the incrementor into the "%d" argument
    titlePattern[incrementorIndex] = titlePattern[incrementorIndex] % incrementor
    
    # get the length of the incrementor plus length of all characters to the
    # left of the incrementor.
    modifiedTitle = ""
    for index in range(0, incrementorIndex + 1):
        modifiedTitle += titlePattern[index]
    modifiedTitle = title[len(modifiedTitle):]
    
    # insert a slice of the old file name
    titlePattern[oldTitleIndex] = titlePattern[oldTitleIndex] % modifiedTitle

    # join all the modified arguments and the extension
    combinedStr = "".join(titlePattern) + ext
    return os.path.join(dir, combinedStr)


if __name__ == "__main__":
    main(args)