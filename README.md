<h1>Python script to analyze EATON IPM UPS Logs</h1>


Export the logs from EATON IPM Manager in CSV format

Execute the python script with logs filename as argument

<h3>Linux:</h3>

**ups_analyzer -f filename.csv**

Arguments 

-f | --filename : Input Logs filename with extention

<h3>Windows:</h3>

**C:\Python27\python.exe script_location\ups_analyzer.py --filename filename.csv**

Arguments 

-f | --filename : Input Logs filename with extention


<h2>Dependencies</h2>

packages:

    1. tqdm

Installation Procedure

pip install tqdm
