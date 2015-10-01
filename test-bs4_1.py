from bs4 import BeautifulSoup
soup = BeautifulSoup(open('1.html'))

#print soup.prettify()
#print soup.td.string
#for string in soup.strings:
#for string in soup.stripped_strings:
    #print(repr(string))
#    print(repr(string)).decode('utf8')

print '[+]..'
#print soup.find_all('td colspan="3"')


#print soup.get_text()

#print type(soup.get_text())
#print type([text for text in soup.stripped_strings])
mlist = [text for text in soup.stripped_strings]
for n in mlist:
    if "w3.org" in n :continue
    print n


import re
soup.find(text=re.compile("sisters"))
# u'Once upon a time there were three little sisters; and their names were\n'




#################







from bs4 import BeautifulSoup
soup = BeautifulSoup(open('1.html'))
#del soup['head']

#print soup

#print soup.get_text()

print soup.find_all("table").get_text()






########################



from bs4 import BeautifulSoup
import re

#soup = BeautifulSoup(open('1.html'))
f = open("1.html", "r") 
fin = f.read()
f.close()
mycon = re.compile(r"<form(.*?)<\/form>",re.DOTALL).findall(fin)
#print type(mycon)
#print mycon[0]
mytext = "<form" + mycon[0] + "</form>"

soup = BeautifulSoup(mytext)
#print soup.get_text()
f = open('2.txt' ,'ab')
f.write(soup.get_text().encode('utf8'))
f.close()
