import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


#GLOBAL VARIABLES  ENTER YOUR INFO BELOW
######################################################################################################################################
resume_global = 'yourResumeName.pdf'

email_user_global = ['emailAccount1@example.com', 'emailAccount2@example.com', 'emailAccount3@example.com']

email_password_global = ['email1Password', 'email2Password', 'email3Password']

email_subject_global = 'Email Subject Line'

def printBody(name):
    string = '''Insert email body here'''
    return string
########################################################################################################################################
#
#          In your gmail account turn on less secure app access before running
#          Set Up Filters
#
########################################################################################################################################
#          run webScrape(URL,site,keyword,pages) to add companies to email from a database
#          run hyperCon() to send emails
#
########################################################################################################################################

# Finding potential emails...
def nonamelist(adress):
    ads = ['employment' + adress, 'info' + adress,'hire' + adress,'staff' + adress,'hiring' + adress,'hello' + adress,'contact' + adress,'jobs' + adress,'careers' + adress,'hr' + adress,'mail' + adress, 'join' + adress, 'business' + adress,'media' + adress]
    return ads

def extralist(first, last, adress):
    ads = [first + last + adress,first + '.' + last + adress,last + first + adress,first[0] + last + adress,last + adress,first + adress,last + '.' + first + adress,first + last[0] + adress,first[0] + last[0] + adress,last[0] + first[0] +  adress]
    return ads

# Sends an email from your email account
def sendEmail(email_user, email_password, email_send, subject, filename, body):

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    msg.attach(MIMEText(body,'plain'))

    attachment  =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    
    server.login(email_user,email_password)

    server.sendmail(email_user,email_send,text)
    server.quit()

# Use to contact a company with a single email account. Used when the user doesn't have a contact name.
def contact(website, company):
    email_send = nonamelist(website)
    companyEdit = firstCap(company)
    body = printBody(companyEdit)
    for i in email_send:
        if searchInCompaniesEmailed(i):
            print(i + ' in companiesEmailed')
            
        else:
            while True:
                try:
                    sendEmail(email_user_global, email_password_global, i, email_subject_global, resume_global, body)
                except Exception :
                    continue
                addToCompaniesEmailed(i)
                break

# Use to contact a company with a single email account. Used when the user wants to input a contact name.
def contactName(website, company, first, last):
    email_send = extralist(first,last,website)
    companyEdit = firstCap(company)
    body = printBody(companyEdit)
    for i in email_send:
        if searchInCompaniesEmailed(i):
            print(i + ' in companiesEmailed')
            
        else:
            while True:
                try:
                    sendEmail(email_user_global, email_password_global, i, email_subject_global, resume_global, body)
                except Exception :
                    continue
                addToCompaniesEmailed(i)
                break

# Use to contact companies from more than one account.
def contactWithEmail(emailAccount, emailPassword, website, company):

    email_send = nonamelist(website)
    companyEdit = firstCap(company)
    body = printBody(companyEdit)
    for i in email_send:
        if searchInCompaniesEmailed(i):
            print(i + ' in companiesEmailed')
            
        else:
            while True:
                try:
                    sendEmail(emailAccount, emailPassword, i, email_subject_global, resume_global, body)
                except Exception :
                    continue
                addToCompaniesEmailed(i)
                break

# Makes sure names are capitalized
def firstCap(name):
    return name[0].upper() + name[1:]

# Make sure the company hasn't already been emailed. Avoids double emailing a company.
def searchInCompaniesEmailed(email):
    searchfile = open("companiesEmailed.txt", "r")
    for line in searchfile:
        if email.lower() in line: 
            searchfile.close()
            return True
    searchfile.close()
    return False

# Adds a company to the companiesEmailed.txt file.
# Updates the txt file so the user knows what companies they have contacted.
# Avoids double emails.
def addToCompaniesEmailed(email):
    file_object = open('companiesEmailed.txt', 'a')
    file_object.write(" ")
    file_object.write(email)
    file_object.write(" ")
    file_object.close()

    
# Takes an input of a company name.
# Searches google for that company.
# Returns the company website URL and the name of the company.
def linkChoose(name):
    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found") 

    query = name
    forCon = []
    for j in search(query, tld="co.in", num=5, stop=5, pause=2): 
        jMid = middle(j)
        if notBadSite(jMid):
            forCon = [jMid, name]
            return forCon
        else:
            return forCon

# Checks a list of common missearches that appear on google.
# Avoids emailing all companies listed in this txt file.
def notBadSite(adress):
    searchfile = open("badSites.txt", "r")
    for line in searchfile:
        if adress in line: 
            searchfile.close()
            return False
    searchfile.close()
    return True

# Removes a company from the bottom of the companiesToEmail.txt file
def popTxt():
    fd=open("companiesToEmail.txt","r")
    d=fd.read()
    fd.close()
    m=d.split("\n")
    pop = m[-1]
    s="\n".join(m[:-1])
    fd=open("companiesToEmail.txt","w+")
    for i in range(len(s)):
        fd.write(s[i])
    fd.close()
    if pop == '':
        return 'Empty Con'
    else:
        return pop

# finds the first . in a URL.
# Helper function for middle().
def getDotIndex(s):
    return s.find('.')

# finds the first / in a URL after the first .
# Helper function for middle().
# Removes extra characters from the URL after .com, .org, etc.
def getSlashIndex(s):
    return s.find('/', getDotIndex(s),len(s)-1)

# finds the // in a URL that is often right before the company name.
# Helper function for middle().
def getDoubleSlash(s):
    return s.find('//')

# Uses the above helper functions to extract the company name out of the company's website URL.
# Aids in finding the companies email.
def middle(s):
    if s.find('www.') == -1:
        middle = s[getDoubleSlash(s)+2:getSlashIndex(s)]
    else:
        middle = s[getDotIndex(s)+1:getSlashIndex(s)]
    return middle

# Sends an email to 28 companies from the companiesToEmail text file
# Removes those companies from the companiesToEmail text file
def autoCon():
    counter = 0
    while counter != 28:
        first = popTxt()
        url = linkChoose(first)
        if first == 'Empty Con':
            return 'Empty Con'
        elif (len(url) != 0) and (searchInCompaniesEmailed(url[0]) != True):
            contact('@' + url[0], url[1]) 
            counter +=1

# Same as autoCon(), but allows the email to specify which email account they want to send from.
def autoConWithEmail(emailAccount, emailPassword):
    counter = 0
    while counter != 28:
        first = popTxt()
        url = linkChoose(first)
        if first == 'Empty Con':
            return 'Empty Con'
        elif (len(url) != 0) and (searchInCompaniesEmailed(url[0]) != True):
            contactWithEmail(emailAccount, emailPassword, '@' + url[0], url[1]) 
            counter +=1

# Sends emails to 28 companies from each email that the user listed at the top of the file.
def hyperCon():
    for i in range(0,len(email_user_global)):
        autoConWithEmail(email_user_global[i], email_password_global[i])
        print('autoCon ' + str(i) + 'finished running')


'''''''''''''''
WEB SCRAPING
'''''''''''''''

import requests
from bs4 import BeautifulSoup

# Adds a company to companiesToEmail.txt file
def addScraper(email):
    file_object = open('companiesToEmail.txt', 'a')
    file_object.write(email)
    file_object.write("\n")
    file_object.close()

# Scrapes company names off of Monster Jobs site.
# User inputs the URL and search keyword to find jobs in their field.
def scrapeMonster(URL, keyword):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='ResultsContainer')
    if keyword == '':
        job_elems = results.find_all('section', class_='card-content')
    else:
        job_elems = results.find_all('h2',
                                string=lambda text: keyword in text.lower())
    for job_elem in job_elems:
        company_elem = job_elem.find('div', class_='company')
        if None in (company_elem):
            continue
        addScraper(company_elem.text.strip())

# Scrapes company names off of Thomas Net.
# User inputs URL, keyword, and the number of pages of companies they want scraped.
def scrapeThomas(URL, keyword,pages):
    for i in range(pages):
        page = requests.get((URL + '&pg=' + str(i +1)))
        results = BeautifulSoup(page.content, 'html.parser')
        if keyword == '':
            job_elems = results.find_all("h2", {"class":"profile-card__title"})
        else:
            job_elems = results.find_all('h2',
                                    string=lambda text: keyword in text.lower())
        for job_elem in job_elems:
            company_elem = job_elem.find('a')
            if None in (company_elem):
                continue
            addScraper(company_elem.text.strip())
    
# Scrapes Y Combinator.
# User inputs the URL and a keyword
def scrapeYComb(URL, keyword):
    page = requests.get(URL)
    results = BeautifulSoup(page.content, 'html.parser')
    if keyword == '':
        job_elems = results.find("a", {"target":"_blank"})
    else:
        job_elems = results.find_all('h2',
                                string=lambda text: keyword in text.lower())
    for job_elem in job_elems:
        company_elem = job_elem.find('td', {"class":"name"})
        if None in (company_elem):
            continue
        addScraper(company_elem.text.strip())

# Scrapes Indeed.
# User inputs the URL, keyword, and how many pages of companies they want scraped.
def scrapeIndeed(URL, keyword, pages):
    for i in range(pages):
        page = requests.get(URL + "&start=" + str(i*10))
        results = BeautifulSoup(page.content, 'html.parser')
        if keyword == '':
            job_elems = results.find_all("span", {"class":"company"})
        else:
            job_elems = results.find_all('h2',
                                    string = lambda text: keyword in text.lower())
        for job_elem in job_elems:
            company_elem = job_elem
            if None in (company_elem):
                continue
            addScraper(company_elem.text.strip())

# Scrapes company names from either thomas net, indeed, or monster, depending on the users input
def webScrape(URL,site,keyword,pages):
    if site.lower() == 'thomas':
        scrapeThomas(URL, keyword,pages)
    elif site.lower() == 'indeed':
        scrapeIndeed(URL, keyword, pages)
    elif site.lower() == 'monster':
        scrapeMonster(URL, keyword)
