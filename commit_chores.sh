#!/bin/bash

# Runs some chores that are to be executed before every commit.
# This script will be run through a pre-commit hook. Making a script to avoid
# having to make multiple hooks for some background chores.

# Use poetry to fetch the latest dev requirements and dump them - prevents me from
# having to do this manually, and ensures that I don't end up forgetting this.

poetry export --dev --output dev-requirements.txt

# Likewise, fetching the non-dev requirements and dumping them too.
poetry export --output requirements.txt

# Adding both these files to git staging - will have no effect if there are no changes,
# and if there are any changes, they'll be added to staging and be a part of the next
# commit
git add dev-requirements.txt
git add requirements.txt

# For the same reason, adding poetry lock file, as well.
git add poetry.lock
