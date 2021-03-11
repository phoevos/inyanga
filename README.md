# Inyanga

A simple app for the mining and storing of metadata from the Diavgeia OpenDataAPI.  
Built for the NTUA-ECE course 'Analysis and Design of Information Systems'.

* `collect.py`: The main function for communicating with the Diavgeia API and storing documents
* `dict2akn.py`: Function that takes a dictionary as input and converts it to AkomaNtoso-like format
* `cli.py`: Client built with PyInquirer to:

  1. Fetch metadata from Diavgeia and store them in AkomaNtoso-like format using MongoDB
  2. View locally stored documents
  3. Search by ADA, Date or any text field
  4. Export locally stored documents as .akn or .json files

## To run

1. `python server.py` to initiate the server
2. `python cli.py` to start the client

You will need a running MongoDB (created using v4.4.4) instance, as well as the pip dependencies installed first.  
Run `./dependencies.sh` to install dependencies.
