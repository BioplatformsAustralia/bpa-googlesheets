# bpa-googlesheets

Download data from googlesheets API call with given credentials.json file and googlesheets ID.

Just uses organization ID from command-line, atm.

## With docker:

### Install:
```
docker build -t bioplatformsaustralia/bpagooglesheets .
```

### Example run:
In the following example the local directory 'data' is used to hold the credentials key and to write output:
```
docker run -it --rm -v /data/googlesheets:/data bioplatformsaustralia/bpagooglesheets:bioplatforms bpa-googlesheets -i 19ZTNrCr -c /data/Bioplatforms-googlesheet-credentials.json -t /data/output/summary_table_data_path.json
```

## With command-line:

### Install:
```
(Install Python3)
(cd into this repo)
pip install -r requirements.txt
python setup.py develop
```
### Pre-run/Env setup
```
. ~/.virtual/bpa-googlesheets/bin/activate
source <<your bpa.env file>>
```

### Example run:
```
bpa-googlesheets -i 19ZTNrCr_TRiMB-aAJ007-F-z -c /opt/Bioplatforms.json
```

## Help:
```
bpa-googlesheets --help
```




