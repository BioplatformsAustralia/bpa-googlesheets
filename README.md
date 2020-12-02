# bpa-googlesheets

Download data from googlesheets API call with given credentials.json file and googlesheets ID.

Just uses organization ID from command-line, atm.
## Install:
```
(Install Python3)
(cd into this repo)
pip install -r requirements.txt
python setup.py develop
```
## Pre-run/Env setup
```
. ~/.virtual/bpa-googlesheets/bin/activate
source <<your bpa.env file>>
```
## Help:
```
bpa-googlesheets --help
```

## Example run:
```
bpa-googlesheets -i 19ZTNrCr_TRiMB-aAJ007-F-z -c /opt/Bioplatforms.json
```


