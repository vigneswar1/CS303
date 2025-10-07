import time, tracemalloc

def split_tokens(expr):
    expr = expr.replace(' ','')
    result = []
    idx = 0
    while idx < len(expr):
        if expr[idx] in '()':
            result.append(expr[idx])
            idx += 1
        elif idx < len(expr)-1 and expr[idx:idx+2] in ['->','<->']:
            result.append(expr[idx:idx+2])
            idx += 2
        elif expr[idx] in ['~','&','|']:
            result.append(expr[idx])
            idx += 1
        elif expr[idx].isupper():
            result.append(expr[idx])
            idx += 1
        else:
            raise ValueError(f"Unexpected char: {expr[idx]}")
    return result

def build_tree(expr):
    prec = {'~':1,'&':2,'|':3,'->':4,'<->':5}
    ops_set = set(prec.keys())
    tokens = split_tokens(expr)
    out = []
    ops = []
    pos = 0
    while pos < len(tokens):
        t = tokens[pos]
        if t.isupper():
            out.append(t)
        elif t=='~':
            ops.append(t)
        elif t in ops_set:
            while ops and ops[-1]!='(' and ops[-1] in ops_set and prec[ops[-1]] <= prec[t]:
                out.append(ops.pop())
            ops.append(t)
        elif t=='(':
            ops.append(t)
        elif t==')':
            while ops and ops[-1]!='(':
                out.append(ops.pop())
            if ops and ops[-1]=='(':
                ops.pop()
        pos += 1
    while ops:
        out.append(ops.pop())
    stack = []
    for t in out:
        if t.isupper():
            stack.append(t)
        elif t=='~':
            opnd = stack.pop()
            stack.append(('~',opnd))
        elif t in ops_set:
            r = stack.pop()
            l = stack.pop()
            stack.append((t,l,r))
    if len(stack)!=1:
        raise ValueError("Malformed formula")
    return stack[0]

def remove_implications(f):
    if isinstance(f,str):
        return f
    op = f[0]
    if op=='~':
        return ('~',remove_implications(f[1]))
    elif op=='->':
        l = remove_implications(f[1])
        r = remove_implications(f[2])
        return ('|',('~',l),r)
    elif op=='<->':
        l = remove_implications(f[1])
        r = remove_implications(f[2])
        return ('&',('|',('~',l),r),('|',('~',r),l))
    else:
        return (op,remove_implications(f[1]),remove_implications(f[2]))

def push_not(f):
    if isinstance(f,str):
        return f
    op = f[0]
    if op=='~':
        inner = f[1]
        if isinstance(inner,str):
            return f
        iop = inner[0]
        if iop=='~':
            return push_not(inner[1])
        elif iop=='&':
            return ('|',push_not(('~',inner[1])),push_not(('~',inner[2])))
        elif iop=='|':
            return ('&',push_not(('~',inner[1])),push_not(('~',inner[2])))
    else:
        return (op,push_not(f[1]),push_not(f[2]))
    return f

def distribute_or(f):
    if isinstance(f,str) or (isinstance(f,tuple) and f[0]=='~'):
        return f
    op = f[0]
    if op=='|':
        l = distribute_or(f[1])
        r = distribute_or(f[2])
        if isinstance(l,tuple) and l[0]=='&':
            return ('&',distribute_or(('|',l[1],r)),distribute_or(('|',l[2],r)))
        elif isinstance(r,tuple) and r[0]=='&':
            return ('&',distribute_or(('|',l,r[1])),distribute_or(('|',l,r[2])))
        return ('|',l,r)
    elif op=='&':
        return ('&',distribute_or(f[1]),distribute_or(f[2]))
    return f

def to_cnf_set(f):
    all_clauses = []
    def collect_clauses(x):
        if isinstance(x,str) or (isinstance(x,tuple) and x[0]=='~'):
            all_clauses.append(x)
        elif x[0]=='&':
            collect_clauses(x[1])
            collect_clauses(x[2])
        else:
            all_clauses.append(x)
    collect_clauses(f)
    res = []
    def collect_literals(x,lits):
        if isinstance(x,str) or (isinstance(x,tuple) and x[0]=='~'):
            lits.add(lit_str(x))
        elif x[0]=='|':
            collect_literals(x[1],lits)
            collect_literals(x[2],lits)
    def lit_str(l):
        if isinstance(l,str):
            return l
        return '~'+l[1]
    for c in all_clauses:
        s = set()
        if isinstance(c,str) or (isinstance(c,tuple) and c[0]=='~'):
            s.add(lit_str(c))
        else:
            collect_literals(c,s)
        res.append(s)
    return res

def convert_cnf(f):
    f = remove_implications(f)
    f = push_not(f)
    f = distribute_or(f)
    return to_cnf_set(f)

def complement(lit):
    if lit.startswith('~'):
        return lit[1:]
    return '~'+lit

def resolve(c1,c2):
    for l in c1:
        if complement(l) in c2:
            return (c1-{l}) | (c2-{complement(l)})
    return None

def clause_to_text(c):
    if len(c)==0:
        return "NIL"
    return " v ".join(sorted(list(c)))

def resolve_prover(premises,goal):
    step=0
    steps_list=[]
    all_cl = []
    idx = 0
    for p in premises:
        tree = build_tree(p)
        cnf = convert_cnf(tree)
        for cl in cnf:
            idx += 1
            all_cl.append((idx,cl))
            steps_list.append(f"{idx}. {clause_to_text(cl)}")
    steps_list.append("By proof of contradiction we assume")
    neg_goal = ('~',build_tree(goal))
    goal_cnf = convert_cnf(neg_goal)
    for cl in goal_cnf:
        idx += 1
        all_cl.append((idx,cl))
        steps_list.append(f"{idx}. {clause_to_text(cl)}")
    steps_list.append("Conclusions derived")
    curr_clauses = dict(all_cl)
    resolved_pairs = set()
    while True:
        new_c = []
        ids = list(curr_clauses.keys())
        for i,id1 in enumerate(ids):
            for id2 in ids[i+1:]:
                pair = tuple(sorted([id1,id2]))
                if pair in resolved_pairs:
                    continue
                resolved_pairs.add(pair)
                res = resolve(curr_clauses[id1],curr_clauses[id2])
                if res is not None:
                    step += 1
                    new_id = max(curr_clauses.keys())+1
                    if len(res)==0:
                        steps_list.append(f"{new_id}. NIL ({id1},{id2})")
                        return True,step,steps_list
                    new_c.append((new_id,res))
                    steps_list.append(f"{new_id}. {clause_to_text(res)} ({id1},{id2})")
        if not new_c:
            break
        for cid,cl in new_c:
            if cl not in curr_clauses.values():
                curr_clauses[cid]=cl
    return False,step,steps_list

tracemalloc.start()
print("Enter premises (empty line to stop)")
premises=[]
while True:
    l=input().strip()
    if not l:
        break
    premises.append(l)
goal=input("Enter goal: ").strip()
START=time.time()
res,steps_count,steps_taken=resolve_prover(premises,goal)
END=time.time()
_,mem=tracemalloc.get_traced_memory()
tracemalloc.stop()
print("\n\nResolution Result")
print("Proven" if res else "Not Proven")
print(f"Steps: {steps_count}\n")
for s in steps_taken:
    print(s)
timetaken = round(END-START,4)
print("\n     Time & Memory Usage       ")
print("---------------------------------")
print(" Time: {} ms | Memory: {} MB".format(timetaken,round(mem/1024/1024,5)))
print("---------------------------------")
