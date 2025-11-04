def clause_parsing(premise):
    if "(" not in premise:
        return premise, []
    indx = premise.index("(")
    function = premise[:indx]
    values = premise[indx+1:-1]

    balance = 0
    curr = ""
    vals = []
    for ptr in values:
        if ptr == ',' and balance == 0:
            vals.append(curr)
            curr = ""
        else:
            if ptr == "(":
                balance += 1
            elif ptr == ")":
                balance -= 1
            curr += ptr
    if curr:
        vals.append(curr)
    return function, vals

def check_if_its_a_variable(term):
    if not term:
        return False
    return term[0].islower()

def unification(expr1, expr2, values=None):
    if values is None:
        values = {}
    if values == -1:
        return -1
    if expr1 == expr2:
        return values

    if check_if_its_a_variable(expr1) and expr1 in values:
        return unification(values[expr1], expr2, values)
    if check_if_its_a_variable(expr2) and expr2 in values:
        return unification(expr1, values[expr2], values)

    if check_if_its_a_variable(expr1):
        if expr1 in expr2 and expr1 != expr2:
            return -1
        values[expr1] = expr2
        return values
    if check_if_its_a_variable(expr2):
        if expr2 in expr1 and expr1 != expr2:
            return -1
        values[expr2] = expr1
        return values

    if "(" in expr1 and "(" in expr2:
        func1, values1 = clause_parsing(expr1)
        func2, values2 = clause_parsing(expr2)
        if func1 != func2 or len(values1) != len(values2):
            return -1
        for i in range(len(values1)):
            values = unification(values1[i], values2[i], values)
            if values == -1:
                return -1
        return values
    return -1

def make_substitutions(expr, values):
    if "(" not in expr:
        if expr in values:
            result = values[expr]
            while result in values and result != values[result]:
                result = values[result]
            return result
        return expr

    func, vals = clause_parsing(expr)
    new_values = [make_substitutions(val, values) for val in vals]
    return func + "(" + ",".join(new_values) + ")"

def split_the_rule(rule):
    premises, conclusion = rule.split("->")
    # Replace 'and' word instead of '∧'
    premises = [p.strip() for p in premises.split("and")]
    return premises, conclusion.strip()

def parser_for_kb(kb):
    facts = []
    rules = []
    for sentence in kb:
        sentence = sentence.replace(" ", "")
        if '->' in sentence:
            rules.append(sentence)
        else:
            facts.append(sentence)
    return facts, rules

knowledgeBase = [
    "Ancestor(Mother(x), x)",
    "Ancestor(x, y) and Ancestor(y, z) -> Ancestor(x, z)",
    "Mother(John)"
]

queries = [
    "Ancestor(Mother(y), John)",
    "Ancestor(Mother(Mother(y)), John)",
    "Ancestor(Mother(Mother(Mother(y))), Mother(y))",
    "Ancestor(Mother(John), Mother(Mother(John)))"
]

def forward_chaining(kb, query):
    facts, rules = parser_for_kb(kb)
    what_we_know = set(facts)
    query = query.replace(" ", "")
   
    while True:
        new_facts = set()
       
        for rule in rules:
            premises, conclusion = split_the_rule(rule)
            all_subs = [{}]
           
            for premise in premises:
                next_subs = []
                for sub in all_subs:
                    for fact in what_we_know:
                        sub_copy = sub.copy()
                        res = unification(make_substitutions(premise, sub_copy), fact, sub_copy)
                        if res != -1:
                            next_subs.append(res)
                all_subs = next_subs
                if not all_subs:
                    break
           
            for sub in all_subs:
                new_fact = make_substitutions(conclusion, sub)
                if new_fact not in what_we_know:
                    new_facts.add(new_fact)
       
        # Check query against all known facts
        for fact in what_we_know.union(new_facts):
            if unification(fact, query, {}) != -1:
                return True
       
        if not new_facts:  
            return False
       
        what_we_know.update(new_facts)


for q in queries:
    result = forward_chaining(knowledgeBase, q)
    print(f"Query: {q} -> {result}")



