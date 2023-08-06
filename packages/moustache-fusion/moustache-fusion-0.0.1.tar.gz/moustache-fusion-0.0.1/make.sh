#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

__FILE__="$(realpath "$0")"
__SCRIPT__="$(basename "${__FILE__}")"
__ROOT__="$(dirname "${__FILE__}")"
__ROOT__="$(realpath "${__ROOT__}")"

COVERAGE_DIR="${__ROOT__}/tests/out/coverage"
DEBUG=0

usage()
{
    printf "NAME\n"
    printf "  %s\n" "${__SCRIPT__}"
    printf "\nDESCRIPTION\n"
    printf "  Utilities for moustache_fusion development.\n"
    printf "\nSYNOPSIS\n"
    printf "  %s [OPTION] [COMMAND]\n" "${__SCRIPT__}"
    printf "\nCOMMANDS\n"
    printf "  clear\t\tClear coverage, pytest and python cache\n"
    printf "  coverage\tRun tests with code coverage, report written in ${COVERAGE_DIR}\n"
    printf "  quality\tStatic code alalysis with flake8\n"
    printf "  tests\t\tRun tests\n"
    printf "\nOPTIONS\n"
    printf "  -d|--debug\tTrace commands before executing them (set -o xtrace)\n"
    printf "  -h|--help\tDisplay this help text and exit\n"
    printf "\nEXEMPLES\n"
    printf "  %s -h\n" "${__SCRIPT__}"
}

main()
{
    (
        opts=$(getopt --longoptions debug,help -- d "$@") || (usage >&2 ; exit 1)
        eval set -- "$opts"
        while true; do
            case "${1}" in
                -d|--debug)
                    DEBUG=1
                    shift
                    ;;
                -h|--help)
                    usage
                    exit 0
                    ;;
                --)
                    shift
                    break
                    ;;
            esac
        done

        if [ $DEBUG -eq 1 ]; then
            set -o xtrace
        fi

        case "${1:-}" in
            clear)
                echo "Clearing coverage, pytest and python cache..."
                rm -rf ${__ROOT__}/.coverage ${__ROOT__}/.pytest_cache ${__ROOT__}/build ${__ROOT__}/dist ${__ROOT__}/*.egg-info
                find ${__ROOT__} -type d -iname "__pycache__" -exec rm -rf "{}" \; 2>/dev/null
                exit $?
            ;;
            coverage)
                coverage run --source=${__ROOT__}/moustache_fusion -m pytest -vv ${__ROOT__}/tests \
                && coverage html --directory=${COVERAGE_DIR} \
                && chmod -R 777 ${__ROOT__}/tests/out
                exit $?
            ;;
            quality)
                flake8
                exit $?
            ;;
            tests)
                pytest -vv /app/tests \
                && chmod -R 777 ${__ROOT__}/tests/out
                exit $?
            ;;
            --)
                shift
            ;;
            *)
                >&2 usage
                exit 1
            ;;
        esac

        exit 0
    )
}

main "$@"
