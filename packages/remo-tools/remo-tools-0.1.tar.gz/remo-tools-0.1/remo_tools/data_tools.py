import re
from datetime import datetime

class DataTools:
    pass
    def digits_only(txt):
        """This function extracts the digits only from a string
        
        Args:
            txt: the string to extract the digits from it
        
        Returns: 
            the extracted numbers if they exist.
            if no numbers are found it returns None
        
        examples:
            > digits_only("a12bc45")  
            > 1245
            
            > digits_only("abc")  
            > None
        """
        digits = ""
        for i in txt:
            if i.isnumeric():
                digits += i
        if len(digits) > 0:
            return digits
        else:
            return None
        
    
    
    def email_format_check(email):
        """This function checks if a given string has the correct email format or not
        
        Args:
            email: the string that represents the email
    
        Returns: 
            True/False 
        
        Examples:
            > email_format_check("someemail@domain.com")
            > True
            
            > email_format_check("someemail.com@")
            > False
            
            > email_format_check("someemail@domain.com@")
            > False
        """
        mail_pattern = re.compile(r".*@.*\.\w*$")
        match = re.match(mail_pattern, email)
        if match != None:
            return True
        else:
            return False
        
        
    def days_between(date1, date2, unit= "years"):
        """This fucntion returns the difference between two dates the input date should be dd/mm/yyyy the output number of days/months/years between the two dates
        
        Args:
            date1: the first date "dd/mm/yyyy"
            date2: the second date "dd/mm/yyyy"
            unit: the difference between the two dates in days/months/years
            
        Returns:
            the difference between the two dates
            returns None if the dates are in wrong format
            
        Examples:
            > days_between("01/11/2020","31/12/2020","days")
            > 60
            
            > days_between("01/11/2020","31/12/2020","years")
            > 0.164
        """
        try:
            date1 = datetime.strptime(date1, "%d/%m/%Y")
            date2 = datetime.strptime(date2, "%d/%m/%Y")
            diff = abs((date2 - date1).days) 
            # converting days to years
            fin_diff = 0.0
            if unit=="years" or unit=="y":
                fin_diff = round(diff/365,3)
            if unit=="months" or unit=="m":
                fin_diff = round(diff/30,3)
            if unit=="days" or unit=="d":
                fin_diff = diff
            return fin_diff
        except ValueError:
            "The date format is not correct. It should be dd/mm/yyyy"
            return None


    def list_to_dict(lst):
            """
            This function enumerates a list and return enumerated list in form of a dictionary
                    Args:
                        list: the list to be convetrted to dictionary
                        
                    Returns: 
                        dictionary: the enumarted list values as keys and numbers as values in a dictionary
                        
            		example:
                    		> list_to_dict(['a','b','c'])
                    		> {'a':0,'b':1,'c':2}
            """
            try:
                dictionary = {}
                for value, key in enumerate(lst):
                    dictionary[key] = value
                return dictionary
            except TypeError:
                "The entered value is not a list"
                return None
            
    