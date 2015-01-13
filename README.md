Python Interface to LegiScan API
================================

Python module for interacting with [LegiScan API](http://legiscan.com/legiscan)
to download information about bills in state legislatures.  This module works
with the "pull API".  You must have an API key to use this module. Register for
a key at [LegiScan API](http://legiscan.com/legiscan).

Functions essentially follow the format described in the 
[API User Manual](http://legiscan.com/misc/LegiScan_API_User_Manual.pdf).


Examples
--------

Read the API User Manual and start by typing `help(LegiScan)` to familiarize
yourself with the available functions.  Here are some examples to get you
started using the module.

Tell the API who you are and search for abortion legislation in the Texas state
legislature for current year...

    legis = LegiScan('MY_API_KEY_GOES_HERE')
    bills = legis.search(state='tx', query='abortion')
    bills['summary']  # how many results did we get?
    
    # print the bill titles
    for b in bills['results']:
        print b['title']

Get more detailed information for the first search result...

    bill_id = bills['results'][0]['bill_id']
    bill_detail = legis.get_bill(bill_id=bill_id)

Figure out who the first sponsor of the bill is...

    people_id = bill_detail['sponsors'][0]['people_id']
    sponsor = legis.get_sponsor(people_id)
    print sponsor['name']


License
-------

Your interaction with the LegiScan API and use of the data is subject to the
[LegiScan Terms of Service](http://legiscan.com/terms-of-service).

This code was written by Chris Poliquin and provided under the MIT License.
Chris Poliquin is not associated with LegiScan Inc.  LegiScan Inc. has not
endorsed this module.

### The MIT License (MIT)

Copyright (c) 2014 Chris Poliquin <cpoliquin@hbs.edu>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

