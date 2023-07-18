#!/bin/bash

# this script will send a POST to the rest API to set email verification based on your option. You can also use the list option to query the API for user info to validate.


function print_help {
        echo "Usage: $0 [-v|-u|-l] email_address"
        echo "Options:"
        echo "  -v      Verify an email address within the API"
        echo "  -u      Unverify an email address within the API"
        echo "  -l      Query and list the user's API info"
        echo "  -h      Print the help menu"
        exit 1
}


if [ $# -eq 0 ];
then
        print_help
fi



while getopts ":vul:h" option; do
  case $option in
    v)
      podman exec -it mailman-core curl --user restadmin:restpass -X POST http://mailman-core:8001/3.1/addresses/$2/verify #| python3 -m json.tool
      exit;;
    u)
      podman exec -it mailman-core curl --user restadmin:restpass -X POST http://mailman-core:8001/3.1/addresses/$2/unverify #| python3 -m json.tool
      exit;;
    l)
      podman exec -it mailman-core curl --user restadmin:restpass -X GET http://mailman-core:8001/3.1/addresses/$2 | python3 -m json.tool
      exit;;
    h)
      print_help
      ;;
    *)
      echo "invalid option: -$OPTARG"
      print_help
      ;;
    :)
      echo "Option -$OPTARG requires an argument."
      print_help
      ;;
  esac
done
