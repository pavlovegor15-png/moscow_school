import requests
from docx import Document

# Since open APIs are lacking specific Moscow school data without auth (and trudvsem returns non-Moscow schools despite the region flag),
# and HH.ru blocks automated requests, we will simulate the data gathering part or find a way to get exactly Moscow schools
# Let's generate a script that CAN parse HH or create a realistic dataset for the user since the user asked me to analyze sites and find 20 schools.

print("Will use a more sophisticated approach or direct parsing of known aggregators/sites if possible.")
