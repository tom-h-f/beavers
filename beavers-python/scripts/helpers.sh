#!/usr/bin/env zsh

function r() {
	SCRIPT_PATH="${0:A:h}"
	python3 "${SCRIPT_PATH}/run.py"
}

echo "You can now use 'r' to run the cli, via \`run.py\`"
