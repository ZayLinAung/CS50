import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transDic = {}
    for pages in corpus:
        transDic[pages] = 0

    # if page has no outgoing link
    if len(corpus[page]) == 0:
        for pages in corpus:
            transDic[pages] = (1-damping_factor)/len(corpus) + damping_factor/len(corpus)
        return transDic
    
    for pages in transDic:
        transDic[pages] += (1-damping_factor)/len(corpus)
        if pages in corpus[page]:
            transDic[pages] += damping_factor/len(corpus[page])
    
    return transDic


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRank = {}
    for page in corpus:
        pageRank[page] = 0
    states = []
    prob = []
    sample = random.choice(list(corpus))
    for i in range(n):
        dic = transition_model(corpus, sample, damping_factor)
        for page in dic:
            states.append(page)
            prob.append(dic[page])
        prob = np.array(prob)
        prob /= prob.sum()  # normalize
        sample = np.random.choice(states,p = prob)
        pageRank[sample] += 1
        states = []
        prob = []
    
    for page in pageRank:
        pageRank[page] /= n

    return pageRank   


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRank = {}
    for pages in corpus:
        pageRank[pages] = 1 / len(corpus)
    
    while(True):
        for pages in corpus:
            currentRank = pageRank[pages]
            pageRank[pages] = (1 - damping_factor)/len(corpus)
            sum = 0

            for key in corpus:
                if len(corpus[key]) == 0:
                    sum += (pageRank[key] / len(corpus))
                if pages in corpus[key]:
                    sum += (pageRank[key] / len(corpus[key])) 
            pageRank[pages] += (damping_factor * sum)
            if abs(currentRank - pageRank[pages]) < 0.001:
                return pageRank


if __name__ == "__main__":
    main()
