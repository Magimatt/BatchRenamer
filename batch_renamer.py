import argparse, glob, os, sys, re

parser = argparse.ArgumentParser(prog="batch_renamer.py",
                                 description='Batch rename files in folder.')
parser.add_argument('-d', '--directory',
                    help=r'[Optional: default=current directory]\n' +
                    'Full path to directory (e.g. "c:\temp")',
                    default=os.getcwd())
parser.add_argument('-s', '--select',
                    help="Pattern selection to determine what files to " +
                         "rename (e.g. *.doc)",
                    required=True)
parser.add_argument('-i', '--increment',
                    help="Add a number that will increment after each file " +
                         "is renamed. This will overwrite characters to the" +
                         " left in the old string if the incrementor " +
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
                         "files. Only prints test filenames to console.")
args = parser.parse_args()

def main(args):
    if args.test is not None:
        test_rename(args.directory, args.select, args.name, args.increment, args.multiplier)
    else:
        rename(args.directory, args.select, args.name, args.increment, args.multiplier)


'''
USAGE:
batch_renamer.py -d "c:/temp" -s *.doc -i 138 -m 2 -n "this " "%d " "is " "%s " "new"

The above example will convert all *.doc files in c:/temp dir to new%d%s.doc,
where %d is the incrementor and %s is the previous base name of the file.
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
            try:
                os.rename(pathAndFilename, newFilename)
            except FileExistsError:
                print(f"ERROR: The file name '{newFilename}' already exists and cannot be created.")
                isBadInput = True
                while isBadInput:
                    userInput = input("Do you wish to continue renaming? Y or N\n").upper()
                    if userInput == 'Y':
                        isBadInput = False
                        continue
                    elif userInput == 'N':
                        isBadInput = False
                        exit()
                    else:
                        print("Please type 'Y' or 'N'.")
                        continue
            

            fileCount += 1
        else:
            titlePattern = "".join(titlePattern)
            os.rename(pathAndFilename,
                  os.path.join(dir, titlePattern % title + ext))

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
Take the pattern and remove the length of the incrementor plus any newly
renamed characters. That length is removed from the front of the original
title. The new filename path is then constructed out of the new pattern
with the correct characters substituted.
'''
def name_recombobulator(dir, titlePattern, incrementor, title, ext,
               initIncrementorLength):
    '''if the incrementor increases in  magnitude the amount of digits will
    increase. We need to slice the titlePattern if that happens, but only from
    the prefix (e.g. "new%d%s" splits to prefix="new", suffix="%d%s")'''
    incrementorIndex = [titlePattern.index(x) for x in titlePattern if re.match("%d", x)][0]
    oldTitleIndex = [titlePattern.index(x) for x in titlePattern if re.match("%s", x)][0]

    incrementorLengthDelta = len(str(incrementor)) - initIncrementorLength
    #modifiedPattern = re.sub(r"%.", "", titlePattern)

    '''modifiy the argument before the incrementor argument if the incrementor
    increase digits '''
    if (incrementorLengthDelta > 0):
        #patternPrefix = modifiedPattern
        modifiedPrefix = titlePattern[incrementorIndex - 1]
        #patternSuffix = titlePattern[len(modifiedPattern):len(titlePattern)]
        #modifiedPrefix = patternPrefix[0:incrementorLengthDelta * -1]
        modifiedPrefix = modifiedPrefix[0:incrementorLengthDelta * -1]
        #modifiedTitlePattern = modifiedPrefix + patternSuffix
        titlePattern[incrementorIndex - 1] = modifiedPrefix

    #replaceLength = len(modifiedPattern) + len(str(incrementor))
    #modifiedTitle = title[replaceLength:]
    #combinedStr = titlePattern % (incrementor, modifiedTitle + ext)
    titlePattern[incrementorIndex] = titlePattern[incrementorIndex] % incrementor
    modifiedTitle = ""
    for index in range(0, incrementorIndex + 1):
        modifiedTitle += titlePattern[index]
    modifiedTitle = title[len(modifiedTitle):]
    titlePattern[oldTitleIndex] = titlePattern[oldTitleIndex] % modifiedTitle
    combinedStr = "".join(titlePattern) + ext
    return os.path.join(dir, combinedStr)


'''
take any number of arguments in the renaming pattern (e.g. command:
batchrenamer.py -d c:\temp -s s01e00*.mp4 -i 1
                -n "this - " "%d " "is " "%s " "- new.ext")

'''

if __name__ == "__main__":
    main(args)