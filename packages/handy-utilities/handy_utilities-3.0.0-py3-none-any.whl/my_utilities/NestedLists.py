
import sys


"""

This function prints all elements of a list and its child lists if any.
Before executing it also checks if the root argument is a list or not.

"""

def printNestedList(meraList, indent=False, level=0, whereToWrite=sys.stdout):

    if(isinstance(meraList, list)):

        for each_item in meraList:
            if isinstance(each_item, list):
                printNestedList(each_item, indent, level+1, whereToWrite)
            else:
                if(indent):
                    for i in range(level):
                        print("\t", end='', file=whereToWrite)
                    print(each_item, file=whereToWrite)
                else:
                    print(each_item, file=whereToWrite)
    else:
        print(meraList+" is not a list")
