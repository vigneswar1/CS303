import copy

class BS:
    def __init__(self):
        self.nodes = {'B':[],'E':[],'A':['B','E'],'J':['A'],'M':['A']}
        self.probability_table = {
            'B':{'T':0.001,'F':0.999},
            'E':{'T':0.002,'F':0.998},
            'A':{('T','T'):{'T':0.95,'F':0.05},('T','F'):{'T':0.94,'F':0.06},('F','T'):{'T':0.29,'F':0.71},('F','F'):{'T':0.001,'F':0.999}},
            'J':{('T',):{'T':0.90,'F':0.10},('F',):{'T':0.05,'F':0.95}},
            'M':{('T',):{'T':0.70,'F':0.30},('F',):{'T':0.01,'F':0.99}}
        }
    
    def probability_function(self,node,parent,truthvalue):
        if not self.nodes[node]:
            return self.probability_table[node][truthvalue]
        else:
            parent_truthvalues = tuple(parent[x] for x in self.nodes[node])
            return self.probability_table[node][parent_truthvalues][truthvalue]
        
    def chain_rule_prob(self,variables,evidence):
        if not variables:
            return 1.0
        curr = variables[0]
        rem = variables[1:]
        if curr in evidence:
            prob = self.probability_function(curr,evidence,evidence[curr])
            return prob * self.chain_rule_prob(rem,evidence)
        else:
            total_prob = 0
            for bool in ['T','F']:
                new_evidence = evidence.copy()
                new_evidence[curr] = bool
                prob = self.probability_function(curr,new_evidence,bool)
                total_prob += prob * self.chain_rule_prob(rem,new_evidence)
            return total_prob
    
    def bayesProb(self, variable, value, evidence):
        all_variables = ['B','E','A','J','M']
        new_evidence = evidence.copy()
        new_evidence[variable] = value
        nr = self.chain_rule_prob(all_variables,new_evidence)
        dr = 0
        for bool in ['T','F']:
            new_evidence = evidence.copy()
            new_evidence[variable] = bool
            dr += self.chain_rule_prob(all_variables,new_evidence)
        
        return nr/dr
    
    def Joint_distribution(self,variable,evidence):
        true_prob = self.bayesProb(variable,'T',evidence)
        false_prob = 1 - true_prob
        return true_prob,false_prob
    

bs = BS()
prob_t, prob_f = bs.Joint_distribution('J', {'B': 'T', 'E': 'T'})
print(f"P(J| B=T, E=T) = < {prob_t:.4f} , {prob_f:.4f} >")

prob_t, prob_f = bs.Joint_distribution('A', {'B': 'T'})
print(f"P(A| B=T) = < {prob_t:.4f} , {prob_f:.4f} >")

prob_t, prob_f = bs.Joint_distribution('E', {'M': 'T'})
print(f"P(E| M=T) = < {prob_t:.4f} , {prob_f:.4f} >")

prob_t, prob_f = bs.Joint_distribution('B', {'A': 'T'})
print(f"P(B| A=T) = < {prob_t:.4f} , {prob_f:.4f} >")


print("\n\n Conditional-Independence \n")
prob_t, prob_f = bs.Joint_distribution('J',{'M':'T','A':'T'})
print(f"P(J|M,A) = < {prob_t:.4f} , {prob_f:.4f} >")
prob_t, prob_f = bs.Joint_distribution('J',{'A':'T'})
print(f"P(J|A) = < {prob_t:.4f} , {prob_f:.4f} >")
