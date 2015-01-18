
import os
import json
from urllib import urlencode
from urllib import quote_plus

from codes import BILL_STATUS, BILL_PROGRESS

try:
    import requests
except:
    print '\nThis program requires the Python requests module.'
    print 'Install using: pip install requests\n'
    raise

"""
Interact with LegiScan API.

"""

# a helpful list of valid legiscan state abbreviations (no Puerto Rico)
STATES = ['ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga',
          'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me',
          'mi', 'mn', 'mo', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm',
          'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx',
          'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy']

class LegiScanError(Exception):
    pass

class LegiScan(object):
    BASE_URL = 'http://api.legiscan.com/?key={0}&op={1}&{2}'

    def __init__(self, apikey=None):
        """LegiScan API.  State parameters should always be passed as
           USPS abbreviations.  Bill numbers and abbreviations are case
           insensitive.  Register for API at http://legiscan.com/legiscan
        """
        # see if API key available as environment variable
        if apikey is None:
            apikey = os.environ['LEGISCAN_API_KEY']
        self.key = apikey.strip()

    def _url(self, operation, params=None):
        """Build a URL for querying the API."""
        if not isinstance(params, str) and params is not None:
            params = urlencode(params)
        elif params is None:
            params = ''
        return self.BASE_URL.format(self.key, operation, params)

    def _get(self, url):
        """Get and parse JSON from API for a url."""
        req = requests.get(url)
        if not req.ok:
            raise LegiScanError('Request returned {0}: {1}'\
                    .format(req.status_code, url))
        data = json.loads(req.content)
        if data['status'] == "ERROR":
            raise LegiScanError(data['alert']['message'])
        return data

    def get_session_list(self, state):
        """Get list of available sessions for a state."""
        url = self._url('getSessionList', {'state': state})
        data = self._get(url)
        return data['sessions']

    def get_master_list(self, state=None, session_id=None):
        """Get list of bills for the current session in a state or for
           a given session identifier.
        """
        if state is not None:
            url = self._url('getMasterList', {'state': state})
        elif session_id is not None:
            url = self._url('getMasterList', {'id': session_id})
        else:
            raise ValueError('Must specify session identifier or state.')
        data = self._get(url)
        # return a list of the bills
        return [data['masterlist'][i] for i in data['masterlist']]

    def get_bill(self, bill_id=None, state=None, bill_number=None):
        """Get primary bill detail information including sponsors, committee
           references, full history, bill text, and roll call information.

           This function expects either a bill identifier or a state and bill
           number combination.  The bill identifier is preferred, and required
           for fetching bills from prior sessions.
        """
        if bill_id is not None:
            url = self._url('getBill', {'id': bill_id})
        elif state is not None and bill_number is not None:
            url = self._url('getBill', {'state': state, 'bill': bill_number})
        else:
            raise ValueError('Must specify bill_id or state and bill_number.')
        return self._get(url)['bill']

    def get_bill_text(self, doc_id):
        """Get bill text, including date, draft revision information, and
           MIME type.  Bill text is base64 encoded to allow for PDF and Word
           data transfers.
        """
        url = self._url('getBillText', {'id': doc_id})
        return self._get(url)['text']

    def get_amendment(self, amendment_id):
        """Get amendment text including date, adoption status, MIME type, and
           title/description information.  The amendment text is base64 encoded
           to allow for PDF and Word data transfer.
        """
        url = self._url('getAmendment', {'id': amendment})
        return self._get(url)['amendment']

    def get_supplement(self, supplement_id):
        """Get supplement text including type of supplement, date, MIME type
           and text/description information.  Supplement text is base64 encoded
           to allow for PDF and Word data transfer.
        """
        url = self._url('getSupplement', {'id': supplement_id})
        return self._get(url)['supplement']

    def get_roll_call(self, roll_call_id):
        """Roll call detail for individual votes and summary information."""
        data = self._get(self._url('getRollcall', {'id': roll_call_id}))
        return data['roll_call']

    def get_sponsor(self, people_id):
        """Sponsor information including name, role, and a followthemoney.org
           person identifier.
        """
        url = self._url('getSponsor', {'id': people_id})
        return self._get(url)['person']

    def search(self, state, bill_number=None, query=None, year=2, page=1):
        """Get a page of results for a search against the LegiScan full text
           engine; returns a paginated result set.

           Specify a bill number or a query string.  Year can be an exact year
           or a number between 1 and 4, inclusive.  These integers have the
           following meanings:
               1 = all years
               2 = current year, the default
               3 = recent years
               4 = prior years
           Page is the result set page number to return.
        """
        if bill_number is not None:
            params = {'state': state, 'bill': bill_number}
        elif query is not None:
            params = {'state': state, 'query': query,
                      'year': year, 'page': page}
        else:
            raise ValueError('Must specify bill_number or query')
        data = self._get(self._url('search', params))['searchresult']
        # return a summary of the search and the results as a dictionary
        summary = data.pop('summary')
        results = {'summary': summary, 'results': [data[i] for i in data]}
        return results

    def __str__(self):
        return '<LegiScan API {0}>'.format(self.key)

    def __repr__(self):
        return str(self)

