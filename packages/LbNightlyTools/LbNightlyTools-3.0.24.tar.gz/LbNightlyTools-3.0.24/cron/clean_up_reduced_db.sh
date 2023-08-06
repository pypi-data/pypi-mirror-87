#!/bin/bash
###############################################################################
# (c) Copyright 2013 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

# Ensure that the dasboard's database contains all the summaries from the
# builds.

# Note: this script must be run from the machine where CouchDB is installed

# prepare environment
rootdir=$(dirname $0)/..
cd $rootdir

. setup.sh

python >> /eos/user/l/lhcbsoft/logs/clean_up_reduced_db.log 2>&1 <<EOF
import logging
logging.basicConfig(level=logging.DEBUG)
from LbNightlyTools import Dashboard
from datetime import date, timedelta, datetime
from itertools import groupby
print('%s: removing old data from reduced db' % datetime.now())
# we keep only 14 days
end_date = (date.today() - timedelta(days=15)).isoformat()
d = Dashboard(server='https://lhcb-couchdb.cern.ch/', dbname='nightlies-reduced')

def next_day():
    from itertools import groupby
    key, rows = groupby(d.db.iterview('summaries/byDay', batch=100,
                                      endkey=end_date, include_docs=True),
                        lambda r: r.key).next()
    return key, [{'_id': r.id, '_rev': r.doc['_rev'], '_deleted': True}
                 for r in rows]

def days():
    while True:
        yield next_day()

for key, rows in days():
    print('-> cleaning {} ({} documents)'.format(key, len(rows)))
    d.db.update(rows)
EOF
