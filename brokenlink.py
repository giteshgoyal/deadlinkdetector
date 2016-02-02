import urllib.request
from bs4 import BeautifulSoup
import urllib.error
from urllib.parse import urlparse
url="http://www.nitjreader.in/"
url=input("Enter Website to be Scanned\n")
maxpages=input("Enter The Depth of Scan ...Press 0 For Whole Website Scan \n")
parse_object=urlparse(url)
file_name=parse_object.netloc
print("-----------------------------Output Saved to "+file_name+".txt ..Be patient Please-----------------------------------------")
maxpages=int(maxpages)
broken_links=0
working_links=0
#stack that maintains links to visit
urls=[url]
#maintains link that are visited
visited=[url]
file_name=file_name+".txt"
fopen=open(file_name,"w")
fopen.write("URL" + '---------------->')
fopen.write("STATUS\n")


def web_spider():
    global urls
    pages=1
    while pages<=maxpages and len(urls)>0 :
        try:
            htmltext=urllib.request.urlopen(urls[0]).read()
        except:
            print(urls[0])
        soup = BeautifulSoup(htmltext,'html.parser')
        urls.pop(0)
       # print(len(urls))
        continue_spider(soup)
        if maxpages!=0:
            pages=pages+1   
    return


def continue_spider(soup):
    global urls
    global broken_links
    global working_links
    for tag in soup.findAll('a',href=True):
        tag['href']=urllib.parse.urljoin(url,tag['href'])
        response,status=check_link(tag['href'])
        if url in tag['href'] and tag['href'] not in visited and response==1:
            urls.append(tag['href'])
            visited.append(tag['href'])
            working_links=working_links+1
            
        elif response!=1:
            broken_links=broken_links+1
            fopen.write(tag['href'] + '---------------->')
            fopen.write(str(status) + '\n\n')
        
      
            
    return


def check_link(url):
    print (url)
    global urls
    try:
        response = urllib.request.urlopen(url)
        return 1, 'OK'
    except urllib.error.HTTPError as e:
        return 0, print(str(e.code))
    except urllib.error.URLError as e:
        print(str(e.args))
        return 0, 'Invalid Url'
    except:
        return 0, 'Wrong Url'
    return

web_spider()
total_links=working_links+broken_links
fopen.write("-------------------------------------------------------------------------SUMMARY---------------------------------------------------------------------" + '\n\n')
fopen.write("Total links Visited "+str(total_links)+" \n ")
fopen.write("Total working links Visited "+str(working_links)+" \n")
fopen.write("Total dead links Visited "+str(broken_links)+"\n")
print("Total links Visited "+str(total_links)+"  ")
print("Total links Visited "+str(working_links)+"  ")
print("Total links Visited "+str(broken_links)+"  ")
fopen.close()
            
    


       
       

        
        
