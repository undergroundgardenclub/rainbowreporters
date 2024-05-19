#!/bin/bash -x
# set -e will abort this script on non-zero exist codes. Ex) Jest error is a 1
set -e

# //////////////////////////////////////////////////////////////////////////////
# Variables
# //////////////////////////////////////////////////////////////////////////////

# Loggings
UNDERLINE='\033[4;37m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[1;31m'
NC='\033[0m'

# Paths/Labels
RR_PATH="$PWD"
echo "RR_PATH: ${RR_PATH}"
RR_BACKENDS_API_PATH="$RR_PATH/services/backends-api"
RR_DATA_PATH="$RR_PATH/data"
RR_FRONTENDS_WWW_BUILD_PATH="$RR_PATH/services/frontends-www/dist"
RR_FRONTENDS_WWW_PATH="$RR_PATH/services/frontends-www"

# Env
VALID_ENVIRONMENTS="local production"
TARGET_ENV=$1
if echo $VALID_ENVIRONMENTS | grep -w $TARGET_ENV >> /dev/null; then
  echo "Recognized Environment: '${TARGET_ENV}'"
  source ./.env
else # bad case
  echo
  echo -e "Error: unrecognized environment: $RED"$TARGET_ENV"$NC"
  echo '  Must be one of: '$VALID_ENVIRONMENTS
  echo
  exit 1
fi

FLY_ORG_NAME=$FLY_ORG_NAME
GIT_SHA="$(git rev-parse HEAD)"


# //////////////////////////////////////////////////////////////////////////////
# Common Functions
# //////////////////////////////////////////////////////////////////////////////

function confirm_command () {
  # Remind of environment
  echo -e "Env: ${UNDERLINE}${TARGET_ENV}${NC}"
  # Remind of command
  if [[ -n "$1" ]]
  then
    echo -e "Cmd: ${UNDERLINE}run.sh ${1} ${2} ${3} ${4}${NC}\n"
  fi
  # Confirm
  read -p "Are you sure? [Y/n] " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Y]$ ]]
  then
    echo -e "${GREEN}Running${NC}\n"
  else
    echo -e "${RED}Aborting${NC}\n"
    exit 0
  fi
}

function confirm_finish() {
  echo -e "\n${GREEN}run.sh - Finished${NC}\n"
}

function get_secret {
  echo $(bash "${RR_PATH}/ops/get-secret.sh" -o $FLY_ORG_NAME -a backends-api $1)
}


# //////////////////////////////////////////////////////////////////////////////
# Run
# //////////////////////////////////////////////////////////////////////////////
COMMAND=$2
OPTION_ONE=$3
OPTION_TWO=$4
OPTION_THREE=$5
echo -e "${GREEN}run.sh - $COMMAND ${OPTION_ONE} ${OPTION_TWO} ${OPTION_THREE}${NC}\n"

case "${COMMAND}" in
  deploy:backends-api)
  confirm_command $COMMAND $OPTION_ONE
  cp -r $RR_DATA_PATH $RR_BACKENDS_API_PATH # copy data into working dir for docker build context
  fly deploy $RR_BACKENDS_API_PATH -a backends-api
  ;;
  deploy:frontends-www)
  confirm_command $COMMAND $OPTION_ONE
  fly deploy $RR_FRONTENDS_WWW_PATH -a frontends-www
  ;;
  *)
  echo "Unrecognized Service: '${2}'"
  exit 1
  ;;
esac


# //////////////////////////////////////////////////////////////////////////////
# Exit
# //////////////////////////////////////////////////////////////////////////////
echo "Exiting run.sh"
exit 0
