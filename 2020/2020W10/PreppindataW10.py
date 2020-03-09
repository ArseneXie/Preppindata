from kanren import *
from kanren.core import lall

def higher(a, b, list):
    return membero((a,b), zip(list, list[1:]))

def clue1(x):
    return success if x[0][0:1]=='A' and x[3]=='1' else fail

def isans(x,list):
    return membero(x, list)

def anyans(ca,cb,list):
    return conde([membero(ca, list)],[membero(cb, list)])

customer = var()

clues = lall(
    (eq, (var(), var(), var(), var()), customer),
    (membero,('Baroness', var(), var(), var()), customer),
    (membero,('Sergeant', var(), var(), var()), customer),
    (membero,('Reverend', var(), var(), var()), customer),
    (membero,('Doctor', var(), var(), var()), customer),
    (membero,(var(), 'Bevens', var(), var()), customer),
    (membero,(var(), 'Shadwell', var(), var()), customer),
    (membero,(var(), 'Dimmadome', var(), var()), customer),
    (membero,(var(), 'Rotzenheimer', var(), var()), customer),
    (membero,(var(), var(), 'Rose Bar', var()), customer),
    (membero,(var(), var(), 'Lemon Gel', var()), customer),
    (membero,(var(), var(), 'Chamomile Bar', var()), customer),
    (membero,(var(), var(), 'Hibiscus Soap-on-a-Rope', var()), customer),
    (higher,(var(), var(), var(), '1'), (var(), var(), var(), '2'), customer),
    (higher,(var(), var(), var(), '2'), (var(), var(), var(), '3'), customer),
    (higher,(var(), var(), var(), '3'), (var(), var(), var(), '4'), customer),
    (higher,(var(), 'Dimmadome', var(), var()), (var(), 'Bevens', var(), var()), customer),
    (higher,(var(), var(), 'Lemon Gel', var()), (var(), var(), 'Rose Bar', var()), customer),
    (anyans,('Sergeant', var(), var(), '1'),('Sergeant', var(), var(), '3'), customer),   
    (anyans,(var(), var(), 'Lemon Gel', '1'),(var(), var(), 'Lemon Gel', '3'), customer)
)    

solutions = run(0, customer, clues)

# #
# #,
#     conde([membero(('Sergeant', var(), var(), '1'), customer)],[membero(('Sergeant', var(), var(), '3'), customer)],[membero((var(), var(), 'Lemon Gel', '1'), customer)],[membero((var(), var(), 'Lemon Gel', '3'), customer)])
# )
# #

print('\nHere are all the details:')
attribs = ['Title', 'LastName', 'Product', 'Priority']
print('\n' + '\t\t'.join(attribs))
print('=' * 57)
for item in solutions[0]:
    print('')
    print('\t\t'.join([str(x) for x in item]))