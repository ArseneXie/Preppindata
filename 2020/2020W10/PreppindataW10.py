from kanren import *
from kanren.core import lall
import pandas as pd

def higher(a, b, list):
    return membero((a,b), zip(list, list[1:]))

def any2(a, b, list):
    return conde([membero(a, list)],[membero(b, list)])

def any3(a, b, c, list):
    return conde([membero(a, list)],[membero(b, list)],[membero(c, list)])

def any4(a, b, c, d, list):
    return conde([membero(a, list)],[membero(b, list)],[membero(c, list)],[membero(d, list)])

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
    (any4,('Baroness', 'Bevens', var(), '1'),('Reverend', 'Rotzenheimer', var(), '1')
     ,('Sergeant', 'Shadwell', var(), '1'),('Doctor', 'Dimmadome', var(), '1'), customer),
    # Clue2a Bevens' priority is directly after Dimmadome
    (higher,(var(), 'Dimmadome', var(), var()), (var(), 'Bevens', var(), var()), customer),
    # Clue6 The priority of the person who ordered the Rose Bar is directly after the person who ordered the Lemon Gel.
    (higher,(var(), var(), 'Lemon Gel', var()), (var(), var(), 'Rose Bar', var()), customer),
    # Clue2b Neither of these people ordered the Chamomile Bar or the Hibiscus Soap-on-a-Rope.
    (any2, (var(), 'Dimmadome', 'Rose Bar', var()), (var(), 'Dimmadome','Lemon Gel', var()), customer),
    (any2, (var(), 'Bevens', 'Rose Bar', var()), (var(), 'Bevens', 'Lemon Gel', var()), customer),
    # Clue3 The Sergeant and the person who ordered Lemon Gel are either 1st priority or 3rd priority
    (any2, ('Sergeant', var(), var(), '1'), ('Sergeant', var(), var(), '3'), customer),
    (any2, (var(), var(), 'Lemon Gel', '1'), (var(), var(), 'Lemon Gel', '3'), customer),
    # Clue4a The Reverend didn't order the Rose Bar.
    (any3, ('Reverend', var(), 'Lemon Gel', var()), ('Reverend', var(), 'Chamomile Bar', var()),
     ('Reverend', var(), 'Hibiscus Soap-on-a-Rope', var()), customer),
    # Clue4b And the Reverend isn't 2nd priority.
    (any3, ('Reverend', var(), var(), '1'), ('Reverend', var(), var(), '3'), ('Reverend', var(), var(), '4'), customer),
    # Clue5 The Sergeant either ordered Hibiscus Soap-on-a-Rope or is 4th priority.
    (any2, ('Sergeant', var(), 'Hibiscus Soap-on-a-Rope', var()), ('Sergeant', var(), var(), '4'), customer),
    # Clue7a Dimmadome is not a Doctor
    (any3, ('Baroness', 'Dimmadome', var(), var()), ('Sergeant', 'Dimmadome', var(), var()),
     ('Reverend', 'Dimmadome', var(), var()), customer),
    # Clue7b the Baroness didn't order the Hibiscus Soap-on-a-Rope.
    (any3, ('Baroness', var(), 'Rose Bar', var()), ('Baroness', var(), 'Lemon Gel', var()),
     ('Baroness', var(), 'Chamomile Bar', var()), customer)
)    

solutions = run(0, customer, clues)

for s in solutions:
    df = pd.DataFrame(s, columns = ['Title', 'LastName', 'Product', 'Priority']) 
    df['Clue1b'] = df.apply(lambda x: not(x['Title'][0:1]==x['LastName'][0:1] and x['Priority']!='1'), axis=1)
    df = df[df['Clue1b']].drop('Clue1b',axis=1)
    if len(df)==4:
        final = df.copy()
        print(df)
