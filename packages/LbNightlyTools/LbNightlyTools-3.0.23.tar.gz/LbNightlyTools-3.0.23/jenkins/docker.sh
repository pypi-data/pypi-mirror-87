#!/bin/bash

if [ -z $main_dir ] ; then
  scripts_dir=$(cd $(dirname $0) ; pwd)
  main_dir=$(cd ${scripts_dir}/.. ; pwd)
fi

if [[ "$os_label" = *docker* ]] ; then
  export os_label=$(echo $platform | cut -d: -f2 | cut -d- -f2)
  export platform=$(echo $platform | cut -d: -f1)
fi

if [ -e $HOME/private ] ; then
  propagate_private="-e PRIVATE_DIR=/tmp/$USER/private -v $HOME/private:/tmp/$USER/private"
fi

cont_name=${slot}.${slot_build_id}.${platform//+/_}${project+.${project}}

curl -o ${main_dir}/jenkins/lb-docker-run https://gitlab.cern.ch/lhcb-core/LbDocker/raw/master/scripts/lb-docker-run
chmod a+x ${main_dir}/jenkins/lb-docker-run

cmd="${main_dir}/jenkins/lb-docker-run \
 --name ${cont_name} \
 -e slot \
 -e platform \
 -e project \
 -e flavour \
 -e scripts_repository \
 -e scripts_version \
 -e NODE_NAME \
 -e slot_build_id \
 -e WORKSPACE=/workspace \
 -e JOB_NAME \
 -e BUILD_NUMBER \
 -e BUILD_URL \
 -e os_label \
 -e JENKINS_HOME \
 -e JENKINS_MOCK \
 -e projects_list \
 -e LBN_BUILD_JOBS \
 -e LBN_LOAD_AVERAGE \
 -e JENKINS_OVERRIDE_PIP_REQUIREMENTS \
 -e JENKINS_RESET_VIRTUALENV \
 --privileged \
 --ssh-agent \
 -v $scripts_dir/docker-home:/userhome \
 $propagate_private \
 --network host \
 --no-interactive \
 --no-lbenv \
 --update"

for mockCopy in python scripts jenkins setup.sh ; do
  if [ ! -e ${WORKSPACE}/$mockCopy ] ; then
    cmd="$cmd -v ${main_dir}/$mockCopy:$PWD/$mockCopy"
  fi
done

# strip -build and -release from os_label
os_label=${os_label%%-build}
os_label=${os_label%%-release}

# check if the current workspace is used by another container
if [ -e ${WORKSPACE}/tmp/container/name.txt ] ; then
  # this means another container is running in this directory, let's kill it
  # (see https://its.cern.ch/jira/browse/LBCORE-1464)
  echo "WARNING: found container using this workspace, killing it now"
  docker kill $(cat ${WORKSPACE}/tmp/container/name.txt) || true
fi

# let's create the stamp file
rm -rf ${WORKSPACE}/tmp/container
# this prevent "git clean -xfd" to remove the directory containing the
# stamp file
git init ${WORKSPACE}/tmp/container
(
  cd ${WORKSPACE}/tmp/container
  git config user.name 'nobody'
  git config user.email 'noreply@cern.ch'
  echo "${cont_name}" > name.txt
  git add .
  git commit -q -m "container name"
)

set -x
$cmd --${os_label} $1
