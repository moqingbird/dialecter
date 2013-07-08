class NGram:
    ngram=""
    count=0
    likelihood=0

    def __init__(self,id,words,counts,likelihoods,saved):
        self.id=id
        self.words=words
        self.counts=counts
        self.likelihoods=likelihoods
        self.saved=saved


