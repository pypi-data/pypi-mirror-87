#!/usr/bin/env bash

export buildid="${slot}.${slot_build_id}"
export artifactsdir="${ARTIFACTS_DIR}"

export lhcbpr_api_url=${lhcbpr_api_url:-"https://lblhcbpr.cern.ch/api"}

lhcbpr_check_ssl_cmd=$( [ ! -z ${NOSQL+x} ] && echo "--check-ssl")
echo "Build file to run test"
lbpr-get-command  --url $lhcbpr_api_url $lhcbpr_check_ssl_cmd -o runtest.sh  $project $buildid $platform  $testgroup $testenv $config_file
echo
echo "Now running the test"
mycount=${count:-1}
echo "Will run the test $mycount time(s)"
for i in `seq 1 $mycount`; do
    sh runtest.sh $i
    if [[ $? -ne 0 ]]; then
	break
    fi
done
