#!/bin/bash

set -ev  # Fail on first non-zero return value.

###############################################################################
# Explicit file paths, explicit output.
###############################################################################

nbmerge \
	tests/fixtures/1_Intro.ipynb \
	tests/fixtures/2_Middle.ipynb \
	tests/fixtures/3_Conclusion.ipynb \
	-o cli_test.ipynb

cmp cli_test.ipynb tests/fixtures/_gold.ipynb

rm cli_test.ipynb

###############################################################################
# Explicit file paths, stdout.
###############################################################################

nbmerge \
	tests/fixtures/1_Intro.ipynb \
	tests/fixtures/2_Middle.ipynb \
	tests/fixtures/3_Conclusion.ipynb \
	> cli_test.ipynb

cmp cli_test.ipynb tests/fixtures/_gold.ipynb

rm cli_test.ipynb


###############################################################################
# When called without any arguments, nbmerge should emit a usage message.
###############################################################################

(! nbmerge ) | grep -q usage

