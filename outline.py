from urllib import response
from flask import Flask
from pip._vendor import requests
from bs4 import BeautifulSoup
import json
from flask import render_template

app = Flask(__name__)
@app.route("/")
@app.route('/index')


def displayJobDetails():
    
    response = requests.get('https://raw.githubusercontent.com/DracTown/chum-bucket_P8/main/pythonBeautifulSoup-main/jobDetails.json')
    responseJSON=response.json()
    temp={
        "Company Name":{responseJSON[0]['Company Name']},
        "JOB Description":{responseJSON[0]['JOB Description']},
        "JOB Salary":{responseJSON[0]['JOB Salary']},
        "JOB Title":{responseJSON[0]['JOB Title']}

    }
    return render_template('index.html', temp = responseJSON)
app.run(host='localhost', debug=True)

jobResults = []
def getJobList(role, location):
    # Complete the missing part of this function here
    jobResults.clear()
    url = "https://www.indeed.com/jobs?q=" + role + "&l=" + location
    payload = {}
    headers = {
        'Cookie': 'CTK=1fvqtabopq05p800; INDEED_CSRF_TOKEN=zObWlBjnc0oLVAS3aidx8lvSAZOgVukr; JSESSIONID=627D0DD3248349B13DE876D0883448E6; PREF="TM=1649096863522:L=' + location + '"; RQ="q=' + role + '&l=+' + location + '&ts=1649703016594:q=+' + role + '+&l=+' + location + '&ts=1649699917805&pts=1649129121573"; UD="LA=1649703016:LV=1649127002:CV=1649698419:TS=1649096863:SG=8138e1e8a2add6bf3bc2dced46849fdb"; indeed_rcc="PREF:CTK:UD:RQ"; jaSerpCount=2'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    for job in soup.find_all('div', attrs={'class': 'slider_container css-11g4k3a eu4oa1w0'}):
        jobTitle = job.find('h2', class_='jobTitle')
        companyName = job.find('span', class_='companyName')
        jobDescription = job.find('div', class_='job-snippet')
        salary = job.find('div', class_='salary-snippet-container')
        if salary:
            salary = salary.text
        else:
            salary = "No Salary Listed"
            
        jobs = [jobTitle.text, companyName.text, jobDescription.text, salary]
        jobResults.append(jobs)

def saveDataInJSON(jobDetails):
    # Complete the missing part of this function here
    jsonStr = json.dumps(jobDetails)
    parse = json.loads(jsonStr)
    with open('jobDetails.json', 'w', encoding = 'utf-8') as jdjs:
        jdjs.write(json.dumps(parse, indent = 4, sort_keys = True)) 
    print("Saving data to JSON")        
    
    
#main function
def main():
    # Write a code here to get job location and role from user e.g. role = input()
    print("Enter role you want to search")
    role = input()
    # Complete the missing part of this function here
    print("Enter the Location to search")
    location = input()
    getJobList(role,location)
    saveDataInJSON(jobResults)
if __name__ == '__main__':
    main()