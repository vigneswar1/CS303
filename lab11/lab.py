import random
from collections import defaultdict, Counter

class BayesianNetwork:
    def __init__(self, network):
        self.network = network
        self.variables = list(network.keys())

    def sample_variable(self, var, sampled_values):
        parents = self.network[var]['parents']
        parent_values = tuple(sampled_values[p] for p in parents)
        p_true = self.network[var]['cpt'][parent_values]
        return random.random() < p_true

    def prior_sample(self):
        sampled = {}
        for var in self.variables:
            sampled[var] = self.sample_variable(var, sampled)
        return sampled

    def rejection_sampling(self, query_var, evidence, N=10000):
        counts = Counter()
        for _ in range(N):
            sample = self.prior_sample()
            if all(sample[e] == v for e, v in evidence.items()):
                counts[sample[query_var]] += 1
        total = sum(counts.values())
        if total == 0:
            return None
        return {k: v / total for k, v in counts.items()}

    def weighted_sample(self, evidence):
        w = 1.0
        sampled = {}
        for var in self.variables:
            parents = self.network[var]['parents']
            parent_values = tuple(sampled[p] for p in parents)
            p_true = self.network[var]['cpt'][parent_values]
            if var in evidence:
                sampled[var] = evidence[var]
                w *= p_true if evidence[var] else (1 - p_true)
            else:
                sampled[var] = random.random() < p_true
        return sampled, w

    def likelihood_weighting(self, query_var, evidence, N=10000):
        weighted_counts = defaultdict(float)
        for _ in range(N):
            sample, w = self.weighted_sample(evidence)
            weighted_counts[sample[query_var]] += w
        total = sum(weighted_counts.values())
        return {k: v / total for k, v in weighted_counts.items()}

    def gibbs_sampling(self, query_var, evidence, N=10000, burn_in=1000):
        state = {}
        for var in self.variables:
            if var in evidence:
                state[var] = evidence[var]
            else:
                state[var] = random.choice([True, False])

        counts = Counter()

        for i in range(N + burn_in):
            for var in self.variables:
                if var in evidence:
                    continue
                p_true = self.mb_conditional(var, state)
                state[var] = random.random() < p_true
            if i >= burn_in:
                counts[state[query_var]] += 1

        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    def mb_conditional(self, var, state):
        def joint_prob(x_val):
            s = state.copy()
            s[var] = x_val
            parents = self.network[var]['parents']
            parent_values = tuple(s[p] for p in parents)
            p_var = self.network[var]['cpt'][parent_values] if x_val else 1 - self.network[var]['cpt'][parent_values]
            p_children = 1.0
            for child, node in self.network.items():
                if var in node['parents']:
                    parent_values = tuple(s[p] for p in node['parents'])
                    p_c = node['cpt'][parent_values]
                    p_children *= p_c if s[child] else (1 - p_c)
            return p_var * p_children

        p_true = joint_prob(True)
        p_false = joint_prob(False)
        return p_true / (p_true + p_false)


if __name__ == "__main__":
    bn = BayesianNetwork({
        'Burglary': {'parents': [], 'cpt': {(): 0.001}},
        'Earthquake': {'parents': [], 'cpt': {(): 0.002}},
        'Alarm': {'parents': ['Burglary', 'Earthquake'],
                  'cpt': {(True, True): 0.95, (True, False): 0.94,
                          (False, True): 0.29, (False, False): 0.001}},
        'JohnCalls': {'parents': ['Alarm'],
                      'cpt': {(True,): 0.90, (False,): 0.05}},
        'MaryCalls': {'parents': ['Alarm'],
                      'cpt': {(True,): 0.70, (False,): 0.01}},
    })

    print("Prior Sampling:", bn.rejection_sampling('Burglary', {}, 10000))
    print("Rejection Sampling:", bn.rejection_sampling('Burglary', {'JohnCalls': True, 'MaryCalls': True}, 10000))
    print("Likelihood Weighting:", bn.likelihood_weighting('Burglary', {'JohnCalls': True, 'MaryCalls': True}, 10000))
    print("Gibbs Sampling:", bn.gibbs_sampling('Burglary', {'JohnCalls': True, 'MaryCalls': True}, 10000))
