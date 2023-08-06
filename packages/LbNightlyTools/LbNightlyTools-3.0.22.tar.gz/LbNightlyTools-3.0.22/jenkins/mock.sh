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

# This script is meant as a wrapper around Jenkins scripts so that they can be
# run by hand for testing.
#
# Usage: jenkins/mock.sh <step> <slot> <platform>
#
# where <step> is any of checkout, platforms, preconditions, build
#       <slot> is a slot name
#       <platform> is the platform id string

# Check arguments

if [ $# -lt 3 ] ; then
    echo "Usage: $0 <step> <slot> <platform> [<project>]"
    exit 1
fi

case $1 in
  checkout) step=nightly-builds/checkout ;;
  build)    step=nightly-builds/build ;;
  test)     step=nightly-builds/tests ;;
  *)        echo "invalid step '$1'"
            exit 1 ;;
esac
slot=$2
platform=$3
project=$4
flavour=${flavour:-mock}

export scripts_dir=$(cd $(dirname $0) ; pwd)
export main_dir=$(cd ${scripts_dir}/.. ; pwd)

# Prepare Jenkins-like environment
export slot
export platform
export project
export flavour
export NODE_NAME=$(hostname)
# variables that can be overridden
export slot_build_id=${slot_build_id:-999}
export WORKSPACE=${WORKSPACE:-${main_dir}/mock_workspace}
export JOB_NAME=${JOB_NAME:-nightly-test-slot-build-platform}
guessed_label=${platform#*-}
guessed_label=${guessed_label%%-*}
export os_label=${os_label:-${guessed_label}}
export JENKINS_HOME=${JENKINS_HOME:-jenkins_home}
# this variable might be used inside the Jenkins scripts to avoid some ops
export JENKINS_MOCK=true

command=${scripts_dir}/${step}.sh
if [ ! -e $command ] ; then
    echo "invalid step '$step'"
    exit 1
fi

if [ ! -d $WORKSPACE ] ; then
	mkdir -p $WORKSPACE
fi

cd $WORKSPACE

cmd=$PWD/jenkins/${step}.sh
exec ${scripts_dir}/docker.sh $cmd

#EOF
