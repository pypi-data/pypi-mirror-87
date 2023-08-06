#!/bin/bash -e
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

. $(dirname $0)/../utils.sh

set_common

# ensure that we do not use stale configuration files
# (unless we are testing with jenkins/mock.sh)
if [ "${JENKINS_MOCK}" != true ] ; then
    rm -rf configs
fi

# checkout configs only if missing
[ -e configs ] || lbn-get-configs

# Dump the current configuration to stdout (ignore errors)
set +e
lbn-check-config
set -e

rm -rf slot-params-*.txt

# extract list of enabled or requested slots
lbn-enabled-slots --debug \
    --resolve-mrs \
    --flavour "${flavour}" \
    ${slots:+--slots "${slots}"} \
    --output 'slot-params-{name}.txt'
