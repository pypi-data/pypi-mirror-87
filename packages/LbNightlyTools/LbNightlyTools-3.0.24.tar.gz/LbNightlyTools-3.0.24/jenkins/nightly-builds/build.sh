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

. $(dirname $0)/../utils.sh

set_common --build

if [ "$JENKINS_MOCK" != "true" ] ; then
    # FIXME: workaround for SLC5
    # EOS_MGM_URL=${EOS_BASE_URL} eos cp --recursive -p ${EOS_ARTIFACTS_DIR}/packs/src/ ${ARTIFACTS_DIR}/packs/
    mkdir -p ${ARTIFACTS_DIR}/{packs/src,ccache,rpms}/
    EOS_MGM_URL=${EOS_BASE_URL} eos cp $(EOS_MGM_URL=${EOS_BASE_URL} eos \
                                         find -f --maxdepth 1 ${EOS_ARTIFACTS_DIR}/packs/src/) \
                                       ${ARTIFACTS_DIR}/packs/src/

    EOS_MGM_URL=${EOS_BASE_URL} eos cp -p ${EOS_ARTIFACTS_DIR}/{configs.zip,slot.patch} ${ARTIFACTS_DIR}/
    if [ "${flavour}" != "release" ] ; then
        # note that we ignore errors when retrieving the ccache dir
        # FIXME: workaround for SLC5
        # EOS_MGM_URL=${EOS_BASE_URL} eos cp -p ${EOS_ARTIFACTS_DIR}/ccache/"*${platform}*" ${ARTIFACTS_DIR}/ccache/ || true
        cache=$(EOS_MGM_URL=${EOS_BASE_URL} eos \
                find -f --maxdepth 1 ${EOS_ARTIFACTS_DIR}/ccache/ | grep ${platform}) || true
        if [ -n "$cache" ] ; then
            EOS_MGM_URL=${EOS_BASE_URL} eos cp $cache ${ARTIFACTS_DIR}/ccache/ || true
        fi
    else
        # only for release builds we try to get the source RPMs too
        EOS_MGM_URL=${EOS_BASE_URL} eos cp $(EOS_MGM_URL=${EOS_BASE_URL} eos \
                                find -f --maxdepth 1 ${EOS_ARTIFACTS_DIR}/rpms/ | grep '/[^_/]\+_[^_/]\+rpm$') \
                                           ${ARTIFACTS_DIR}/rpms/ || true
    fi

    # Drop all platform related products
    for d in build packs tests ; do
        EOS_MGM_URL=$EOS_BASE_URL eos rm -r ${EOS_ARTIFACTS_DIR}/${d}/${platform} || true
    done
fi

CCACHE_LIMITS="-M 0 -F 0"
if [ ! -e "${ARTIFACTS_DIR}/ccache/ccache_dir.${slot}.${platform}.zip" ] ; then
    # if there is no previous ccache dir, we initialize an empty one
    if which ccache &>/dev/null ; then
        mkdir -p ${PWD}/build/.ccache
        env CCACHE_DIR=${PWD}/build/.ccache ccache ${CCACHE_LIMITS}
        mkdir -p "${ARTIFACTS_DIR}/ccache"
        (cd build && zip -r -q "${ARTIFACTS_DIR}/ccache/ccache_dir.${slot}.${platform}.zip" .ccache)
    fi
fi

build_slot \
    "${flavour}" \
    "${slot}" \
    "${slot_build_id}" \
    "${platform}" \
    --build-dir "${ARTIFACTS_DIR}" \
    ${os_label:+--os-label "${os_label}"}
