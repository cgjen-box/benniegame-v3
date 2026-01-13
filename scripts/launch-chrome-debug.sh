#!/bin/bash
# Launch Chrome in debug mode with persistent profile for Ludo.ai automation
#
# Usage:
#   ./scripts/launch-chrome-debug.sh                    # Opens Chrome (blank)
#   ./scripts/launch-chrome-debug.sh https://ludo.ai   # Opens Chrome at Ludo.ai
#
# The debug profile maintains login sessions and preferences between runs.
# Chrome DevTools MCP can connect to localhost:9222 for browser automation.

CHROME_BINARY="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE_DIR="/Users/user289321/chrome-debug-profile"
DEBUG_PORT=9222

# Check if Chrome is already running on debug port
if curl -s "http://localhost:${DEBUG_PORT}/json" > /dev/null 2>&1; then
    echo "Chrome is already running in debug mode on port ${DEBUG_PORT}"
    echo "Connect via: http://localhost:${DEBUG_PORT}/json"
    exit 0
fi

echo "Launching Chrome in debug mode..."
echo "  Profile: ${PROFILE_DIR}"
echo "  Debug port: ${DEBUG_PORT}"
echo "  Connect via: http://localhost:${DEBUG_PORT}/json"

"${CHROME_BINARY}" \
    --remote-debugging-port=${DEBUG_PORT} \
    --user-data-dir="${PROFILE_DIR}" \
    "$@" &

echo "Chrome launched. PID: $!"
