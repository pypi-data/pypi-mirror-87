class NoraCalculator:
    """Class for basic math operations"""
    
    def __init__(self, num_a, num_b):
        self.num_a = num_a
        self.num_b = num_b
    
    def norasum(self):
        """
        Calculate the sum of two numbers.
        Args:
            None.
        Return:
            float: the sum of two numbers.        
        """        
        return self.num_a + self.num_b
    
    def norasubtract(self):
        """
        Calculate the subtract of two numbers.
        Args:
            None.
        Return:
            float: the subtract of two numbers.            
        """    
        return self.num_a - self.num_b
    
    def noramultiply(self):
        """
        Calculate the multiply of two numbers.
        Args:
            None.
        Return:
            float: the multiply of two numbers.            
        """    
        return self.num_a * self.num_b
    
    def noradivision(self, num_round=2):
        """
        Calculate the division of two numbers.
        Args:
            num_round (int): the numb of places after comma that function must to return. 
        Return:
            float: the sum of two numbers.            
        """    
        return round(self.num_a / self.num_b, num_round)