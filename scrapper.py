# Author - Aman Chourasiya
# This menu-driven application extracts data of companies from clutch.co

# please install all dependencies using this command-  pip install -r requirements.txt

# make sure you have python3 installed in your system

# changing things now and then

# it is alpha branch now

import requests
import csv
import time
from tqdm import tqdm
from bs4 import BeautifulSoup as BS


headersT = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"}
# headersT is a dictionary which conveys information to the web server regarding the source of request
server_eror="Access Denied by server. Quitting.."

path_dictionary={}
supported_domains=[]
parser="html.parser"
not_avai="Not Available"

def populate_domains_links(): # function to map domains to their links
    path_dictionary['Mobile App Development']='https://clutch.co/directory/mobile-application-developers'
    path_dictionary['Web Development']='https://clutch.co/web-developers'
    path_dictionary['Software Development']='https://clutch.co/developers'
    path_dictionary['Artificial Intelligence']='https://clutch.co/developers/artificial-intelligence'
    path_dictionary['Blockchain']='https://clutch.co/developers/blockchain'
    path_dictionary['Social Media Marketing']='https://clutch.co/agencies/social-media-marketing'
    path_dictionary['Digital Marketing']='https://clutch.co/agencies/digital-marketing'
    path_dictionary['Web Design']='https://clutch.co/web-designers'
    path_dictionary['Graphic Design']='https://clutch.co/agencies/graphic-designers'
    path_dictionary['Logo Design']='https://clutch.co/agencies/logo-designers'

    supported_domains.append('Mobile App Development')
    supported_domains.append('Web Development')
    supported_domains.append('Software Development')
    supported_domains.append('Artificial Intelligence')
    supported_domains.append('Blockchain')
    supported_domains.append('Social Media Marketing')
    supported_domains.append('Digital Marketing')
    supported_domains.append('Web Design')
    supported_domains.append('Graphic Design')
    supported_domains.append('Logo Design')


def hourratehandler(data): # function to show less than operator
    if '&lt;' in data.text:
        return data.text.split(" ", 1)[1]
    return data.text


def getcontact(url): # function to obtain contact number of the company
    cnumber=None
    time.sleep(0.2)
    with requests.Session() as session2:
        session2.headers.update(headersT)
        t = session2.get(url)
        if(t.status_code!=200):
            print(server_eror)
            exit()
        try:
            cnumber = BS(t.content, features=parser).find(class_='quick-menu-details').find('a').string.strip()
        except Exception as _:
            return not_avai

    v=None
    try:
        v = int(cnumber)
    except Exception as _:
        v=cnumber
    return v


def getlink(url): # function to get link to the website in desired format
    for i in range(len(url)):
        if(url[i]=='?'):
            return url[:i]
    return url


def getlargestpagenumber(root):
    try:
        num=root.find("nav").find("ul", class_=["pagination justify-content-center"]).find("li",class_=["page-item last"]).find('a')['data-page']
    except Exception as _:
        return 1
    # print(num)
    return int(num)


# defining few selectors for DOM parsing
selector1="provider-info col-md-10"
selector2="col-md-3 provider-info__details"
selector3="row provider-info--content"
selector4="list-item custom_popover"


populate_domains_links() # mapping domains to their links in clutch.co

# Application Menu
border="|                                     |"
Menu=[
    " _____________________________________",
    "|     List of Domains Supported       |",
    "| ----------------------------------- |",
    "|  1. Mobile App Development          |",
    border,
    "|  2. Web Development                 |",
    border,
    "|  3. Software Development            |",
    border,
    "|  4. Artificial Intelligence         |",
    border,
    "|  5. Blockchain                      |",
    border,
    "|  6. Social Media Marketing          |",
    border,
    "|  7. Digital Marketing               |",
    border,
    "|  8. Web Design                      |",
    border,
    "|  9. Grapphic Design                 |",
    border,
    "|  10. Logo Design                    |",
    "|_____________________________________|\n",
    " ______________________________________________",
    "| Instructions for providing input -           |",
    "|----------------------------------------------|",
    "| If you want to choose a single domain, enter |",
    "| its number as input.                         |",
    "|                                              |",
    "| If you want to choose multiple domains,      |",
    "| enter each of their numbers space separated. |",
    "| For example, if you want to choose           |",
    "| Web Development and Blockchain, Enter- 2 5   |",
    "|______________________________________________|\n"
]

for i in Menu: print(i)

domains=input("Enter the domain(s) you want to choose: ").strip().split()
choosen_domains=[]
for i in domains:
    try:
        if(int(i)>10 or int(i)<1):
            print("Please enter valid number. Exiting..")
            exit()
        choosen_domains.append(int(i)-1)
    except TypeError:
        print("Please enter valid number. Exiting program..")
        exit()

# corner cases
if(len(choosen_domains)==0):
    print("Please enter atleast one domain. Quitting..")
    exit()
else:
    print("\nChoosen Domains-\n")
    for i in choosen_domains:
        print(supported_domains[i])

# Taking number of companies required as input
num_companies=None
try:
    menu2=[
    " ______________________________________________",
    "| Data of how many companies do you want from  |",
    "| each domain choosen by you?                  |",
    "| For example if you want data of 400 companies|",
    "| from each of the domains choosen, enter 400. |",
    "|______________________________________________|\n"
    ]
    for i in menu2: print(i)
    print()
    num_companies=int(input("Enter a single number: "))
except TypeError:
    print("Invalid Input. Quitting..")
    exit()

if(num_companies<=0 or num_companies==None):
    print("Please enter positive integer. Quitting..")
    exit()

# Fields in the csv file
fields=['Domain','Company','Website','Location','Contact','Rating','Review Count','Hourly Rate','Min Project Size','Employee Size']

# csv file initialization
filename = "company_data"+str(int(time.time()))+".csv"
csvfile=open(filename,'w')
csvwriter=csv.writer(csvfile)
csvwriter.writerow(fields) 

blcok=0
# starting a session
with requests.Session() as session:
    session.headers.update(headersT)

    # collecting data for each domain
    for index in choosen_domains:

        # progress bar creation
        print("\nCollecting data of companies involved in "+supported_domains[index]+"...\nProgress Bar..\n")
        pbar = tqdm(total=num_companies, position=0, leave=True)
        print()

        url_main=path_dictionary[supported_domains[index]]
        time.sleep(0.2)
        th = session.get(url_main) # opening the domain site in clutch.co
        if(th.status_code!=200):
            print(server_eror)
            exit()
        soup = BS(th.text, features=parser)

        root=soup.find("body").find("main", class_=["directory_wrap"]).find("section", class_=["container"])
        num_pages=getlargestpagenumber(root) # Maximum number of pages

        count_companies=0 # Keeps count of companies collected so far
        page_index=0 # Current page index in the site

        while(page_index<=num_pages and count_companies<num_companies):

            add_on="?page="+str(page_index) # specifying page number in url
            page_index+=1

            url=url_main+add_on
            time.sleep(0.2)
            th = session.get(url) # load the corresponding page
            if(th.status_code!=200):
                print(server_eror)
                exit()
            soup = BS(th.text, features=parser)

            root=soup.find("body").find("main", class_=["directory_wrap"]).find("section", class_=["container"])
            
            # list of all the companies in the current page
            list_companies=root.find("div", class_=["list_wrap"]).find("ul", class_=["directory-list active"])

            # there are two kinds of companies sponsored and non-sponsored
            req=list_companies.find_all('li', {"class": "provider provider-row sponsor"})
            len_sponsored=len(req)

            req+=list_companies.find_all('li', {"class": "provider provider-row"})
            add_class=' sponsor'

            #company info(current page):
            for i in range(len(req)):
                
                if(i>=len_sponsored):
                    add_class=''

                details=[] # to store the details of a company
                details.append(supported_domains[index])

                # each of the following properties is under try-except block to avoid any error during parsing or unexpected behaviour

                #company name:-
                try:
                    company=req[i].find('div').find('div').find('div').find('div').find("h3").find("a")
                    details.append(company.text.strip())
                except Exception as _:
                    details.append(not_avai)


                #website:-
                try:
                    website=req[i].find("div").find("div",class_=["provider-detail col-md-2"]).find('ul').find('li').find('a').get("href")
                    details.append(getlink(website))
                except Exception as _:
                    details.append(not_avai)


                #location:-
                try:
                    location=req[i].find("div", class_=['row']).find('div',class_=[selector1]).find("div", class_=[selector3]).find("div", class_=[selector2]).find('div', class_=['module-list']).find_all("div", class_=[selector4])[2].find("span")
                    details.append(location.text.strip())
                except Exception as _:
                    details.append(not_avai)


                #contact:-
                try:
                    profileURL=req[i].find("div").find("div",class_=["provider-detail col-md-2"]).find('ul').find('li', class_=['website-profile']).find('a').get("href")
                    profileURL="https://clutch.co/"+profileURL
                    contact = getcontact(profileURL)
                    details.append(contact)
                except Exception as _:
                    details.append(not_avai)


                #Rating:-
                try:
                    rating=req[i].find('div', class_=['row']).find("div", class_=[selector1]).find("div", class_=["row provider-info--header"]).find('div', class_=["company col-md-12"+add_class]).find("div", class_=["rating-reviews"]).find("a").find("div", class_=["reviews-totals-stars"]).find("div", class_=['fivestar']).find("div", class_=["star star-1 star-odd"]).find("span")
                    details.append(round(float(rating.text.strip()),2))
                except Exception as _:
                    details.append(not_avai)


                #Review count:-
                try:
                    review_cnt=req[i].find('div', class_=['row']).find("div", class_=[selector1]).find("div", class_=["row provider-info--header"]).find('div', class_=["company col-md-12"+add_class]).find("div", class_=["rating-reviews"]).find("div", class_=['reviews-link']).find("a")
                    details.append(review_cnt.text.strip())
                except Exception as _:
                    details.append(not_avai)


                #Hourly rate:-
                try:
                    hr_rate=req[i].find("div", class_=['row']).find('div',class_=[selector1]).find("div", class_=[selector3]).find("div", class_=[selector2]).find('div', class_=['module-list']).find_all("div", class_=[selector4])[0].find("span")
                    details.append(hourratehandler(hr_rate))
                except Exception as _:
                    details.append(not_avai)


                #Min project size:-
                try:
                    minProjSize=req[i].find("div", class_=['row']).find('div',class_=[selector1]).find("div", class_=[selector3]).find("div", class_=[selector2]).find('div', class_=['module-list']).find("div", class_=["list-item block_tag custom_popover"]).find("span").text
                    details.append(minProjSize)
                except Exception as _:
                    details.append(not_avai)


                #Employee size:-
                try:
                    employeeSize=req[i].find("div", class_=['row']).find('div',class_=[selector1]).find("div", class_=[selector3]).find("div", class_=[selector2]).find('div', class_=['module-list']).find_all("div", class_=[selector4])[1].find("span").text
                    details.append(employeeSize)
                except Exception as _:
                    details.append(not_avai)


                csvwriter.writerow(details) # populating the csv file with data
                count_companies+=1

                pbar.update(1)
                if(count_companies>=num_companies):
                    pbar.close()
                    break

csvfile.close()
