#!/bin/bash
# these are travis encrypted in the env section
docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASS

# for final PR make sure to also check TRAVIS_BRANCH to make sure it is master and also
# check our slug TRAVIS_REPO_SLUG to make sure we are crops/ and not bavery/ or todor/
echo "TRAVIS_REPO_SLUG=$TRAVIS_REPO_SLUG"
TRAVIS_USER=`echo $TRAVIS_REPO_SLUG | cut -d '/' -f1`
if [ "`cat ./scripts/repoMapping.txt | grep -v "#" | grep $TRAVIS_USER`" != "" ]; then
    DOCKERHUB_REPO=`cat ./scripts/repoMapping.txt | grep -v "#" | grep $TRAVIS_USER| awk '{print $2}'`
    echo "OVERRIDE, TRAVIS_USER set to $TRAVIS_USER"
else
    DOCKERHUB_REPO=$TRAVIS_USER
fi
docker images | grep ${DOCKERHUB_REPO}\/ | grep -v deps | grep -v \<none\> | awk '{print $1 ":" $2}'
if [ "$TRAVIS_PULL_REQUEST" = "false" ]; then
    # l8r also check $TRAVIS_REPO_SLUG so we only push to dockerhub on master
    for i in `docker images | grep ${DOCKERHUB_REPO}\/ | grep -v deps | grep -v \<none\> | awk '{print $1 ":" $2}'`; do
	echo Pushing $i
	docker push $i
    done
else
    print "No Pushy, TRAVIS_PULL_REQUEST=$TRAVIS_PULL_REQUEST"

fi
