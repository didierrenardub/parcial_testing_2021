import os

from time import sleep

def bkp_issues(time_seconds: int):
    """bkp a file every X seconds
    
    Run this on the same dir as the src file
    """

    while True:
        os.system("cp issue.tracker issue.tracker.bkp")
        sleep(time_seconds)

bkp_issues(5)