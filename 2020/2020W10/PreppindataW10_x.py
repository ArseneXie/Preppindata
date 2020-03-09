from kanren import *
from kanren.core import lall

def higher(a, b, list):
    return membero((a,b), zip(list, list[1:]))

def clue1(x):
    return success if x[0][0:1]=='A' and x[3]=='1' else fail

def isans(x,list):
    return membero(x, list)

def anyans(cx, list):
    return conde([membero(cx[0], list)],[membero(cx[1], list)],[membero(cx[2], list)])


customer = var()

clues = lall(
    (eq, (var(), var(), var(), var()), customer),
    (membero,('ATitle', var(), var(), var()), customer),
    (membero,('BTitle', var(), var(), var()), customer),
    (membero,('CTitle', var(), var(), var()), customer),
    (membero,('DTitle', var(), var(), var()), customer),
    (higher,(var(), var(), var(), '1'), (var(), var(), var(), '2'), customer),
    (higher,(var(), var(), var(), '2'), (var(), var(), var(), '3'), customer),
    (higher,(var(), var(), var(), '3'), (var(), var(), var(), '4'), customer),
    (anyans,[('ATitle', 'Aname', 'AProd', '1'),
             ('BTitle', 'Bname', 'BProd', '1'),
             ('CTitle', 'Cname', 'CProd', '1')], customer),
    (membero,('BTitle', var(), var(), '2'), customer),
    (membero,('DTitle', 'Dname', 'DProd', '3'), customer),
    (membero,('CTitle', 'Cname', 'CProd', '1'), customer)
)

solutions = run(0, customer, clues)

print('\nHere are all the details:')
attribs = ['Title', 'LastName', 'Product', 'Priority']
print('\n' + '\t\t'.join(attribs))
print('=' * 57)
for item in solutions[0]:
    print('')
    print('\t\t'.join([str(x) for x in item]))
    

#
# def left(q, p, list):
#    return membero((q,p), zip(list, list[1:]))
# def next(q, p, list):
#    return conde([left(q, p, list)], [left(p, q, list)])

# houses = var()

# rules = lall(
#    (eq, (var(), var(), var(), var(), var()), houses),

#    (membero,('Englishman', var(), var(), var(), 'red'), houses),
#    (membero,('Swede', var(), var(), 'dog', var()), houses),
#    (membero,('Dane', var(), 'tea', var(), var()), houses),
#    (left,(var(), var(), var(), var(), 'green'),
#    (var(), var(), var(), var(), 'white'), houses),
#    (membero,(var(), var(), 'coffee', var(), 'green'), houses),
#    (membero,(var(), 'Pall Mall', var(), 'birds', var()), houses),
#    (membero,(var(), 'Dunhill', var(), var(), 'yellow'), houses),
#    (eq,(var(), var(), (var(), var(), 'milk', var(), var()), var(), var()), houses),
#    (eq,(('Norwegian', var(), var(), var(), var()), var(), var(), var(), var()), houses),
#    (next,(var(), 'Blend', var(), var(), var()),
#    (var(), var(), var(), 'cats', var()), houses),
#    (next,(var(), 'Dunhill', var(), var(), var()),
#    (var(), var(), var(), 'horse', var()), houses),
#    (membero,(var(), 'Blue Master', 'beer', var(), var()), houses),
#    (membero,('German', 'Prince', var(), var(), var()), houses),
#    (next,('Norwegian', var(), var(), var(), var()),
#    (var(), var(), var(), var(), 'blue'), houses),
#    (next,(var(), 'Blend', var(), var(), var()),
#    (var(), var(), 'water', var(), var()), houses),
#    (membero,(var(), var(), var(), 'zebra', var()), houses)
# )

# solutions = run(0, houses, rules)
# output = [house for house in solutions[0] if 'zebra' in house][0][0]

# print('\n' + output + ' is the owner of the rabbit')
# print('\nHere are all the details:')
# attribs = ['Name', 'Pet', 'Color', 'Country']
# print('\n' + '\t\t'.join(attribs))
# print('=' * 57)
# for item in solutions[0]:
#     print('')
#     print('\t\t'.join([str(x) for x in item]))    
    
stra = 'Arsene'
stra[0:1]    
    