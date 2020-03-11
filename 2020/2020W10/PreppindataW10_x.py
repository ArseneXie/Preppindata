 from kanren import *
 from kanren.core import lall,lany
 
 def higher(a, b, list):
     return membero((a,b), zip(list, list[1:]))
 
 customer = var()
 
 clues = lall(
     # Solution with 4 fields: Title, LastName, Product, Priority and Dummy
     (eq, (var(), var(), var(), var(), var()), customer),  
     # All Values 
     (membero,('Baroness', var(), var(), var(), var()), customer),
     (membero,('Sergeant', var(), var(), var(), var()), customer),
     (membero,('Reverend', var(), var(), var(), var()), customer),
     (membero,('Doctor', var(), var(), var(), var()), customer),
     (membero,(var(), 'Bevens', var(), var(), var()), customer),
     (membero,(var(), 'Shadwell', var(), var(), var()), customer),
     (membero,(var(), 'Dimmadome', var(), var(), var()), customer),
     (membero,(var(), 'Rotzenheimer', var(), var(), var()), customer),
     (membero,(var(), var(), 'Rose Bar', var(), var()), customer),
     (membero,(var(), var(), 'Lemon Gel', var(), var()), customer),
     (membero,(var(), var(), 'Chamomile Bar', var(), var()), customer),
     (membero,(var(), var(), 'Hibiscus Soap-on-a-Rope', var(), var()), customer),
     (membero,(var(), var(), var(), var(), 'O'), customer),
     (membero,(var(), var(), var(), var(), 'X'), customer),
     # Priority 1 > 2 > 3 > 4 
     (higher,(var(), var(), var(), '1', var()), (var(), var(), var(), '2', var()), customer), 
     (higher,(var(), var(), var(), '2', var()), (var(), var(), var(), '3', var()), customer),
     (higher,(var(), var(), var(), '3', var()), (var(), var(), var(), '4', var()), customer),
     # Clue1a  customer with the highest priority has a title and last name that begin with the same letter
     (lany,(membero,('Baroness', 'Bevens', var(), '1', 'O'), customer),
      (membero,('Reverend', 'Rotzenheimer', var(), '1', 'O'), customer),
      (membero,('Sergeant', 'Shadwell', var(), '1', 'O'), customer),
      (membero,('Doctor', 'Dimmadome', var(), '1', 'O'), customer),
      (membero,('Baroness', 'Bevens', var(), var(), 'X'), customer),
      (membero,('Reverend', 'Rotzenheimer', var(), var(), 'X'), customer),
      (membero,('Sergeant', 'Shadwell', var(), var(), 'X'), customer),
      (membero,('Doctor', 'Dimmadome', var(), var(), 'X'), customer)), 
     # Clue2a Bevens' priority is directly after Dimmadome
     (higher,(var(), 'Dimmadome', var(), var(), var()), (var(), 'Bevens', var(), var(), var()), customer),
     # Clue2b Neither of these people ordered the Chamomile Bar or the Hibiscus Soap-on-a-Rope.
     (membero,(var(), 'Dimmadome', 'Chamomile Bar', var(), 'X'), customer),
     (membero,(var(), 'Dimmadome','Hibiscus Soap-on-a-Rope', var(), 'X'), customer),
     (membero,(var(), 'Bevens', 'Chamomile Bar', var(), 'X'), customer),
     (membero,(var(), 'Bevens', 'Hibiscus Soap-on-a-Rope', var(), 'X'), customer),
     # Clue3 The Sergeant and the person who ordered Lemon Gel are either 1st priority or 3rd priority
     (lany,(membero,('Sergeant', var(), var(), '1', 'O'), customer),
      (membero,('Sergeant', var(), var(), '3', 'O'), customer)),
     (lany,(membero,(var(), var(), 'Lemon Gel', '1', 'O'), customer),
      (membero,(var(), var(), 'Lemon Gel', '3', 'O'), customer)),
     # Clue4 The Reverend didn't order the Rose Bar and isn't 2nd priority.
     (membero,('Reverend', var(), 'Rose Bar', var(), 'X'), customer),
     (membero,('Reverend', var(), var(), '2', 'X'), customer),
     # Clue5 The Sergeant either ordered Hibiscus Soap-on-a-Rope or is 4th priority.
     (lany,(membero,('Sergeant', var(), 'Hibiscus Soap-on-a-Rope', var(), 'O'), customer),
      (membero,('Sergeant', var(), var(), '4', 'O'), customer)),
     # Clue6 The priority of the person who ordered the Rose Bar is directly after the person who ordered the Lemon Gel.
     (higher,(var(), var(), 'Lemon Gel', var(), var()), (var(), var(), 'Rose Bar', var(), var()), customer),
     # Clue7a Dimmadome is not a Doctor
     (membero,('Doctor', 'Dimmadome', var(), var(), 'X'), customer),
     # Clue7b the Baroness didn't order the Hibiscus Soap-on-a-Rope.
     (membero,('Baroness', var(), 'Hibiscus Soap-on-a-Rope', var(), 'X'), customer),
     
 )    
 
 solutions = run(0, customer, clues)