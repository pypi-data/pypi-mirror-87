# Swift CCF

## Installation

No dependencies

Download from pip:

pip install Swift-CCF-Kravchuk

## Usage

python exec/main.py [-v] [-fx] -(f|d|p) directory/filename

OR (if downloaded from pip)

k-swift-ccf [-v] [-fx] -(f|d|p) directory/filename

-f specify path to a php file to be verified and/or formatted
-d specify path to a directory with php files to be verified and/or formatted
-p specify path to a project directory with php files to be verified and/or formatted

(Note: -d key doesn't check folders inside recursively)

-v specify this key with no arguments to print warnings and errors in scanned code in log file

-fx specify this key with no arguments to modify your code and create log file with changes
