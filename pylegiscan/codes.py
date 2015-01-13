
"""
LegiScan numeric codes for bill status and progress.

"""

# current aggregate status of bill
BILL_STATUS = {1: "Introduced",
               2: "Engrossed",
               3: "Enrolled",
               4: "Passed",
               5: "Vetoed",
               6: "Failed/Dead"}

# significant steps in bill progress.
BILL_PROGRESS = {1: "Introduced",
                 2: "Engrossed",
                 3: "Enrolled",
                 4: "Passed",
                 5: "Vetoed",
                 6: "Failed/Dead",
                 7: "Veto Override",
                 8: "Chapter/Act/Statute",
                 9: "Committee Referral",
                10: "Committee Report Pass",
                11: "Committee Report DNP"}

