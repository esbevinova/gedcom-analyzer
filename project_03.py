from prettytable import PrettyTable
from datetime import date
from datetime import datetime

def valid_tag(file_name):
    """Function reads .ged file line by line,
    checks for the validity of the tags in the file,
    checks if the tags are correspondent to the appropriate level.
    For the level 0 data in format <level><id><tag> the result is returned 
    in the format of <level>|<tag>|<id>.
    Only lines with valid data are returned."""

    try:
        file = open(file_name, 'r') #Open file
    except FileNotFoundError:
        print('Cannot open file ', file_name)
    else:
        with file:

            for line in file:
                line = line.rstrip('\n')    #Strip lines
                line = line.split()     #Split lines into tokent
                level = line[0]     #Assign first token to level
                tag = line[1]       #Assign second token to tag
                argument = line[2:] #Assign comment to argument

                exceptns = ['INDI', 'FAM']  #Exceptions
                valid = {'0': ['HEAD', 'TRLR', 'NOTE'],  #Key: level, value: valid tags
                        '1': ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 
                        'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'],
                        '2': ['DATE']}

                if len(line) == 3 and line[0] == '0' and line[2] in exceptns: #Identify exceptions INDI and FAM
                    tag = line[2]       #For exceptions, switch places for tag and argument
                    argument = line[1]
                    good_line = [str(level), str(tag), str(argument)]
                    answer = tuple(good_line)

                else:   #Check if level and corresponding tag are valid
                    if level in valid:
                        if tag in valid[level]:
                            good_line = [str(level), str(tag), str(' '.join(argument))]
                            answer = tuple(good_line)
                        else:   
                            continue
                    else:
                        continue
                yield answer


class Person():
    """Class Person"""

    pt_lables = ['ID', 'NAME', 'GENDER', 'BIRTHDAY', 'AGE', 
                'ALIVE', 'DEATH', 'CHILD', 'SPOUSE']

    def __init__(self, i_d, name, gender, birthday, death, child, spouse):
        """Function init"""
        
        self.i_d = i_d
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.death = death
        self.child = child
        self.spouse = spouse

        self.today = date.today()
        self.age = ''
        self.alive = bool

        self.get_age(self.birthday, self.death, self.today)
        

    def get_age(self, birthday, death, today):
        """Function uses birthday date, death date and today's date to calculate
        age of the person or age of the person at death"""

        if len(self.birthday) > 0:  #Check for birthday data
            birthday = datetime.strptime(self.birthday, '%d %b %Y')     #Convert birthday to datetime format
            if len(self.death) > 0: #Check for date of death and if such data available calculate age at time of death
                death = datetime.strptime(self.death, '%d %b %Y')   #Convert death to datetime format
                self.age = death.year - birthday.year - ((death.month, death.day) < (birthday.month, birthday.date))
            else:   #Calculate age if person is alive
                self.age = self.today.year - birthday.year - ((self.today.month, self.today.day) < (birthday.month, birthday.date))
            return self.age
        else:
            return 'NA'


    def pt_row(self):
        """Function creates a row for person table"""

        if len(self.death) > 0:     #Check if date of death is available, else assign 'NA'
            self.death = self.death
            self.alive = False           #Get True/False for alive value
        else:
            self.death = 'NA'
            self.alive = True

        if len(self.gender) > 0:    #Check if person gender is available, else assign 'NA'
            self.gender = self.gender
        else:
            self.gender = 'NA'

        if len(self.birthday) > 0:  #Check if person birthday is available, else assign 'NA for birthday and age'
            self.birthday = self.birthday
        else:
            self.birthday = 'NA'
            self.age = 'NA'

        if len(self.child) > 0:     #Check if parents' family id is available, else assign 'NA'
            self.cild = self.child
        else:
            self.child = 'NA'

        if len(self.spouse) > 0:    #Check if person is married and what is the family id, else assign 'NA'
            self.spouse = self.spouse
        else:
            self.spouse = 'NA'
  
        return [self.i_d, self.name, self.gender, self.birthday, self.age, self.alive, self.death, self.child, self.spouse]

   


class Family():
    """Class Family"""

    pt_lables = ['ID', 'MARRIED', 'DIVORCED', 'HUSBAND ID', 
                'HUSBAND NAME', 'WIFE ID', 'WIFE NAME', 'CHILDREN']

    def __init__(self, i_d, married, divorced, husb_id, wife_id, children):
        """Function init"""

        self.i_d = i_d
        self.married = married 
        self.divorced = divorced
        self.husb_id = husb_id
        self.husb_name = ''
        self.wife_id = wife_id
        self.wife_name = ''
        self.children = children

    def pt_row(self, people):
        """Function creates a row for family table"""
        if len(self.married) > 0:   #Check if marriage date is available, else assign 'NA'
            self.married = self.married
        else:
            self.married = 'NA'

        if len(self.divorced) > 0:  #Check if divorce date is available, else assign 'NA'
            divorced = self.divorced
        else:
            divorced = 'NA'

        if len(self.children) > 0:  #Check for children in the family, else assign 'NA'
            self.children = self.children
        else:
            self.children = 'NA'

        return [self.i_d, self.married, divorced, self.husb_id, people[self.husb_id].name, self.wife_id, people[self.wife_id].name, self.children]



class Classification():
    """Class parses through data in GEDCOM file,
    creates instances of class Person for 'INDI' data,
    creates instances of class Family for 'FAM' data"""

    def __init__(self, valid_lines):
        """Function init"""
        self.valid_lines = valid_lines
        self.people = dict()
        self.families = dict()

        self.entity = dict()
        self.get_entities(valid_lines)


    def get_entities(self, valid_lines):
        """Function parses through a list of data from a GEDCOM file
        and devides it into separate entities.
        A new entity starts with an element of data that has level 0"""
        info = []
    
        for i in self.valid_lines:       
            if i[0] == '0' and len(self.entity) == 0:                
                self.entity[i] = info
            elif i[0] == '1' or i[0] == '2':
                info.append(i)
            elif i[0] == '0' and len(self.entity) > 0: 
                self.make_entity(self.entity)
                info = []
                self.entity[i] = info
                continue
                
                       
    def make_entity(self, entity):
        """Function parses through data in self.entity dictionary,
        for 'INDI' data an instance of class person is created,
        for 'FAM' data an instance of class family is created"""
        
        name = ''
        gender = ''
        birthday = ''
        death = ''
        child = ''
        spouse = ''

        married = ''
        divorced = ''
        husb_id = ''
        wife_id = ''
        children = []
        
        
        for key, value in self.entity.items():
            #Person entity
            if key[1] == 'INDI':    
                for value in self.entity.values():      
                    for i in value:
                        if i[0] == '1' and i[1] == 'NAME':  #get person name
                            name = i[2]
                        elif i[0] == '1' and i[1] == 'SEX': #get person gender
                            gender = i[2]
                        elif i[0] == '1' and i[1] == 'BIRT':    #get person birthday
                            b = value.index(i)
                            birth = value[b + 1]
                            if birth[0] == '2' and birth[1] == 'DATE':  #check if birthday date is available 
                                birthday = birth[2] 
                            else:
                                continue
                        elif i[0] == '1' and i[1] == 'DEAT':    #get person death
                            d = value.index(i)
                            dth = value[d + 1]
                            if dth[0] == '2' and dth[1] == 'DATE':  #check if death date is available
                                death = dth[2]
                            else:
                                continue 
                        elif i[0] == '1' and i[1] == 'FAMC': #get id of the family the person was born into
                            child = i[2]
                        elif i[0] == '1' and i[1] == 'FAMS': #get id of the family the person is a spouse in
                            spouse = i[2]
                        elif i[0] == '2' and i[1] == 'DATE':
                            continue

                self.people[key[2]] = Person(key[2], name, gender, birthday, death, 
                                child, spouse)  #create an instance of class person

            #Family entity
            elif key[1] == 'FAM':
                for value in self.entity.values():    
                    for i in value:
                        if i[0] == '1' and i[1] == 'MARR':    #get marriage date
                            m = value.index(i)
                            mar = value[m + 1]
                            if mar[0] == '2' and mar[1] == 'DATE':  #check if marriage is available
                                married = mar[2]
                            else:
                                continue 
                        elif i[0] == '1' and i[1] == 'HUSB':    #get husband id
                            husb_id = i[2]
                        elif i[0] == '1' and i[1] == 'WIFE':    #get wife id
                            wife_id = i[2]
                        elif i[0] == '1' and i[1] == 'CHIL':    #get children id
                            children.append(i[2])
                        elif i[0] == '1' and i[1] == 'DIV':    #get divorce date
                            d = value.index(i)
                            dv = value[d + 1]
                            if dv[0] == '2' and dv[1] == 'DATE':  #check if divorce is available
                                divorced = dv[2]
                            else:
                                divorced = 'NA'

                    
                self.families[key[2]] = Family(key[2], married, divorced, husb_id, 
                                    wife_id, children)   #create an instance of class family
                children = []
        self.entity.clear()


    def person_table(self):
        """Function prints people table """
        pt = PrettyTable()
        pt.field_names=Person.pt_lables
        for person in self.people.values():
            pt.add_row(person.pt_row())
        print(pt)

    def family_table(self):
        """Function prints families table """
        pt = PrettyTable()
        pt.field_names=Family.pt_lables
        for family in self.families.values():
            pt.add_row(family.pt_row(self.people))

        print(pt)




def main():
    """Main function calls valid_tag function and prints the results"""

    file_name = '/Users/nadik/Desktop/555/Project1_Nadia_Vedeneyeva.ged'
    valid_lines = []    

    filtered_file = valid_tag(file_name)
    for line in filtered_file:
        valid_lines.append(line)    #Combine valid data lines into a list of elements

    classify = Classification(valid_lines)

    classify.person_table()
    classify.family_table()

main()