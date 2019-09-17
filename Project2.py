"""
Project 2
Practice programming with GEDCOM data
"""

def valid_tag(file_name):
    """The function reads .ged file line by line,
    checks for the validity of the tags in the file,
    checks if the tags are correspondent to the appropriate level.
    If the tag is valid, the result is returned as <level>|<tag>|'Y'|<argument>,
    if the tag is invalid, the result is returned as <level>|<tag>|'N'|<argument>.
    For the level 0 data in format <level><id><tag> the result is returned 
    in the format of <level>|<tag>|Y/N|<id>.
    The result is returned in the format of an input line followed by 
    a line with evaluated answer."""

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
                    val = 'Y'
                    
                  
                else:   #Check if level and corresponding tag are valid
                    if level in valid:
                        if tag in valid[level]:
                            val = 'Y'
                        else:   
                            val = 'N'
                    else:
                        val = 'N'


                validation = [str(level), str(tag), str(val), str(' '.join(argument))]
                line = ' '.join(line) #Format the input line
                answer = '|'.join(validation)   #Format evaluation line
                print(line)
                yield answer


def main():
    """Main function calls valid_tag function and prints the results"""

    file_name = '/Users/nadik/Desktop/gedcom-analyzer/Project1.ged'
    for line in valid_tag(file_name):
        print(line)

main()