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

#
# Common set up for all the Jenkins scripts
#

function set_common {

    local DESCRIPTION="DESCRIPTION : \
Function to define common set up for all the Jenkins scripts"
    local USAGE="USAGE : \
set_common [--build] [--test]"

    local special_config=false

    while (( "$#" )); do
    if [[ "$1" =~ ^- ]] ; then
        case "$1" in
        "--build" | "--test" )
            local special_config=true ;;

        "-h" | "--help")
            echo ${DESCRIPTION}
            echo ${USAGE}
            exit 0;;

        *)
            echo "ERROR : Option $1 unknown in $0"
            echo "${USAGE}"
            exit 2
        esac
    else
        echo "ERROR : $0 doesn't have parameter"
        exit 1
    fi

    shift
    done

    # Need to set HOME on master because HOME not writable when connect by tomcat
    # Need to be FIX
    if [[ "${NODE_LABELS}" == *"master"* ]]
    then
        export HOME=$PWD
    fi

    set -x
    if ( echo $platform | grep -q slc5 ) ; then
      # on SLC5 kinit is not on the standard path and .bash_profile is not
      # called when we run the script in the container
      export PATH=/usr/sue/bin:$PATH
    fi

    export EOS_BASE_URL=root://eosproject.cern.ch/
    export EOS_ARTIFACTS_ROOT=/eos/project/l/lhcbwebsites/www/lhcb-nightlies-artifacts
    export EOS_ARTIFACTS_BASE=${EOS_ARTIFACTS_ROOT}/${flavour}/${slot}
    export EOS_ARTIFACTS_DIR=${EOS_ARTIFACTS_BASE}/${slot_build_id}
    kinit -k -t ${PRIVATE_DIR:-${HOME}/private}/lhcbsoft.keytab lhcbsoft@CERN.CH
    if [ -n "${slot_build_id}" ] ; then
        # we have to make sure the artifacts dir exists
        # (and its ccache subdir, for the ccache_dir)
        EOS_MGM_URL=${EOS_BASE_URL} eos mkdir -p ${EOS_ARTIFACTS_DIR}/ccache
    fi

    # clean up possible stale files
    rm -rf artifacts build tmp

    if [[ "${special_config}" == "true" && $(pwd) != "/workspace" && "${NODE_LABELS}" == *docker* ]] ; then
        exec ${scripts_dir}/docker.sh "$0"
    fi
    set +x

    export CMTCONFIG=${platform}
    export BINARY_TAG=${platform}
    # default (backward-compatible) build flavour
    if [ "${flavour}" == "" ] ; then
        export flavour=nightly
    fi

    # make sure credentials are not exposed
    unset AFS_USER
    unset AFS_PASSWORD
    # initial environment seen by the Jenkins script
    printenv > environment.txt
    python -c 'from os import environ; from pprint import pprint; pprint(dict(environ))' > environment.py

    # enforce C (POSIX) localization
    export LC_ALL=C

    # used by some tests to reduce the number of concurrent tests
    export LHCB_NIGHTLY_MAX_THREADS=1

    export ARTIFACTS_DIR=${ARTIFACTS_DIR:-${PWD}/artifacts/${slot_build_id}}
    mkdir -p ${ARTIFACTS_DIR}
    export TMPDIR=${WORKSPACE}/tmp
    mkdir -p ${TMPDIR}
    export PRIVATE_DIR=${PRIVATE_DIR:-${HOME}/private}

    # copy initial enviroment to artifacts
    env_log_dir=${ARTIFACTS_DIR}/$(basename ${0/.sh/})${platform:+/${platform}}${project:+/${project}}
    mkdir -p ${env_log_dir}
    cp environment.txt environment.py ${env_log_dir}

    echo ===================================================================
    echo Worker Node: $NODE_NAME
    echo Workspace: $WORKSPACE
    echo Artifacts dir: $ARTIFACTS_DIR
    echo EOS destination: $EOS_ARTIFACTS_DIR
    echo ===================================================================

    LbEnvPath=/cvmfs/lhcb.cern.ch/lib/LbEnv-${lbenv_flavour:-testing}.sh

    if [ "${special_config}" == "true" ] ; then
        export LD_LIBRARY_PATH=$(echo $LD_LIBRARY_PATH | tr : \\n | grep -v /gcc/ | tr \\n :)
        . $LbEnvPath -c ${platform}

        # add Intel VTune to the search path
        export CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:/cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/vtune_amplifier

        if [ "$(lb-describe-platform | awk '/^os_id:/{print $2}')" = "slc6" ] ; then
          # avoid a warning from Vc about binutils being too old
          export PATH=/cvmfs/lhcb.cern.ch/lib/lcg/releases/binutils/2.30/x86_64-slc6/bin:$PATH
        fi
    else
        . $LbEnvPath
    fi

    if [ "${USER}" != "lblocal" ] ; then
      if klist -5 > /dev/null 2>&1 ; then
        kinit -R
        klist -5
      fi
    fi

    set -o xtrace -o errexit
    . ./setup.sh

    export SET_COMMON=true
    if [ "${special_config}" == "true" ] ; then
        export SET_SPECIAL_CONFIG=true
    fi

    ulimit -u unlimited || true
    # disable core dumps
    ulimit -c 0
}
