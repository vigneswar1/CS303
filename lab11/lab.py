import copy
import random

class SamplingTypes:
    def __init__(self):
        self.nodes = {'B':[],'E':[],'A':['B','E'],'J':['A'],'M':['A']}
        self.prob_table = {
            'B':{'T':0.001,'F':0.999},
            'E':{'T':0.002,'F':0.998},
            'A':{('T','T'):{'T':0.95,'F':0.05},('T','F'):{'T':0.94,'F':0.06},('F','T'):{'T':0.29,'F':0.71},('F','F'):{'T':0.001,'F':0.999}},
            'J':{('T',):{'T':0.90,'F':0.10},('F',):{'T':0.05,'F':0.95}},
            'M':{('T',):{'T':0.70,'F':0.30},('F',):{'T':0.01,'F':0.99}}
        }
        self.var_order = ['B','E','A','J','M']
    
    def get_prob(self, node, evidence, truthvalue):
        if not self.nodes[node]:
            return self.prob_table[node][truthvalue]
        else:
            parent_vals = tuple(evidence[p] for p in self.nodes[node])
            return self.prob_table[node][parent_vals][truthvalue]
        
    def prior_sample(self):
        sample = {}
        for var in self.var_order:
            prob_T = self.get_prob(var, sample, 'T')
            sample[var] = 'T' if random.random() < prob_T else 'F'
        return sample
        
    def rejection_sampling(self, query_var, query_val, evidence, N=10000):
        count = 0
        match = 0
        for _ in range(N):
            s = self.prior_sample()
            valid = True
            for var in evidence:
                if s[var] != evidence[var]:
                    valid = False
                    break
            if valid:
                count += 1
                if s[query_var] == query_val:
                    match +=1
        return match/count if count else 0.0
        
    def likelihood_weighting(self, query_var, query_val, evidence, N=10000):
        total = 0.0
        w_match = 0.0
        for _ in range(N):
            sample = {}
            weight = 1.0
            for var in self.var_order:
                if var in evidence:
                    sample[var] = evidence[var]
                    weight *= self.get_prob(var, sample, evidence[var])
                else:
                    prob_T = self.get_prob(var, sample, 'T')
                    sample[var] = 'T' if random.random() < prob_T else 'F'
            total += weight
            if sample[query_var] == query_val:
                w_match += weight
        return w_match/total if total else 0.0
        
    def gibbs_sampling(self, query_var, query_val, evidence, N=10000):
        state = {}
        for var in self.var_order:
            if var in evidence:
                state[var] = evidence[var]
            else:
                state[var] = 'T' if random.random() < 0.5 else 'F'
        cnt = 0
        ok = 0
        for _ in range(N):
            for var in self.var_order:
                if var not in evidence:
                    neigh = {}
                    for v in self.var_order:
                        if v != var:
                            neigh[v] = state[v]
                    prob_T = self.get_prob(var, neigh, 'T')
                    state[var] = 'T' if random.random() < prob_T else 'F'
            cnt +=1
            if state[query_var] == query_val:
                ok +=1
        return ok/cnt if cnt else 0.0

bs = SamplingTypes()

print("P(J=T | A=T)")
print(bs.rejection_sampling('J','T', {'A':'T'},5000))
print(bs.likelihood_weighting('J','T', {'A':'T'},5000))
print(bs.gibbs_sampling('J','T', {'A':'T'},5000))

print("P(B=T | M=T)")
print(bs.rejection_sampling('B','T', {'M':'T'},5000))
print(bs.likelihood_weighting('B','T', {'M':'T'},5000))
print(bs.gibbs_sampling('B','T', {'M':'T'},5000))
