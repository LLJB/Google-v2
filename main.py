def adv_lookup(index, query):
    
    query = query.split()
    res=[]
    tres={}
    for keyword in query:
        j=0
        while j<len(index):
            if (keyword,j) in index:
                tres[(keyword,j)]=index[(keyword,j)]
            j=j+1
    
    
    def reverse_index(dict):
        index=[]
        solution={}
        for e in dict:
            if dict[e] not in index:
                index.append(dict[e])
        for i in index:
            solution[i]=[]
            for x in dict:
                if dict[x]==i:
                    solution[i].append(x)
        return solution
    
    tres=reverse_index(tres)
    
    for e in tres:
        k=0
        while k<len(index):
            i=0
            vt=True
            while i<len(query):
                vt=vt and (query[i],k+i) in tres[e]
                i=i+1
            k=k+1
            if vt and e not in res:
                res.append(e)
      
    if res!=[]:
        return res

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    i=0
    while i<len(words):
        add_to_index(index, words[i], url,i)
        i=i+1
        
def add_to_index(index, keyword, url,i):
    index[(keyword,i)] = url
    

cache = {
   'http://www.udacity.com/cs101x/final/multi.html': """<html>
<body>

<a href="http://www.udacity.com/cs101x/final/a.html">A</a><br>
<a href="http://www.udacity.com/cs101x/final/b.html">B</a><br>

</body>
""", 
   'http://www.udacity.com/cs101x/final/b.html': """<html>
<body>

Monty likes the Python programming language
Thomas Jefferson founded the University of Virginia
When Mandela was in London, he visited Nelson's Column.

</body>
</html>
""", 
   'http://www.udacity.com/cs101x/final/a.html': """<html>
<body>

Monty Python is not about a programming language
Udacity was not founded by Thomas Jefferson
Nelson Mandela said "Education is the most powerful weapon which you can
use to change the world."
</body>
</html>
""", 
}

def get_page(url):
    if url in cache:
        return cache[url]
    else:
        print "Page not in cache: " + url
        return None
    





#Here are a few examples from the test site:

index, graph = crawl_web('http://www.udacity.com/cs101x/final/multi.html')

print adv_lookup(index, 'Python')
#>>> ['http://www.udacity.com/cs101x/final/b.html', 'http://www.udacity.com/cs101x/final/a.html']

print adv_lookup(index, 'Monty Python')
#>>> ['http://www.udacity.com/cs101x/final/a.html']

print adv_lookup(index, 'Python programming language')
#>>> ['http://www.udacity.com/cs101x/final/b.html']

print adv_lookup(index, 'Thomas Jefferson')
#>>> ['http://www.udacity.com/cs101x/final/b.html', 'http://www.udacity.com/cs101x/final/a.html']

print adv_lookup(index, 'most powerful weapon')
#>>> ['http://www.udacity.com/cs101x/final/a.html']
