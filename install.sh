#!/usr/bin/env bash
set -ex

readonly SYSTEMD_DIR="${HOME}/.config/systemd/user"
readonly OVERRIDE_DIR="${SYSTEMD_DIR}/yt-live.service.d"
readonly OVERRIDE_CONF="${OVERRIDE_DIR}/override.conf"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

function main() {
    pushd "${SCRIPT_DIR}/yt-live" || return 1
    poetry build -f wheel
    pip3 install "dist/$(ls dist | grep whl)"
    popd || return 0

    mkdir -p "${HOME}/.config/systemd/user"
    cp "${SCRIPT_DIR}/systemd/yt-live.service" "${SYSTEMD_DIR}/"

    if [[ ! -f "${OVERRIDE_CONF}" ]]; then
        read -p "Please input API Key: " API_KEY
        read -p "Please input the path of client_secret.json: " CLIENT_SECRETS_FILE
        read -p "Please input the Discord webhook URL: " DISCORD_WEBHOOK_URL

        mkdir -p "${OVERRIDE_DIR}"
        cat <<EOF >"${OVERRIDE_CONF}"
[Service]
Environment=API_KEY=${API_KEY}
Environment=CLIENT_SECRETS_FILE=${CLIENT_SECRETS_FILE}
Environment=DISCORD_WEBHOOK_URL=${DISCORD_WEBHOOK_URL}
EOF
    fi

    systemctl --user daemon-reload

    mkdir -p "${HOME}/.local/bin"
    cp "${SCRIPT_DIR}/bin/yt-live-ctl" "${HOME}/.local/bin/"
}

main "$@" || (echo "Failed to install" 1>&2 && return 1)
