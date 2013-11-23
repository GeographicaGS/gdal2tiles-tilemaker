'''
Created on 19/11/2013

@author: alasarr
'''
import sys

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
            
def timeString(elapsed_time):
    
    if elapsed_time >= 60*60:
        hours = int(elapsed_time/(60*60))
        minutes = int((elapsed_time%(60*60)) / 60) 
        seconds = (elapsed_time%(60*60))%60
        return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"
    elif elapsed_time >= 60:
        minutes = int(elapsed_time/60) 
        seconds = elapsed_time%60
        return str(minutes) + "m " + str(seconds) + "s"
    else:
        return str(elapsed_time) + "s"    
