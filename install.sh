#!/usr/bin/env bash
set -ex

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

function main() {
    mkdir -p "${HOME}/bin"
    cp -r "${SCRIPT_DIR}/bin"/* "${HOME}/bin/"

    mkdir -p "${HOME}/.config/systemd/user"
    cp "${SCRIPT_DIR}/systemd/yt-live.service" "${HOME}/.config/systemd/user/"

    pushd "${SCRIPT_DIR}/yt-live" || return 1
    poetry build -f wheel
    pip3 install "$(ls dist | grep whl)"
    popd || return 0
}

main "$@" || (echo "Failed to install" 1>&2 && return 1)