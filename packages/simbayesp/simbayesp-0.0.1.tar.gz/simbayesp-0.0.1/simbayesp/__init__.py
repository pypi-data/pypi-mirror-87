# From https://www.programiz.com/python-programming/docstrings
def add_binary(a, b):
    '''
    Returns the sum of two decimal numbers in binary digits.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    binary_sum = bin(a+b)[2:]
    return binary_sum

def exact_bayes(TPR = 0.90, TNR = 0.80, prevalence = 0.05):
    '''
    Returns the calculated PPV with a closed form of bayes' Theorem.

            Parameters:
                TPR(float): The sensitive rate of cannabis tests
                TNR(float): The rate that cannabis tests identifie non-users
                prevalence(float): The propotion of people people using cannabis

            Returns:
                    PPV (float): The calculated PPV
    '''
    PPV = (TPR * prevalence) / (TPR * prevalence + (1-TNR)*(1-prevalence))
    return PPV
