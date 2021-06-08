import requests
from bs4 import BeautifulSoup
# import pprint

########################
## SCRAPE HACKER NEWS ##
########################

# I am getting news from first 2 pages
res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')

soup = BeautifulSoup(res.text,'html.parser')
soup2 = BeautifulSoup(res2.text,'html.parser')

links = soup.select('.storylink')
links2 = soup2.select('.storylink')

subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

first_2pages_links = links + links2
first_2pages_subtexts = subtext + subtext2

# typical pattern to sort a dictionary, using a lambda  
def sort_stories_by_votes(hnlist):
    return sorted(hnlist,key= lambda k: k['votes'],reverse=True)

def create_custom_hn(links,subtext):
    hn = []
    for index,item in enumerate(links):
        # why we use enumerate?
        # links[index] = item, but to retrieve subtext (that is not being enumerate) we need to use enumerate
        title = links[index].getText()
        href = links[index].get('href',None)
        vote = subtext[index].select('.score')
        # now this is going to run if the vote list exist
        if len(vote):
            points = int(vote[0].getText().replace(' points','')) # get rid of the point text and just keep the 'int' for the next check
            if points > 99:
                hn.append({'title':title,'link':href,'votes':points}) 
    # return hn
    return sort_stories_by_votes(hn)

def page_from_scraped_data():
    # my_news: is the list of dictionaries
	my_news = create_custom_hn(first_2pages_links,first_2pages_subtexts)
	return my_news
# pprint.pprint(create_custom_hn(first_2pages_links,first_2pages_subtexts))

########################
## SCRAPE HACKER JOBS ##
########################

resJ = requests.get('https://news.ycombinator.com/jobs')
soupJ = BeautifulSoup(resJ.text,'html.parser')

linksJ = soupJ.select('.storylink')
# print(linksJ)
subtextJ = soupJ.select('.subtext')

def create_custom_hnJ(linksJ,subtextJ):
    hnJ = []
    for index,item in enumerate(linksJ):
        title = item.getText()
        href = item.get('href',None)
        hnJ.append({'title':title,'link':href}) 
    return hnJ

def jobs_from_scraped_data():
    # my_jobs: is the list of dictionaries
	my_jobs = create_custom_hnJ(linksJ,subtextJ)
	return my_jobs

# pprint.pprint(create_custom_hnJ(linksJ,subtextJ))
