class NGram:
    ngram=""
    count=0
    likelihood=0

    def __init__(self,id,words,counts,total_count,likelihoods,total_likelihood,saved):
        self.id               = id
        self.words            = words
        self.counts           = counts
        self.total_count      = total_count
        self.likelihoods      = likelihoods
        self.total_likelihood = total_likelihood
        self.saved            = saved


