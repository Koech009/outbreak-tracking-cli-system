# Write two or three lines in a scratch file that manually instantiate a Region, add a case ID, call to_dict(), and print it. 
# Make sure it looks like what you'd expect to see in a JSON file.

from region import Region

region1 = Region(568," Nyeri", 500000)
region1.case_list = [237, 458, 273]
dictionary = region1.to_dict()
print(dictionary)