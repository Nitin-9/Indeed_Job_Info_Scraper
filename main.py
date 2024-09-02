#import mysql.connector, csv, time, os, codecs
import csv, time, os, codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from patch import webdriver_executable

# First of all, download Python in your system and install this library which I have imported.


# This code will create a folder named Htmlfile in your folder where these files will be stored.

foldername = 'HtmlFiles'

directory = os.getcwd() + f'\{foldername}'
if not os.path.isdir(directory): os.makedirs(directory)

# .....


# If you want to insert your data into the database then create a database name.
# This code connect your database.
# And if you don't need it, you can comment it and select this part use control+? .

# connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password='',
#     database="dnb_dat_aus"
# )
#
# cursor = connection.cursor()
# .....

# This is driver install
webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
driver = webdriver.Chrome(webdriver_path)
# In vscode we don't need to give path of driver in Chrome().we can write below line dirctly and get output of above two lines.
#driver = webdriver.Chrome()


# ...

# This function csv create code
#
def write_output(data):
    with open('indeed_data.csv', mode='a', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(data)
    output_file.close()


write_output(["Company_Name"])
# # ....

# my code starts from here


# I have given the range from 1 to 21 which will go to 20 pages because I went to the website and saw the pagination, so I fixed it by giving the range.

url = "https://ca.indeed.com/jobs?q=systems+engineer&l=Montr%C3%A9al%2C+QC"

# or this code, it will see the page in your folder, if it is taken to that place, it will go to else or it will get it from the driver, it will save the page or it will give the result.
#
filename = directory + '\\' + 'indeed_job_page' + '.html'

if os.path.isfile(f"{filename}"):
    f = codecs.open(filename, "r", "utf-8")
    soup = BeautifulSoup(f, 'lxml')
    all_locations = soup.find_all('li', {'class': 'css-5lfssm eu4oa1w0'})
#
else:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    all_locations = soup.find_all('li', {'class': 'css-5lfssm eu4oa1w0'})
# except:
#     time.sleep(3)
#     soup = BeautifulSoup(driver.page_source, 'lxml')
#     all_locations =  soup.find_all('li', {'class': 'css-5lfssm eu4oa1w0'})
    f = codecs.open(filename, "w", "utf-8")
    f.write(driver.page_source)
#     print(all_locations)


for loc in all_locations:
    Company_Name = loc.find('span', {'class': 'css-63koeb eu4oa1w0'}).text.strip()

    Address = loc.find('div', {'class': 'css-1p0sjhy eu4oa1w0'}).text.strip()
    print(Company_Name,Address)

    # Revenue = loc.find('div', {'class': 'col-md-2 last'}).text.replace(' ', '').replace('\n\n\n', ' ').replace(
    #     '\n\n', ' ').replace('SalesRevenue($M):', '').strip()

    #     print('Company_Name:', Company_Name, ' ,', 'Address:', Address, ' ,', 'Revenue:', Revenue)
    #
    #     # This info part will write the result in the form.
    #
    info = [Company_Name,Address]
    write_output(info)
    #     # ....

        # This part will insert the result into the database
        # And if you don't need it, you can comment it and select this part use control+?
        # val = (Company_Name, Address, Revenue)
        # cursor.execute('INSERT IGNORE INTO tbl_dnb_data (Company_Name,Address,Revenue) VALUES (%s,%s,%s)', val)
        # connection.commit()
