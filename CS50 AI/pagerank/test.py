
def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    numOfPages = 0
    transDic = {}
    for pages in corpus:
        numOfPages += 1
        transDic[pages] = 0
    
    for pages in transDic:
        transDic[pages] += (1-damping_factor)/numOfPages
        if page in corpus and pages != page:
            transDic[pages] += round(damping_factor/len(corpus[page]), 3)
        if page not in corpus:
            transDic[pages] += round(damping_factor/numOfPages, 3)
    
    return transDic

def main():
    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html" : {"2.html"}}
    page = "1.html"
    d = 0.85
    dic = transition_model(corpus, page, d)
    print(dic)

if __name__ == "__main__":
    main()