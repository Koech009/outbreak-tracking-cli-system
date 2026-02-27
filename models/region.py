# 2:20–2:50 | Build the Region Class
# Write your __init__ with all four attributes. 
# Then think about what methods a Region logically needs: 
# It should be able to add a case, remove a case, and probably return a summary of itself. 
# Write those method signatures with docstrings first:
#  — describe what each one does, takes, and returns — before writing any logic. 
# This is called design before implementation and it forces clarity.
# The key concept here is encapsulation — the Region manages its own list of cases. 
# Nothing outside should directly append to region.list_of_cases; they should call region.add_case(). 
# Ask yourself why that matters.
    #this encapsulation matters because it prevents regional cases from getting mixed up and has each region as an independent
    #entity ummm, i honestly can't think of another reason.
    #main reason: If outside code can directly do region.list_of_cases.append(case_id), 
                  # you have no way to validate, log, or add logic to that action later. 
                  # If everything goes through region.add_case(), that method becomes a single controlled entry point 
                  # — you can add duplicate checking, error handling, or logging there and it automatically applies everywhere. 
                  # That's the real power.

#questions
#1. in what scenario would we need to remove a case...? cause this is an outbreak tracker... sooo, shouldn't add be the only 
    #method. i can't think of where removing a case comes in...? cause this is focused on catching the new cases so removal seems
    #out of scope here. or is there something i'm missing?

#2. region name and location... hmmm i feel redundancy there. like nyeri region is in nyeri location so what actually gives...?
    #what would be a better more meaningful attribute to replace it with? population maybe? i can't think of another one atm...

#to implement later:
    #validation handling in add_case
class Region:
    def __init__(self, id, name, population):
        self.id = id
        self.name = name
        self.population = population
        self.case_list = []
    #methods to add a case, remove a case, return a self-summary
    def add_case(self, case):
        """Does: This method adds a case to its cases list
           Takes: the instance and a case object
           Returns: A success message stating that the case has been added"""
        if case.id in self.case_list:
            return 
        
        self.case_list.append(case.id)
        return "The case has succesfully been added to the regional list"
        
    def remove_case(self, case):
        """Does: This method removes a case from its cases list
           Takes: the instance and a case object
           Returns: A success message stating that the case has been removed"""
        to_remove = [id for id in self.case_list if id == case.id]
        self.case_list.remove(to_remove)
        return "The case has succesfully been removed from the regional list"
        
    def region_summary(self):
        """Does: This methods gives a summary of the region's stats
           Takes: the instance
           Returns a formatted string summary of all the attributes of the instance"""
        return f"Region Info: {self.name} region has a population of {self.population} people and currently has {len(self.case_list)} outbreaks."
    
    