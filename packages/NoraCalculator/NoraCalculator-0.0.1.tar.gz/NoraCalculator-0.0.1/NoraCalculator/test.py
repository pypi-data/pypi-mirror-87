from calculator import NoraCalculator

num_a, num_b = 10, 20

test = NoraCalculator(num_a, num_b)

def test_sum():    
    assert(test.norasum() == 30)

def test_subtract():    
    assert(test.norasubtract() == -10)
    
def test_multiply():    
    assert(test.noramultiply() == 200)
    
def test_division():    
    assert(test.noradivision() == 0.5)