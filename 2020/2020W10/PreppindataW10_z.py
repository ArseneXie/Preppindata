from kanren import *
from kanren.core import lall,lany

def higher(a, b, list):
    return membero((a,b), zip(list, list[1:]))

customer = var()

clues = lall(
    # Solution with 4 fields: Title, LastName, Product and Priority
    (eq, (var(), var(), var(), var()), customer),  
    # All Values 
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
    (membero,(var(), var(), var(), '1'), customer),
    (membero,(var(), var(), var(), '2'), customer),
    (membero,(var(), var(), var(), '3'), customer),
    (membero,(var(), var(), var(), '4'), customer),
    # Priority 1 > 2 > 3 > 4 
    (higher,(var(), var(), var(), '1'), (var(), var(), var(), '2'), customer), 
    (higher,(var(), var(), var(), '2'), (var(), var(), var(), '3'), customer),
    (higher,(var(), var(), var(), '3'), (var(), var(), var(), '4'), customer),
    # Clue1a  customer with the highest priority has a title and last name that begin with the same letter
    (lany,(membero,('Baroness', 'Bevens', var(), '1'), customer),
     (membero,('Reverend', 'Rotzenheimer', var(), '1'), customer),
     (membero,('Sergeant', 'Shadwell', var(), '1'), customer),
     (membero,('Doctor', 'Dimmadome', var(), '1'), customer)), 
    # Clue2a Bevens' priority is directly after Dimmadome
    (higher,(var(), 'Dimmadome', var(), var()), (var(), 'Bevens', var(), var()), customer),
    # Clue6 The priority of the person who ordered the Rose Bar is directly after the person who ordered the Lemon Gel.
    (higher,(var(), var(), 'Lemon Gel', var()), (var(), var(), 'Rose Bar', var()), customer),
    # Clue2b Neither of these people ordered the Chamomile Bar or the Hibiscus Soap-on-a-Rope.
    (lany,(membero,(var(), 'Dimmadome', 'Rose Bar', var()), customer),
     (membero,(var(), 'Dimmadome','Lemon Gel', var()), customer)),
    (lany,(membero,(var(), 'Bevens', 'Rose Bar', var()), customer),
     (membero,(var(), 'Bevens', 'Lemon Gel', var()), customer)),
    # Clue3 The Sergeant and the person who ordered Lemon Gel are either 1st priority or 3rd priority
    (lany,(membero,('Sergeant', var(), var(), '1'), customer),
     (membero,('Sergeant', var(), var(), '3'), customer)),
    (lany,(membero,(var(), var(), 'Lemon Gel', '1'), customer),
     (membero,(var(), var(), 'Lemon Gel', '3'), customer)),
    # Clue4a The Reverend didn't order the Rose Bar.
    (lany,(membero,('Reverend', var(), 'Lemon Gel', var()), customer),
     (membero,('Reverend', var(), 'Chamomile Bar', var()), customer),
     (membero,('Reverend', var(), 'Hibiscus Soap-on-a-Rope', var()), customer)),
    # Clue4b And the Reverend isn't 2nd priority.
    (lany,(membero,('Reverend', var(), var(), '1'), customer),
     (membero,('Reverend', var(), var(), '3'), customer),
     (membero,('Reverend', var(), var(), '4'), customer)),
    # Clue5 The Sergeant either ordered Hibiscus Soap-on-a-Rope or is 4th priority.
    (lany,(membero,('Sergeant', var(), 'Hibiscus Soap-on-a-Rope', var()), customer),
     (membero,('Sergeant', var(), var(), '4'), customer)),
    # Clue7a Dimmadome is not a Doctor
    (lany,(membero,('Baroness', 'Dimmadome', var(), var()), customer),
     (membero,('Sergeant', 'Dimmadome', var(), var()), customer),
     (membero,('Reverend', 'Dimmadome', var(), var()), customer)),
    # Clue7b the Baroness didn't order the Hibiscus Soap-on-a-Rope.
    (lany,(membero,('Baroness', var(), 'Rose Bar', var()), customer),
     (membero,('Baroness', var(), 'Lemon Gel', var()), customer),
     (membero,('Baroness', var(), 'Chamomile Bar', var()), customer))
)    

solutions = run(1, customer, clues)

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