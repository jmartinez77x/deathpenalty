import requests, re
from bs4 import BeautifulSoup
import pandas as pd
import csv

def read_table(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup.find(lambda tag: tag.name == 'table')

def parse_table(url):
   table = read_table(url)
   return [[td.get_text(strip=True)
            if td.find("a") is None
            else url + td.find("a")["href"]
            for td in tr.find_all("td") if td.get_text(strip=True) is not u""]
            for tr in table.find_all("tr")]

def parse_statement(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    statements = [statement.text.strip() for statement in soup.findAll('p')]
    try:
        start = statements.index(u'Last Statement:')
    except:
        start = 0
    statements = [statements[i] for i in range(0, len(statements)) if i > start]
    return u''.join(statements)

def parse_details(url):
    global counter
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    tdcj_num = ""
    try:
        for statement in soup.find(text='TDCJ Number').parent.find_next_siblings():
            tdcj_num = statement.text.encode('utf-8').strip()
    except:
        tdcj_num = ""
    birth_date = ""
    try:
        for statement in soup.find(text='Date of Birth').parent.find_next_siblings():
            birth_date = statement.text.encode('utf-8').strip()
    except:
        birth_date = ""
    date_received = ""
    try:
        for statement in soup.find(text='Date Received').parent.find_next_siblings():
            date_received = statement.text.encode('utf-8').strip()
    except:
        date_received = ""
    received_age = ""
    try:
        for statement in soup.find(text='Age (when    Received)').parent.find_next_siblings():
            received_age = statement.text.encode('utf-8').strip()
    except:
        received_age = ""
    edu_level = ""
    try:
        for statement in soup.find(text='Education Level (Highest Grade Completed)').parent.find_next_siblings():
            edu_level = statement.text.encode('utf-8').strip()
    except:
        edu_level = ""
    statement5 = ""
    try:
        for statement in soup.find(text='Date of Offense').parent.find_next_siblings():
            statement5 = statement.text.encode('utf-8').strip()
    except:
        statement5 = ""
    offense_age = ""
    try:
        for statement in soup.find(text='Age (at the time    of Offense)').parent.find_next_siblings():
            offense_age = statement.text.encode('utf-8').strip()
    except:
        offense_age = ""
    gender = ""
    try:
        for statement in soup.find(text='Gender').parent.find_next_siblings():
            gender = statement.text.encode('utf-8').strip()
    except:
        gender = ""
    hair_color = ""
    try:
        for statement in soup.find(text='Hair Color').parent.find_next_siblings():
            hair_color = statement.text.encode('utf-8').strip()
    except:
        hair_color = ""
    height = ""
    try:
        for statement in soup.find(text='Height').parent.find_next_siblings():
            height = statement.text.encode('utf-8').strip()
    except:
        height = ""
    weight = ""
    try:
        for statement in soup.find(text='Weight').parent.find_next_siblings():
            weight = statement.text.encode('utf-8').strip()
    except:
        weight = ""
    eye_color = ""
    try:
        for statement in soup.find(text='Eye Color').parent.find_next_siblings():
            eye_color = statement.text.encode('utf-8').strip()
    except:
        eye_color = ""
    native_county = ""
    try:
        for statement in soup.find(text='Native County').parent.find_next_siblings():
            native_county = statement.text.encode('utf-8').strip()
    except:
        native_county = ""
    native_state = ""
    try:
        for statement in soup.find(text='Native State').parent.find_next_siblings():
            native_state = statement.text.encode('utf-8').strip()
    except:
        native_state = ""

    prior_occupation = ""
    try:
        for statement in soup.find(text='Prior Occupation').parent.find_next_siblings():
            prior_occupation = statement.nextSibling.encode('utf-8').strip()
    except:
        prior_occupation = ""
    prison_record = ""
    try:
        for statement in soup.find(text='Prior Prison Record').parent.find_next_siblings():
            prison_record = statement.nextSibling.encode('utf-8').strip()
    except:
        prison_record = ""
    incident_summary = ""
    try:
        for statement in soup.find(text='Summary of Incident').parent.find_next_siblings():
            incident_summary = statement.nextSibling.encode('utf-8').strip()
    except:
        incident_summary = ""
    coDefendants = ""
    try:
        for statement in soup.find(text='Co-Defendants').parent.find_next_siblings():
            coDefendants = statement.nextSibling.encode('utf-8').strip()
    except:
        coDefendants = ""
    victim_info = ""
    try:
        for statement in soup.find(text='Race and Gender of Victim').parent.find_next_siblings():
            victim_info = statement.nextSibling.encode('utf-8').strip()
    except:
        victim_info = ""

    counter = counter + 1
    print("Line Item: " + str(counter))
    f.writerow([tdcj_num,  birth_date,  date_received,  received_age,  edu_level,  statement5,  offense_age, gender,
                hair_color,  height,  weight, eye_color, native_county, native_state,
                prior_occupation, prison_record, incident_summary, coDefendants, victim_info])


counter = 0
columns = ['Execution #', 'Offender Information Link', 'Last Statement Link', 'Last Name',
              'First Name', 'TDCJ Number', 'Age', 'Execution Date', 'Race', 'County']

data = parse_table('http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html')
del data[0]
data = pd.DataFrame(data, columns = columns)
data.ix[:, (1,2)] = data.ix[:, (1,2)].applymap(lambda x: re.sub('dr_executed_offenders.html', '', x))

f = csv.writer(open("offender_details.csv", "w"))
f.writerow(["TDCJ Number","Date of Birth", "Date Received", "Age when Received", "Education Level", "Date of Offense",
            "Age at Offense", "Gender", "Hair Color", "Height", "Weight", "Eye Color", "Native County",
            "Native State", "Prior Occupation", "Prior Prison Record", "Summary of Incident", "Co-Defendents","Victim Information"])

data['Statement Text'] = data['Last Statement Link'].map(lambda x: parse_statement(x))
data['Offender Information Link'].map(lambda x: parse_details(x))
# data['offender_information'].map(lambda x: parse_details('https://www.tdcj.state.tx.us/death_row/dr_info/wardadam.html'))

data.to_csv('TDCJ_with_statements.csv', index=False, encoding='utf-8')