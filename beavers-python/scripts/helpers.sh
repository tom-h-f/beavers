#!/usr/bin/env zsh

SCRIPT_PATH="${0:A:h}"

function pr() {
	python3 "${SCRIPT_PATH}/../run.py" "$@"
}

function pypath() {
	export PYTHONPATH="${SCRIPT_PATH}/lib/core/.venv/"
}

function repl() {
	(cd "${SCRIPT_PATH}/../lib/core"  && uv run python)
}

function kiwf()  {
	pkill -f "${SCRIPT_PATH}/../.venv/bin/python3 main.py"
}

echo "You can now use:"
echo "\t'pr' to run the cli, via \`run.py\`"
echo "\t'repl' to run a REPL with the project's dependencies"
echo "\t'pypath' to change your pythonpath to be for the 'core' package. TODO allow doing this for the other packages/venvs"
echo "\t'kiwf' to kill the app if unresponvive to ctrl+c for some reason"
