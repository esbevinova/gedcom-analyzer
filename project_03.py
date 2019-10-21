from prettytable import PrettyTable
from datetime import date
from datetime import datetime
from collections import defaultdict
import datetime as dt

invalid_date=[]

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

            for line_number, line in enumerate(file):
                line = line.rstrip('\n')    #Strip lines
                line = line.split()     #Split lines into tokent
                level = line[0]     #Assign first token to level
                tag = line[1]       #Assign second token to tag
                argument = line[2:]   #Assign comment to argument

                exceptns = ['INDI', 'FAM']  #Exceptions
                valid = {'0': ['HEAD', 'TRLR', 'NOTE'],  #Key: level, value: valid tags
                        '1': ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 
                        'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'],
                        '2': ['DATE']}

                if len(line) == 3 and line[0] == '0' and line[2] in exceptns: #Identify exceptions INDI and FAM
                    tag = line[2]       #For exceptions, switch places for tag and argument
                    argument = line[1]
                    good_line = [str(level), str(tag), str(argument), line_number + 1]
                    answer = tuple(good_line)

                else:   #Check if level and corresponding tag are valid
                    if level in valid:
                        if tag in valid[level]:
                            good_line = [str(level), str(tag), str(' '.join(argument)), line_number + 1]
                            answer = tuple(good_line)
                        else:   
                            continue
                    else:
                        continue
                yield answer
                
def valid_date (date):
        """ Check whether the date is valid or not 
        returns true if the date is valid
        returns false if the date is not valid"""
        if (date!=None)and(date!="NA"):
            try:
                date=datetime.strptime(date, "%d %b %Y").date()
                dt.datetime(date.year,date.month,date.day)
                return True
            except ValueError:
                invalid_date.append(date)
                return False

            
class Person():
    """Class Person"""

    pt_lables = ['ID', 'NAME', 'GENDER', 'BIRTHDAY', 'AGE', 
                'ALIVE', 'DEATH', 'CHILD', 'SPOUSE']

    def __init__(self, i_d, name, name_line, gender, gender_line, birthday, birthday_line, death, death_line, alive, 
                child, child_line, spouse, spouse_line):
        """Function init"""
        
        self.i_d = i_d
        self.name = name
        self.name_line = str(name_line)
        self.gender = gender
        self.gender_line = str(gender_line)
        self.birthday = birthday
        self.birthday_line = str(birthday_line)
        self.death = death
        self.death_line = str(death_line)
        self.alive = alive
        self.child = child
        self.child_line = str(child_line)
        self.spouse = spouse
        self.spouse_line = str(spouse_line)
        
        self.today = date.today()
        self.age = 'NA'

        self.get_age(self.birthday, self.death, self.today)     

    def get_age(self, birthday, death, today):
        """Function uses birthday date, death date and today's date to calculate
        age of the person or age of the person at death"""
        
        if self.birthday == 'NA':
            self.age = 'NA'
        elif valid_date(self.birthday)== True:
            birthday = datetime.strptime(self.birthday, '%d %b %Y')     #Convert birthday to datetime format             
            if self.death == 'NA':   #Calculate age if person is alive
                self.age = self.today.year - birthday.year - ((self.today.month, self.today.day) < (birthday.month, birthday.day))
            elif valid_date(self.death)==True: #Check for date of death and if such data available calculate age at time of death
                death = datetime.strptime(self.death, '%d %b %Y')   #Convert death to datetime format
                self.age = death.year - birthday.year - ((death.month, death.day) < (birthday.month, birthday.day))
        return self.age
        
    def pt_row(self):
        """Function creates a row for person table"""
        
        if valid_date(self.birthday)!=True:
            self.birthday = None
        else:
            self.birthday= self.birthday
        if valid_date(self.death)!=True:
            self.death = None
        else:
            self.death=self.death
        return [self.i_d, self.name, self.gender, self.birthday, self.age, self.alive, self.death, self.child, self.spouse]


class Family():
    """Class Family"""

    pt_lables = ['ID', 'MARRIED', 'DIVORCED', 'HUSBAND ID', 
                'HUSBAND NAME', 'WIFE ID', 'WIFE NAME', 'CHILDREN']

    def __init__(self, i_d, i_d_line, married, married_line, divorced, divorced_line, husb_id, husb_id_line, 
                                    wife_id, wife_id_line, children, children_lines):
        """Function init"""

        self.i_d = i_d
        self.i_d_line = i_d_line
        self.married = married 
        self.married_line = str(married_line)
        self.divorced = divorced
        self.divorced_line = str(divorced_line)
        self.husb_id = husb_id
        self.husb_id_line = str(husb_id_line)
        self.husb_name = 'NA'
        self.wife_id = wife_id
        self.wife_id_line = str(wife_id_line)
        self.wife_name = 'NA'
        self.children = children
        self.children_lines = str(children_lines)

    def pt_row(self, people):
        """Function creates a row for family table"""
        
        if valid_date(self.married)!=True:
            self.married = None
        else:
            self.married=self.married

        if valid_date(self.divorced)!=True:
            self.divorced = None
        else:
            self.divorced=self.divorced
        return [self.i_d, self.married, self.divorced, self.husb_id, people[self.husb_id].name, self.wife_id, people[self.wife_id].name, self.children]


class Classification():
    """Class parses through data in GEDCOM file,
    creates instances of class Person for 'INDI' data,
    creates instances of class Family for 'FAM' data"""

    def __init__(self, file_name):
        """Function init""" 
        filtered_file = valid_tag(file_name)

        valid_lines = [] 
        for line in filtered_file:
            valid_lines.append(line)    #Combine valid data lines into a list of elements

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
        
        name = 'NA'
        name_line = 0
        gender = 'NA'
        gender_line = 0
        birthday = 'NA'
        birthday_line = 0
        death = 'NA'
        death_line = 0
        alive = True
        child = 'NA'
        child_line = 0
        spouse = 'NA'
        spouse_line = 0

        i_d_line = 0
        married = 'NA'
        married_line = 0
        divorced = 'NA'
        divorced_line = 0
        husb_id = 'NA'
        husb_id_line = 0
        wife_id = 'NA'
        wife_id_line = 0

        children = []
        children_lines = []
         
        for key, value in self.entity.items():  #Person entity
            if key[1] == 'INDI':    
                for value in self.entity.values():      
                    for i in value:
                        if i[0] == '1' and i[1] == 'NAME':  #get person name
                            name = i[2]
                            name_line = i[3]
                        elif i[0] == '1' and i[1] == 'SEX': #get person gender
                            gender = i[2]
                            gender_line = i[3]
                        elif i[0] == '1' and i[1] == 'BIRT':    #get person birthday
                            b = value.index(i)
                            birth = value[b + 1]
                            if birth[0] == '2' and birth[1] == 'DATE' and (valid_date(birth[2])==True):  #check if birthday date is available 
                                birthday = birth[2] 
                                birthday_line = birth[3]
                            else:
                                continue
                        elif i[0] == '1' and i[1] == 'DEAT':    #get person death
                            d = value.index(i)
                            dth = value[d + 1]
                            if dth[0] == '2' and dth[1] == 'DATE' and (valid_date(dth[2])==True):  #check if death date is available
                                death = dth[2]
                                death_line = dth[3]
                                alive=False

                            else:
                                continue 
                        elif i[0] == '1' and i[1] == 'FAMC': #get id of the family the person was born into
                            child = i[2]
                            child_line = i[3]
                        elif i[0] == '1' and i[1] == 'FAMS': #get id of the family the person is a spouse in
                            spouse = i[2]
                            spouse_line = i[3]
                        elif i[0] == '2' and i[1] == 'DATE':
                            continue

                self.people[key[2]] = Person(key[2], name, name_line, gender, gender_line, birthday, birthday_line,
                                 death, death_line, alive, child, child_line, spouse, spouse_line)  #create an instance of class person

            #Family entity
            elif key[1] == 'FAM':
                i_d_line = key[3]
                for value in self.entity.values():    
                    for i in value:
                        if i[0] == '1' and i[1] == 'MARR':    #get marriage date
                            m = value.index(i)
                            mar = value[m + 1]
                            if mar[0] == '2' and mar[1] == 'DATE' and (valid_date(mar[2])==True):  #check if marriage is available
                                married = mar[2]
                                married_line = mar[3]
                            else:
                                continue 
                        elif i[0] == '1' and i[1] == 'HUSB':    #get husband id
                            husb_id = i[2]
                            husb_id_line = i[3]
                        elif i[0] == '1' and i[1] == 'WIFE':    #get wife id
                            wife_id = i[2]
                            wife_id_line = i[3]
                        elif i[0] == '1' and i[1] == 'CHIL':    #get children id
                            children.append(i[2])
                            children_lines.append(i[3])
                        elif i[0] == '1' and i[1] == 'DIV':    #get divorce date
                            d = value.index(i)
                            dv = value[d + 1]
                            if dv[0] == '2' and dv[1] == 'DATE' and (valid_date(dv[2])== True):  #check if divorce is available
                                divorced = dv[2]
                                divorced_line = dv[3]
                            else:
                                divorced = 'NA'
                    
                self.families[key[2]] = Family(key[2], i_d_line, married, married_line, divorced, divorced_line, husb_id, husb_id_line, 
                                    wife_id, wife_id_line, children, children_lines)   #create an instance of class family
                children = []
                children_lines = []
        self.entity.clear()

    def date_format(self, old_date):
        """function helps to format the date once used by us01 & us03"""
        
        if valid_date(old_date)== True:
            new_date = datetime.strptime(old_date, '%d %b %Y').date()     
            return new_date
        
    def before_today(self, date , today):
        """ function to check if the date occuers in the future"""
        """ if the date is greater than today will return false"""
        dt = self.date_format(date)
        today = self.date_format(today)  # calling date_format to format date of today as others dates

        if dt == "NA" or dt == None:
            return True

        return dt < today #return false
    
    def us01_before_current_dates(self,today):
        """ US01 Dates (birth, marriage, divorce, death) should not be after the current date"""
        today = date.today() #retrieve the current day
        today = today.strftime('%d %b %Y') #give current day in string format
        false_result = list() #list save all the incorrect dates to use for testcase

        for person in self.people.values():
            if self.before_today(person.birthday, today) == True: #if the birth == 'NA' or None skip
                continue
            else:
                    print ("ERROR: INDIVIDUAL: US01: ID: {} : Birthday {}: on line ({}): Occurs in the future".format(person.i_d, person.birthday, person.birthday_line))
                    false_result.append('INDI BIRTH ERROR')

        for person in self.people.values():
            if self.before_today(person.death, today) == True:
                continue
            else:
                    print ("ERROR: INDIVIDUAL: US01: ID: {} : Death {}: on line({}) Occurs in the future".format(person.i_d, person.death, person.death_line))
                    false_result.append('INDI DEAT ERROR')
 
        for family in self.families.values():
            if self.before_today(family.married, today) == True:
                continue
            else:
                    print ("ERROR: FAMILY: US01: ID: {} : Marriage date {} on line ({}) Occurs in the future".format(family.i_d, family.married, family.married_line))
                    false_result.append('FAM MARR ERROR')

            if self.before_today(family.divorced, today) == True:
                continue
            else:
                    print ("ERROR: FAMILY: US01: ID: {} : Divorce date {} on line ({}) Occurs in the future".format(family.i_d, family.divorced, family.divorced_line))
                    false_result.append('FAM DIVO ERROR')  

        return false_result   

    def getting_children_lines(self):
        """For future references"""
        for family in self.families.values():
            print(family.i_d)
            for ch, chl in zip(family.children, family.children_lines):
                print(ch, chl)     

    def us02_birth_before_marriage(self):
        """US02: Check if birth occurs before marriage of an individual"""
        """
        for family in self.families.values():
            if self.people[family.husb_id].birthday == 'NA' or family.married == None or self.people[family.wife_id].birthday == 'NA' or self.people[family.wife_id].birthday == None or self.people[family.husb_id].birthday == None:
                continue
            elif(valid_date(self.people[family.husb_id].birthday)==True)and(valid_date(family.married)):
                husb_birth = self.date_format(self.people[family.husb_id].birthday)
                wife_birth = self.date_format(self.people[family.wife_id].birthday)
                marriage = self.date_format(family.married)
                if husb_birth > marriage:
                    yield ("ERROR: FAMILY: US02: ID: {} - Husband's birth date {} on line {} occurs after his marriage date {} on line {}".format(family.husb_id, husb_birth, self.people[family.husb_id].birthday_line, marriage, family.married_line))               
                if wife_birth > marriage:
                    yield ("ERROR: FAMILY: US02: ID: {} - Wife's birth date {} on line {} occurs after her marriage date {} on line {}".format(family.wife_id, wife_birth, self.people[family.wife_id].birthday_line, marriage, family.married_line))
                else:
                    continue  
        """
        for family in self.families.values():
            if family.married == None or family.married == "NA":
                continue
            else:
                marriage = self.date_format(family.married)
                if self.people[family.wife_id].birthday == 'NA' or self.people[family.wife_id].birthday == None:
                    continue
                else:
                    if valid_date(self.people[family.wife_id].birthday) and valid_date(family.married):
                        wife_birth = self.date_format(self.people[family.wife_id].birthday)
                        if wife_birth > marriage:
                            yield ("ERROR: FAMILY: US02: ID: {} - Wife's birth date {} on line {} occurs after her marriage date {} on line {}".format(family.wife_id, wife_birth, self.people[family.wife_id].birthday_line, marriage, family.married_line))
                        
                if self.people[family.husb_id].birthday == 'NA' or self.people[family.husb_id].birthday == None:
                    continue
                else:
                    if valid_date(self.people[family.husb_id].birthday) and valid_date(family.married):
                        husb_birth = self.date_format(self.people[family.husb_id].birthday)
                        if husb_birth > marriage:
                            yield ("ERROR: FAMILY: US02: ID: {} - Husband's birth date {} on line {} occurs after his marriage date {} on line {}".format(family.husb_id, husb_birth, self.people[family.husb_id].birthday_line, marriage, family.married_line))                             
            
    def us03_birth_before_death(self):
        """US03 Birth should occur before death of an individual"""

        for person in self.people.values():
            if person.birthday == 'NA' or person.death == 'NA':
                continue
            elif(valid_date(person.birthday)==True)and(valid_date(person.death)==True):
                birth = self.date_format(person.birthday)
                death = self.date_format(person.death)
                if death < birth:
                    yield ("ERROR: INDIVIDUAL: US03: {}: Died on {}: line ({}): before born on {}".format(person.i_d, person.death, person.death_line, person.birthday)) 
                else:
                    continue

    def us04_marriage_before_divorse(self):
        """User story 04: Function that checks if marriage occurs before divorce of spouses, and if divorce occurs after marriage"""
        for family in self.families.values():
            if family.married == 'NA' or family.divorced == 'NA':
                continue
            else:
                if valid_date(family.married)==True:
                    married = self.date_format(family.married) 
                    if valid_date(family.divorced)==True:
                        divorced = self.date_format(family.divorced) 
                        time_married = divorced.year - married.year - ((divorced.month, divorced.day) < (married.month, married.day))       
                        if time_married < 0:
                            yield "ERROR: FAMILY: US04: {}: Divorced on {} (line {}) before married on {} (line {})".format(family.i_d, family.divorced, family.divorced_line, family.married, family.married_line)
                        else:
                            continue
                            
    def us05_marriage_before_death(self):
        """User story 05: Function that checks if marriage occurs before death of spouses"""
        for family in self.families.values():
            for person in self.people.values():
                if family.husb_id == person.i_d:
                    if (valid_date(person.death) == True) and (valid_date(family.married) == True):
                        married = self.date_format(family.married) 
                        death = self.date_format(person.death) 
                        if (married > death) == True:
                            yield "ERROR: FAMILY: US05: {}: Married on {} (line {}) after Death of Husband on {} (line {})".format(family.i_d, married, family.married_line, death, person.death_line)
                        else:
                            continue
                elif family.wife_id == person.i_d:
                    if (valid_date(person.death) == True) and (valid_date(family.married) == True):
                        married = self.date_format(family.married) 
                        death = self.date_format(person.death)
                        if (married > death) == True:
                            yield "ERROR: FAMILY: US05: {}: Married on {} (line {}) after Death of Wife on {} (line {})".format(family.i_d, married, family.married_line, death, person.death_line)
                        else:
                            continue
    
    def us06_divorce_before_death(self):
        """User story 06: Function that checks if divorce occurs before death of spouses"""
        for family in self.families.values():
            for person in self.people.values():
                if family.husb_id == person.i_d:
                    if (valid_date(person.death) == True) and (valid_date(family.divorced) == True):
                        divorced = self.date_format(family.divorced) 
                        death = self.date_format(person.death)
                        if (divorced > death) == True:
                            yield "ERROR: FAMILY: US06: {}: Divorced on {} (line {}) after Death of Husband on {} (line {})".format(family.i_d, divorced, family.divorced_line, death, person.death_line)
                        else:
                            continue
                elif family.wife_id == person.i_d:
                    if (valid_date(person.death) == True) and (valid_date(family.divorced) == True):
                        divorced = self.date_format(family.divorced) 
                        death = self.date_format(person.death)
                        if (divorced > death) == True:
                            yield "ERROR: FAMILY: US06: {}: Divorced on {} (line {}) after Death of Wife on {} (line {})".format(family.i_d, divorced, family.divorced_line, death, person.death_line)
                        else:
                            continue

    def us07_over150(self):
        """User story 07 checks for persons age and returns an error if a person is over 150 years old, 
        or was over 150 years old at time of death"""
        for person in self.people.values():
            if person.age == 'NA':
                continue
            else:
                if person.alive and person.age > 150:
                    yield "ERROR: INDIVIDUAL: US07: {} More than 150 years old: Birthday {} (line {})".format(person.i_d, person.birthday, person.birthday_line)
                elif person.alive==False and person.age > 150:
                    yield "ERROR: INDIVIDUAL: US07: {} More than 150 years old at death: Birthday {} (line {}), Death date {} (line {})".format(person.i_d, 
                    person.birthday, person.birthday_line, person.death, person.death_line)
                else:
                    continue
    
    def us10_marriage_after14(self):
        """Checks if marriage took place at least 14 years after birth of both spouses (parents must be at least 14 years old)"""
        """for family in self.families.values():
            if self.people[family.husb_id].birthday == 'NA' or self.people[family.wife_id].birthday == 'NA' or self.people[family.husb_id].birthday == None or self.people[family.wife_id].birthday == None or family.married == None or family.married == 'NA':
                continue
            else:
                marriage_date = self.date_format(family.married)      
                husb_age = self.date_format(self.people[family.husb_id].birthday)              
                wife_age = self.date_format(self.people[family.wife_id].birthday)
                husb_age_at_marriage = (marriage_date - husb_age).days/365.25
                wife_age_at_marriage = (marriage_date - wife_age).days/365.25
                if husb_age_at_marriage < 14:
                    yield "ERROR: FAMILY: US10: ID: {}: husband's age is less than 14 years old at the time of marriage {} (line {})".format(family.i_d, family.married, family.married_line)
                if wife_age_at_marriage < 14:
                    yield "ERROR: FAMILY: US10: ID: {}: wife's age is less than 14 years old at the time of marriage {} (line {})".format(family.i_d, family.married, family.married_line)
                else:
                    continue
        """
        for family in self.families.values():
            if family.married == None or family.married == 'NA':
                continue
            else:
                marriage_date = self.date_format(family.married)
                if self.people[family.husb_id].birthday == 'NA' or self.people[family.husb_id].birthday == None:
                    continue
                else:      
                    husb_age = self.date_format(self.people[family.husb_id].birthday)              
                    husb_age_at_marriage = (marriage_date - husb_age).days/365.25
                    if husb_age_at_marriage < 14:
                        yield "ERROR: FAMILY: US10: ID: {}: husband's age is less than 14 years old at the time of marriage {} (line {})".format(family.i_d, family.married, family.married_line)

                if self.people[family.wife_id].birthday == 'NA' or self.people[family.wife_id].birthday == None:
                    continue
                else:
                    wife_age = self.date_format(self.people[family.wife_id].birthday)
                    wife_age_at_marriage = (marriage_date - wife_age).days/365.25
                    if wife_age_at_marriage < 14:
                        yield "ERROR: FAMILY: US10: ID: {}: wife's age is less than 14 years old at the time of marriage {} (line {})".format(family.i_d, family.married, family.married_line)

    def us12_parents_not_too_old(self):
        """Mother should be less than 60 years older than her children and father should be less than 80 years older than his children"""
        for family in self.families.values():
            if self.people[family.husb_id].birthday == 'NA' or self.people[family.husb_id].birthday == None:
                continue
            else:
                if valid_date(self.people[family.husb_id].birthday)==True:
                    fathers_birthday = self.date_format(self.people[family.husb_id].birthday)
                    for child in family.children:
                            if self.people[child].birthday == 'NA' or self.people[child].birthday == None or valid_date(self.people[child].birthday) == False:
                                continue
                            else:
                                child_birthday = self.date_format(self.people[child].birthday)
                                if self.date_within(fathers_birthday, child_birthday, 80, 'years'):
                                    continue
                                else:
                                    yield "ERROR: FAMILY: US12: ID: {} Father's birthday {} (line {}) occurs more than 80 years before his child's birthday {} (line {})".format(self.people[family.husb_id].i_d, self.people[family.husb_id].birthday, self.people[family.husb_id].birthday_line, self.people[child].birthday, self.people[child].birthday_line)

            if self.people[family.wife_id].birthday == 'NA' or self.people[family.wife_id].birthday == None:
                continue
            else: 
                if valid_date(self.people[family.wife_id].birthday)==True:
                    mothers_age = self.date_format(self.people[family.wife_id].birthday)
                    for child in family.children:
                        if self.people[child].birthday == 'NA' or self.people[child].birthday == None or valid_date(self.people[child].birthday) == False:
                            continue
                        else:
                            child_birthday = self.date_format(self.people[child].birthday)
                            if self.date_within(mothers_age, child_birthday, 60, 'years'):
                                continue
                            else:
                                yield "ERROR: FAMILY: US12: ID: {} Mother's birthday {} (line {}) occurs more than 60 years before her child's birthday {} (line {})".format(self.people[family.wife_id].i_d, self.people[family.wife_id].birthday, self.people[family.wife_id].birthday_line, self.people[child].birthday, self.people[child].birthday_line)                      

    def us14_multiple_siblings(self):
        """User story 14: Function that checks if there are more than 5 siblings in the family."""
        same_birthdays = defaultdict(list)
        for family in self.families.values():
            if len(family.children) <= 5:
                continue
            else:
                for child in family.children:
                    child_found = self.people[child]
                    if child_found.birthday == 'NA' or child_found.birthday == None or valid_date(self.people[child].birthday)== False:
                        continue
                    else:
                        same_birthdays[child_found.birthday].append(child)
                    if len(same_birthdays[child_found.birthday]) > 5:
                        yield 'ERROR: FAMILY: US14: Family with ID {} on line {} has more than 5 siblings with the same birthday'.format(family.i_d, family.i_d_line)

    def us27_individual_ages(self):
        """User story 27: Function that gets the age of a person"""
        for person in self.people.values():
            if person.age == 'NA' or person.age < 0:
                continue
            else:
                yield person.i_d, person.age

    def us27_ages_table(self):
        """User story 27: Function that prints us27_individual_ages() table"""
        pt = PrettyTable()
        pt.field_names = ["ID", "AGE"]
        for i_d, age in self.us27_individual_ages():
            pt.add_row([i_d, age])
        print('us27: Ages of individuals')
        print(pt)
    
    def us29_list_deceased(self):
        """"List all deceased individuals in a GEDCOM file"""
        today = date.today() #retrieve the current day
        today = today.strftime('%d %b %Y') #give current day in string format
        deceased =list() #list has all deceased individuls 

        for person in self.people.values():
            if self.before_today(person.death,today) == False or person.alive == True:
                continue
            else:
                deceased.append((person.name, person.death))

        return deceased

    def us30_list_living_married(self):
        """list all living married"""
        living_married = list()

        for family in self.families.values():
            wife_name = self.people[family.wife_id].name
            husb_name = self.people[family.husb_id].name

            if family.divorced == None or family.divorced == 'NA':
                if self.people[family.wife_id].alive == True:
                    living_married.append((family.wife_id, wife_name))
                else:
                    continue
            else:
                continue

            if family.divorced == None or family.divorced == 'NA':
                if self.people[family.husb_id].alive == True:
                    living_married.append((family.husb_id, husb_name))
                else:
                    continue
            else:
                continue

        return living_married   
    
    def us29_deceased_table(self):
        """User Story 29: Function prints list_deceased table"""
        pt = PrettyTable()
        pt.field_names = ["Name", "Death date"]
        for name, dt in self.us29_list_deceased():
            pt.add_row([name, dt])
        print("\nUS29: Individuals deceased")
        print(pt)

    def us30_living_married_table(self):
        """User Story 30: Function prints living_married table"""
        pt = PrettyTable()
        pt.field_names = ["ID", "Name"]
        for id, name in self.us30_list_living_married():
            pt.add_row([id, name])
        print("\nUS30: Living married")
        print(pt)

    def us31_living_singles(self):
        """User Story 31: List all living singles over 30 who have never been married in a GEDCOM file"""
        singles = list()
        for person in self.people.values():
            if person.alive and person.age != 'NA' and person.age != '' and int(person.age) > 30 and person.spouse == 'NA':
                singles.append((person.i_d,person.name))
        return singles
    
    def us32_multiple_births(self):
        """User Story 32: List all multiple births on the same date in a GEDCOM file"""
        birthdays = defaultdict(list)  # birthdays[date] = list of people with that birthday

        # add each person
        for person in self.people.values():
            if person.birthday == 'NA' or person.birthday == '' or person.birthday == None:
                continue
            else:
                birthdays[person.birthday].append(person.name)

        multiple_births = dict()  # multiple_births[date] = list of people with that birthday
        for dt, names in birthdays.items():
            if len(names) > 1:
                multiple_births[dt] = names

        return multiple_births
    
    def us31_singles_table(self):
        """User Story 31: Function prints living_singles() table"""
        pt = PrettyTable()
        pt.field_names = ["ID", "Name"]
        for id, name in self.us31_living_singles():
            pt.add_row([id, name])
        print("\n\nUS31: Individuals over 30 living single")
        print(pt)

    def us32_multiple_births_table(self):
        """User Story: 32: Function prints multiple_births() table"""
        pt = PrettyTable()
        pt.field_names = ['Birthdate', 'People']
        for dt, people in self.us32_multiple_births().items():
            pt.add_row([dt, people])
        
        print("\n\nUS32: People sharing birthdays")
        print(pt)
    
    def date_within(self, dt1, dt2, limit, units):
        """return True if dt1 and dt2 are within units where:
        dt1, dt2 are instances of datetime
        limit is a number
        units is a string in ("days","months","years")
        """
        if units == 'days':
            return (abs((dt1-dt2).days))<=limit
        elif units == 'months':
            return(abs((dt1-dt2).days)/30.4)<=limit
        elif units == 'years':
            return (abs((dt1-dt2).days)/365.25)<=limit

    def us35_recent_births(self):
        """User Story 35: List all the people in a GEDCOM file who were born in the last 30 days"""
        recent_births = defaultdict(list) 
        for person in self.people.values():
            if person.birthday == 'NA':
                continue
            elif(valid_date(person.birthday)==True):
                birthdate=datetime.strptime(person.birthday, "%d %b %Y").date()
                within = ( self.date_within(birthdate, datetime.today().date(), 30, 'days'))
                if within == True:
                    recent_births[person.birthday].append(person.name)
                else:
                    continue
        return recent_births

    def us35_recent_births_table(self):
        """User Story: 35: Function prints recent_births() table"""

        pt = PrettyTable()
        pt.field_names = ['Birthdate', 'People']
        for dt, people in self.us35_recent_births().items():
            pt.add_row([dt, people])
        
        print("\n\nUS35: People who were born in the last 30 days")
        print(pt)
        
    def us42_invalid_date_error(self):
        """User Story: 42: Function prints valid_date() Error"""
        for i in invalid_date:
            print ("Error: US42: {} is an invalid date".format(i))
                
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

    file_name = './test_results.ged'
    
    day = '24 Sep 2019'
    d1= datetime.strptime(day, '%d %b %Y')
    classify = Classification(file_name)
    
    classify.person_table() # print the person table
    classify.family_table() # print the families table
    
    # call each of the user stories
    classify.us01_before_current_dates(d1)
    for err in classify.us02_birth_before_marriage():
        print(err)
    for err in classify.us03_birth_before_death():
        print(err)
    for err in classify.us04_marriage_before_divorse():
        print(err)
    for err in classify.us05_marriage_before_death():
        print(err)
    for err in classify.us06_divorce_before_death():
        print(err)
    for err in classify.us07_over150():
        print(err)
    for err in classify.us10_marriage_after14():
        print(err)
    for err in classify.us12_parents_not_too_old():
        print(err)
    for err in classify.us14_multiple_siblings():
        print(err)
    classify.us27_ages_table()
    classify.us29_deceased_table()
    classify.us30_living_married_table()
    classify.us31_singles_table()
    classify.us32_multiple_births_table()
    classify.us35_recent_births_table()
    classify.us42_invalid_date_error()
       
if __name__ == '__main__':
    main()

