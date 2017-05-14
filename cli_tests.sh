#!/bin/bash

set -ev

###############################################################################

nbmerge \
	tests/fixtures/1_Intro.ipynb \
	tests/fixtures/2_Middle.ipynb \
	tests/fixtures/3_Conclusion.ipynb \
	-o cli_test.ipynb

cmp cli_test.ipynb tests/fixtures/_gold.ipynb

rm cli_test.ipynb

###############################################################################

nbmerge \
	tests/fixtures/1_Intro.ipynb \
	tests/fixtures/2_Middle.ipynb \
	tests/fixtures/3_Conclusion.ipynb \
	> cli_test.ipynb

cmp cli_test.ipynb tests/fixtures/_gold.ipynb

rm cli_test.ipynb
