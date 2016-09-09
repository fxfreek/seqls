#! /usr/bin/python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      fxfreek
#
# Created:     25/08/2016
# Copyright:   (c) fxfreek 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os, sys
from operator import itemgetter
from itertools import groupby
from os.path import abspath, basename, isdir
#from sets import Set
path = r"E:\Users\FXFREEK\Pictures\20041014"
path = r"E:\Users\FXFREEK\Pictures\20081221"
path = r"E:\Users\FXFREEK\Pictures"
# path = r"E:\Users\FXFREEK\Pictures"
# print path
files = os.listdir(path)

finalSeqList = []

# def tree(dir, padding, print_files=False):
#     print padding[:-1] + '+-' + basename(abspath(dir)) + '/'
#     padding = padding + ' '
#     files = []
#     if print_files:
#         files = listdir(dir)
#     else:
#         files = [x for x in listdir(dir) if isdir(dir + sep + x)]
#     count = 0
#     for file in files:
#         count += 1
#         print padding + '|'
#         path = dir + sep + file
#         if isdir(path):
#             if count == len(files):
#                 tree(path, padding + ' ', print_files)
#             else:
#                 tree(path, padding + '|', print_files)
#         else:
#             print padding + '+-' + file

# def padFrame(frame,pad):
#     return '0' * (pad - len(str(frame))) + str(frame)

# def tree(dir, padding, print_files=False, isLast=False, isFirst=False):
#     if isFirst:
#         print padding.decode('utf8')[:-1].encode('utf8') + dir
#     else:
#         if isLast:
#             print padding.decode('utf8')[:-1].encode('utf8') + '└── ' + basename(abspath(dir))
#         else:
#             print padding.decode('utf8')[:-1].encode('utf8') + '├── ' + basename(abspath(dir))
#     files = []
#     if print_files:
#         files = listdir(dir)
#     else:
#         files = [x for x in listdir(dir) if isdir(dir + sep + x)]
#     if not isFirst:
#         padding = padding + '   '
#     files = sorted(files, key=lambda s: s.lower())
#     count = 0
#     last = len(files) - 1
#     for i, file in enumerate(files):
#         count += 1
#         path = dir + sep + file
#         isLast = i == last
#         if isdir(path):
#             if count == len(files):
#                 if isFirst:
#                     tree(path, padding, print_files, isLast, False)
#                 else:
#                     tree(path, padding + ' ', print_files, isLast, False)
#             else:
#                 tree(path, padding + '│', print_files, isLast, False)
#         else:
#             if isLast:
#                 print padding + '└── ' + file
#             else:
#                 print padding + '├── ' + file



def find_digits(file):
    digits = []
    ending_digits =[]
    # print file
    #print 'finding digits in ' + file
    try:
        for x in range(0,len(file)):
           #print file[x]
            if file[x].isdigit():
              #  print file[x]
                digits.append(x)
        digits.sort()
        # print digits
        for k, g in groupby(enumerate(digits), lambda (i,x):i-x):
            ending_digits = map(itemgetter(1), g)
           # print ending_digits
        prefix =  file[0:ending_digits[0]]
        frame = file[ending_digits[0]:ending_digits[-1]+1]
        suffix = file[ending_digits[-1]+1:]
       # print prefix, frame, suffix
        #print len(frame)
        if len(frame) ==1:
            prefix =  file[0:ending_digits[0]]
            frame = file[ending_digits[0]:ending_digits[-1]+1]
            suffix = file[ending_digits[-1]+1:]
    except:
        raise ValueError
    return prefix, frame, suffix


def seqLS (dirPath):
    files = os.listdir(dirPath)
    # print files

    for file in files:

        if isdir(os.path.join(dirPath,file)):
            break
        #find_digits(file)
        try:
            # prefix, frame, suffix = file.split('.')
            prefix, frame, suffix = find_digits(file)
            # print prefix, frame, suffix

            # build a dictionary of the sequences as {name: frames, suffix}
            #
            # eg beauty.01.tif ... beauty.99.tif  will convert to
            # { beauty : [01,02,...,98,99], tif }
            # if not frame.isdigit():
            #         prefix, frame, suffix = find_digits(file)

            try:
                result[prefix][0].append(frame)
            except KeyError:
                # we have a new file sequence, so create a new key:value pair
                result[prefix] = [[frame],suffix]

        except ValueError:
            # the file isn't in a sequence, add a dummy key:value pair
            # print
            result[file] = file



    # print result
    for prefix in result:
        #print prefix
       # print result[prefix]
        if result[prefix] != prefix:
            frames = result[prefix][0]
            #print len(frames)
            frames.sort()

            # find gaps in sequence
            startFrame = int(frames[0])
            endFrame = int(frames[-1])
            pad = len(frames[0])
            idealRange = set(range(startFrame,endFrame))
            realFrames = set([int(x) for x in frames])
            # sets can't be sorted, so cast to a list here
            missingFrames = list(idealRange - realFrames)
            missingFrames.sort()

            #calculate fancy ranges
            subRanges = []
            for gap in missingFrames:
                if startFrame != gap:
                    rangeStart = padFrame(startFrame,pad)
                    rangeEnd  = padFrame(gap-1,pad)
                    subRanges.append('-'.join([rangeStart, rangeEnd]))
                startFrame = gap+1

            subRanges.append('-'.join([padFrame(startFrame,pad), padFrame(endFrame,pad) ]))
            frameRanges = ','.join(subRanges)
            frameRanges = '%s' % (frameRanges)
            if len(frames) == 1:
                frameRanges = frames[0]
            suffix = result[prefix][1]
            sortedList.append(''.join([prefix, frameRanges ,suffix]))
            print ('\t\t' + ''.join([prefix, frameRanges ,suffix]))
        else: 
            sortedList.append(prefix)
            print ('\t\t' + prefix )
    # print sortedList


if __name__ == '__main__':

    print sys.argv
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print path
        tree(path, '', False, False, True)
    print path
    for root, dirs, files in os.walk(path):
        # print root
        # result = {}
        # sortedList = []
        # seqLS(root)
        # print sortedList

        for curDir in dirs:
            fulldir = os.path.join(root, curDir)
            print '\t%s' % (curDir)
            result = {}
            sortedList = []
            seqLS(fulldir)