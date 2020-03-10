#!/bin/bash

host_group=all
node_file=nodes.yml

function die { echo "$1"; exit 1; }
function print_help {
echo "Usage: $0 [--group] [--help] COMMAND WORKDIR

    --help                      show this help and exit
    --group                     specify the ansible group"
    exit 0
}

function check_argnum {
    argnum=$(($# - 1))
    [[ "$1" -eq "$argnum" ]] || die "incorrect argnum: got $argnum, $1 expected"
}

function _start {
    workdir="$1"
    if [[ -a "$workdir" ]]; then
        die "$workdir already exists"
    fi
    mkdir -p "$workdir"
    cp "$node_file" "$workdir/nodes.yml"
    cp -r group_vars/ "$workdir"
    ansible-playbook -i "$workdir/nodes.yml" ansible/start.yml --extra-vars "run_id=$workdir host_group=$host_group"
}

function _stop {
    workdir=${1%/}
    [[ -f "$workdir/nodes.yml" ]] || die "invalid id"
    ansible-playbook -i "$1/nodes.yml" ansible/stop.yml --extra-vars "run_id=$workdir host_group=$host_group"
}

function _check {
    workdir=${1%/}
    [[ -f "$workdir/nodes.yml" ]] || die "invalid id"
    ansible-playbook -i "$1/nodes.yml" ansible/check.yml --extra-vars "run_id=$workdir host_group=$host_group"
}

function _fetch {
    workdir=${1%/}
    [[ -f "$workdir/nodes.yml" ]] || die "invalid id"
    ansible-playbook -i "$1/nodes.yml" ansible/fetch.yml --extra-vars "run_id=$workdir host_group=$host_group"
}

function _reset {
    workdir=${1%/}
    ansible-playbook -i "$1/nodes.yml" ansible/reset.yml --extra-vars "run_id=$workdir host_group=$host_group"
}

getopt --test > /dev/null
[[ $? -ne 4 ]] && die "getopt unsupported"

SHORT=
LONG='\
group:,\
nodes:,\
help'

PARSED=$(getopt --options "$SHORT" --longoptions "$LONG" --name "$0" -- "$@")
[[ $? -ne 0 ]] && exit 1
eval set -- "$PARSED"

while true; do
    case "$1" in
        --group) host_group="$2"; shift 2;;
        --help) print_help; shift 1;;
        --nodes) node_file="$2"; shift 2;;
        --) shift; break;;
        *) die "internal error";;
    esac
done
cmd="$1"
shift 1
case "$cmd" in
    start) check_argnum 1 "$@" && _start "$1" ;;
    stop) check_argnum 1 "$@" && _stop "$1" ;;
#    status) check_argnum 1 "$@" && status_all "$1" ;;
    check) check_argnum 1 "$@" && _check "$1" ;;
    fetch) check_argnum 1 "$@" && _fetch "$1" ;;
#    wait) check_argnum 1 "$@" && wait_all "$1" ;;
    reset) check_argnum 1 "$@" && _reset "$1" ;;
#    exec) check_argnum 2 "$@" && exec_all "$1" "$2" ;;
    *) print_help ;;
esac
