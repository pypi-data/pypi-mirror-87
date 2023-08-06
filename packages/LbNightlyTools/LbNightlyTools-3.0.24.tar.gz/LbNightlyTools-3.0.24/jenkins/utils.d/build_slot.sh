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

function build_slot {

    loglevel_opt="--debug"

    local DESCRIPTION="DESCRIPTION : \
Function to build a slot on a specify platform"
    local USAGE="USAGE : \
build_slot flavour slot slot_build_id platform
                [--build-dir <dir>]
                [--os-label <label>]"

    local nb_param=0

    while (( "$#" )); do
        if [[ "$1" =~ ^- ]] ; then
            case "$1" in
                "--build-dir")
                    if [[ "$2" = "" || "$2" =~ ^- ]] ; then
                        echo "ERROR : Option $1 needs an argument"
                        exit 3
                    else
                        local directory="$2"
                    fi
                    shift ;;

                "--os-label")
                    if [[ "$2" = "" || "$2" =~ ^- ]] ; then
                        echo "ERROR : Option $1 needs an argument"
                        exit 3
                    else
                        local os_label="$2"
                    fi
                    shift ;;

                "-h" | "--help")
                    echo ${DESCRIPTION}
                    echo ${USAGE}
                    exit 0;;
                *)
                    echo "ERROR : Option $1 unknown in $0"
                    echo ${USAGE}
                    exit 2
            esac
        else
            case "${nb_param}" in
                "0")
                    local flavour="$1" ;;
                "1")
                    local slot="$1" ;;
                "2")
                    local slot_build_id="$1" ;;
                "3")
                    local platform="$1" ;;
                *)
                    echo "ERROR : Too many parameters"
                    echo ${USAGE}
                    exit 1
            esac
            local nb_param=$((nb_param+1))
        fi

        shift
    done

    if [ "${nb_param}" != "4" ] ; then
        echo "ERROR : Need more parameters"
        echo ${USAGE}
        exit 1
    fi

    # ensure that the distcc lock directory exists
    if [ -n "$DISTCC_DIR" ] ; then
        mkdir -pv $DISTCC_DIR
    fi

    if [[ "${slot}" = lhcb-coverity ]] ; then
        coverity_opt='--coverity --no-ccache'
        # Coverity builds do not need to trigger tests
        with_tests=no
        # ensure that Coverity is on the PATH
        if [ -e /coverity/cov-analysis/bin ] ; then
            export PATH=/coverity/cov-analysis/bin:${PATH}
        fi
        # set Coverity database password for commit
        if [ -e ${PRIVATE_DIR}/coverity.txt ] ; then
            export COVERITY_PASSPHRASE=$(cat ${PRIVATE_DIR}/coverity.txt)
        fi
    fi

    if [ "$JENKINS_MOCK" != "true" ] ; then
        submit_opt="--submit --flavour ${flavour}"
        rsync_opt="--rsync-dest ${EOS_ARTIFACTS_DIR}"
    fi

    # use a local ccache cache directory
    export CCACHE_DIR=${PWD}/build/.ccache
    # tel ccache to call the compiler on the files and not on the preprocessed version
    export CCACHE_CPP2=yes

    time lbn-build ${loglevel_opt} \
                   --build-id "${slot}.${slot_build_id}" \
                   --artifacts-dir "${directory}" \
                   --clean \
                   ${submit_opt} \
                   ${rsync_opt} \
                   ${coverity_opt} \
                   "${slot}.${slot_build_id}"

    if [ -e build/.ccache ] ; then
        if which ccache &>/dev/null ; then
          mkdir -p ${directory}/build/${platform}
          echo "===== ccache stats ====="
          ccache -s | tee ${directory}/build/${platform}/ccache.stats
          echo "========================"
          # reduce cache size
          ccache -F $(awk '/hit [^r]|miss/{sum += $NF}END{print int(sum * 3)}' ${directory}/build/${platform}/ccache.stats)
          ccache -c
          # reset ccache stats and limits before next build
          ccache -z ${CCACHE_LIMITS}
        fi
        # publish the local ccache directory as artifact
        mkdir -p "${directory}/ccache"
        (cd build && time zip -r -q "${directory}/ccache/ccache_dir.${slot}.${platform}.zip" .ccache)
    fi

    if [ "${flavour}" = "release" -o -n "${make_rpm}" ] ; then
        # ensure the current build directory is in the search path
        export CMAKE_PREFIX_PATH=$PWD/build:$CMAKE_PREFIX_PATH
        # Prepare the RPMs
        time lbn-rpm ${loglevel_opt} ${flavour:+--flavour ${flavour}} --build-id "${slot}.${slot_build_id}" --artifacts-dir "${directory}" "${slot}.${slot_build_id}" --platform "${platform}"
        createrepo ${directory}/rpms
        if [[ "$platform" != *-slc5-* ]] ; then
            lbn-rpm-validator -d --build-folder=${directory}/rpms --repo-url=file:${directory}/rpms ${platform}
        fi
    fi

    if [ "$JENKINS_MOCK" != "true" ] ; then
        EOS_MGM_URL=${EOS_BASE_URL} eos rm ${EOS_ARTIFACTS_DIR}/ccache/ccache_dir.${slot}.${platform}.zip || true
        EOS_MGM_URL=${EOS_BASE_URL} eos cp --recursive -p --no-overwrite ${directory}/ ${EOS_ARTIFACTS_BASE}/
    fi

    # if possible and requested, generate glimpse indexes and upload them to lhcb-archive
    if [ "${flavour}" = "release" -o -n "${run_indexer}" ] ; then
        if which glimpseindex &> /dev/null ; then
            # clean up the build dir before indexing
            rm -rf build
            mkdir build
            for subdir in "${directory}"/packs/{src,shared,${platform}} ; do
              if [ -d ${subdir} ] ; then
                for z in $(find ${subdir} -name '*.zip') ; do
                  unzip -o $z -d build
                done
              fi
            done
            time lbn-index ${loglevel_opt} \
                           ${flavour:+--flavour ${flavour}} \
                           --build-id "${slot}.${slot_build_id}" \
                           --artifacts-dir "${directory}" \
                           "${slot}.${slot_build_id}"
            if [ "${flavour}" = "release" -o -n "${make_rpm}" ] ; then
                time lbn-rpm --glimpse ${loglevel_opt} ${flavour:+--flavour ${flavour}} --build-id "${slot}.${slot_build_id}" --artifacts-dir "${directory}" "${slot}.${slot_build_id}"
            fi
            if [ "$JENKINS_MOCK" != "true" ] ; then
                EOS_MGM_URL=${EOS_BASE_URL} eos cp --recursive -p --no-overwrite ${directory}/ ${EOS_ARTIFACTS_BASE}/
            fi
        fi
    fi

    if [ "$JENKINS_MOCK" != "true" ] ; then
        # Clean up
        rm -rf ${directory} build tmp
    fi

}
