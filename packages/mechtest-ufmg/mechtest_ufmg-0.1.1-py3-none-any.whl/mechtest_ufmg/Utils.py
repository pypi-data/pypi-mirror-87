
import numpy as np 
'''
Auxiliary functions module.
'''



def Hooke(strain, E = 150000, b = 0):
        '''
        Defines the linear equation for the linear portion of the stress-strain curve.

        Inputs:

        strain - the vector containing the strain values
        E - default = 150,000; initial guess for the modulus of elasticity in MPa.
        b - default = 0; intercept of the liear equation.
        '''

        return E * strain + b

def r_squared(x, y, model, modelParams):

        '''
        Calculates the R² statistics to evaluate the quality of the data regression.

        Inputs:

        x - the vector containing the x values of the independent variable of the function.
        y - the vector containing the dependent (measured) values as a function of x.
        model - the function that receives x as variable and calculates a y vector to model measured y.
        modelParams - the parameters of the model function passed as a list.

        Output:

        r_squared - the R² statistics. 
        '''

        res = y - model(x, *modelParams)
        ss_res = np.sum(res ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res/ss_tot)
        
        return r_squared

def find_index(array, value):
    
        i = 0
        while array[i] < value:
                i = i + 1
        return i

def uniform_plast(strain, stress, sig_y, uts):

        '''
        Takes the data portion between the yield stress and the ultimate tensile strength.

        Inputs:

        strain - the vector containing strain data.
        stress - the vector containing stress data.
        sig_y - the yield stress.
        uts - the ultimate tensile strength.

        Outputs:

        eps_c - the strain portion between sig_y and uts.
        sig_c - the stress portion between sig_y and uts.

        '''

    
        eps = strain.to_numpy()
        sig = stress.to_numpy()

        yield_index = find_index(sig, sig_y)
        uts_index = find_index(sig, uts)

        eps_c = eps[yield_index:uts_index]
        sig_c = sig[yield_index:uts_index]

        return eps_c, sig_c

def true_values(strain, stress):
        
        '''
        Returns the true stress and strain vectors.

        Inputs:

        strain - the vector containing the engineering strain vector.
        stress - the vector containing the engineering stress vectos.

        Outputs:

        eps_t, sig_t - the vectors containing the calculated true strain and stress values.
        '''
        
        
        eps_t = np.log(1 + strain)
        sig_t = stress * (1 + strain)

        return eps_t, sig_t


def log_Hollomon(log_strain, K = 300, n = 0.25):

        '''
        Defines the linear form of Hollomon's equation.

        '''
        logK = np.log(K)
        return logK + n * log_strain
        
