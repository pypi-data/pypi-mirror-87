#!/bin/sh

# Prerequisites:
# Environment variables TWINE_TOKEN_GITLAB and TWINE_TOKEN_PYPI must be set to the appropriate access tokens.

set -x
set -e

# set up prerequisites
python3 -m pip install build twine "keyrings.alt>=3.1"

# clean any previous build output, otherwise leftovers may be packaged into the new packages
rm -rf build src/inco_32.egg-info src/inco_32/errinco.py dist

# build packages
python3 -m build .

# upload
python3 -m twine check dist/*
# this may fail if the same version has already been uploaded (when called due to a tag push)
set +x
export TWINE_PASSWORD="$TWINE_TOKEN_GITLAB"
set -x
python3 -m twine upload --username buildmachine --repository-url https://gitlab.indel.ch/api/v4/projects/206/packages/pypi --verbose dist/* || true
# to PyPI only if it's a tag vX.Y.Z
if git describe --dirty --tags --match '*[0-9]*' | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+$'; then
	set +x
	export TWINE_PASSWORD="$TWINE_TOKEN_PYPI"
	set -x
	python3 -m twine upload --username __token__ --repository pypi --verbose dist/*
fi
