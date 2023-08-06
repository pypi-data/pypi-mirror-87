import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simps, trapz
from scipy.optimize import curve_fit
from mechtest_ufmg.Utils import *
import os

def plot_eng_SSC(strain, stress, fig_label = 'Sample ', show_plot = True,
                 save = False, name = 'eng_SSC', ):

    '''
    Plots the conventional, or engineering, stress-strain curves.
    Inputs:
    strain - vector containing the strain data in admensional units, if the data is provided in %, divide it by 100; e.g.: [mm/mm].
    stress - vector containing the stress data relative to the strain vector.
    fig_label - the name of the sample or test run that will appear in the legend.
    show_plot - default = True; if set to false, the plot is not shown when the script runs.
    save - default = False; if set to true, will save the figure ina output folder within the running directory.
    name - default = eng_SSC; sets the name of the file that will be saved.
    Outputs:
    Engineering stress-strain curve as a file or image shown with matplotlib interface.
    '''
        
    plt.figure(figsize=(8, 4.5), facecolor = 'white')
    plt.plot(strain, stress, 'b-', label = fig_label)
    plt.xlabel('strain [mm/mm]')
    plt.ylabel('stress [MPa]')
    plt.xlim(0, 1.05 * max(strain))
    plt.ylim(0, 1.05 * max(stress))
    plt.title(f'Engineering stress/strain curve')
    plt.legend(fontsize = 12, loc = 'lower right', frameon = False)

    if save == True:
        save_path = os.path.abspath(os.path.join('output', name))
        plt.savefig(save_path, dpi = 300, bbox_inches = 'tight',transparent = False)
    
    if show_plot == True:
        plt.show()



def young_modulus(strain, stress, fig_label = 'Sample', show_plot = True, save = False, name = 'elasticity'):

    '''
    Calculates the apparent modulus of elasticity of the material from the engineering stress-strain data. 
    
    Inputs:
    strain - vector containing the strain data in admensional units, if the data is provided in %, divide it by 100; e.g.: [mm/mm].
    stress - vector containing the stress data relative to the strain vector.
    fig_label - the name of the sample or test run that will appear in the legend.
    show_plot - default = True; if set to false, the plot is not shown when the script runs.
    save - default = False; if set to true, will save the figure ina output folder within the running directory.
    name - default = elasticity; sets the name of the file that will be saved.
    
    Outputs:
    E - the apparent modulus of elasticity in the same units as the stress input; e.g.: [MPa].
    b - the stress intercept obtained from the regression process.
    R_squared - the R^2 statistics related to the linear regression of the linear portion of the stress-strain curve.

    Figure showing the portion of the curve that was fitted and the regression data, except b.
    '''

    # taking only the elastic portion of a curve
    x = strain[strain < 0.002]
    y = stress[0:len(x)]

    # performing the linear regression on the elastic part of the data
    init_guess = [100000, 0]
    model = curve_fit(Hooke, x, y, p0 = init_guess)
    ans, cov = model
    E, b = ans
    fit_curve = E * x + b
    E_gpa = round(E / 1000)

    # calculating the R_squared statistic
    r2 = r_squared(x, y, Hooke, ans)
        
    # plotting the figure and showing or saving the figure
    plt.figure(figsize = (8,4.5))
    plt.plot(strain, stress, 'b-', label = fig_label)
    plt.plot(x, fit_curve, 'r-', linewidth = 2, label = 'Fitted curve' )
    plt.xlabel('strain [mm/mm]')
    plt.ylabel('stress [MPa]')
    plt.xlim(0, 1.05* max(strain))
    plt.ylim(0, 1.05 * max(stress))
    plt.title(f'Elasticity modulus determination')
    plt.legend(fontsize = 12, loc = 'lower right', frameon = False)
    plt.text(0.1 * max(strain), 0.1 * max(stress), f'The elasticity modulus is {E_gpa} GPa, R² = {round(r2, 4)}', fontsize = 12)

    if save == True:

        save_path = os.path.abspath(os.path.join('output', name))
        plt.savefig(save_path, dpi = 300, bbox_inches = 'tight',transparent = False)        
    
    if show_plot == True:
        plt.show()

    return E, int(b), r2

def sigma_y(strain, stress, E_mpa, b = 0, fig_label = 'Sample', show_plot = True, save = False, name = 'sigma_yield'):

    '''
    Calculates the yielding stress as the stress related to a permanent deformation of 0.002.

    Inputs:
    strain - vector containing the strain data in admensional units, if the data is provided in %, divide it by 100; e.g.: [mm/mm].
    stress - vector containing the stress data relative to the strain vector.
    E_mpa - the modulus of elasticity in MPa (should work if the units are consistent, but not SI), whether user stated or calculated by young_modulus function.
    b - default = 0; the intercept of the regression for the specific data, leads to a higher precision result.
    fig_label - the name of the sample or test run that will appear in the legend.
    show_plot - default = True; if set to false, the plot is not shown when the script runs.
    save - default = False; if set to true, will save the figure ina output folder within the running directory.
    name - default = sigma_yield; sets the name of the file that will be saved.

    Outputs:
    sigma_yield - the yielding stress in the same unit of stress input.

    Figure showing the lines used to compare and determine the yield strength.
    '''
    # taking part of the data
    x = strain[strain < 0.05]
    k = x - 0.002
    z = Hooke(k, E_mpa)
    # finding the index of sig_y
    i = 0
    while stress[i] > z[i]:
        i = i + 1

    sig_y = stress[i]  
            
    plt.figure(figsize = (8,4.5))
    plt.plot(strain, stress, 'b-', label = fig_label)
    plt.plot(x, Hooke(x, E_mpa, b), 'r--', linewidth = 1, label = 'Hooke\'s law' )
    plt.plot(x, Hooke(k, E_mpa), 'r:', linewidth = 1 )
    plt.xlabel('strain [mm/mm]')
    plt.ylabel('stress [MPa]')
    plt.xlim(0, 1.05 * max(strain))
    plt.ylim(0, 1.05 * max(stress))
    plt.title(f'Yield strength determination')
    plt.legend(fontsize = 12, loc = 'lower right', frameon = False)
    plt.text(0.1 * max(strain), 0.1 * max(stress), f'The yield strength is {round(sig_y)} MPa.', fontsize = 12)

    if save == True:

        save_path = os.path.abspath(os.path.join('output', name))
        plt.savefig(save_path, dpi = 300, bbox_inches = 'tight',transparent = False)

    if show_plot == True:
        plt.show()

    print(f'The yield strength is {round(sig_y)} MPa.')
    
    return sig_y

def ultimate_tens_stren(strain, stress, show = True):

    '''
    Calculates the ultimate tensile stress taking the higher stress from the stress vector input.

    Inputs:
    strain - vector containing the strain data in admensional units, if the data is provided in %, divide it by 100; e.g.: [mm/mm].
    stress - vector containing the stress data relative to the strain vector.
    show - default = True; if true, prints the value of UTS in the command line.

    Output:
    uts - the ultimate tensile strength in the same unit of the stress input.

    '''
        
    uts = max(stress)
    if show == True:
        print(f'The ultimate tensile strength is {round(uts)} MPa. ')

    return uts

def uniform_elongation(strain, stress, show = True):

    '''
    Calculates the uniforme elongation from the input data taking the strain point related to the uts value.

    Inputs:
    strain - vector containing the strain data in admensional units, if the data is provided in %, divide it by 100; e.g.: [mm/mm].
    stress - vector containing the stress data relative to the strain vector.
    show - default = True; if true, prints the value of UTS in the command line.

    Output:
    u_elong - the uniform elongation of the sample.
    '''
    # transform data to numpy arrays
    eps = strain.to_numpy()
    sig = stress.to_numpy()

# finds the index of the maximum stress
    index = np.argmax(sig)
    u_elong = eps[index]

# prints depending on the user's choice
    if show == True:
        print(f'The uniform elongation is {round(u_elong, 4)}.')

    return u_elong

def aprox_resilience(E, sig_y, show = True):

    '''
    Calculates the resilience by the approximation formula U_r = sigma_yield^2/E.

    Inputs:
    E - the apparent elasticity modulus, in MPa.
    sig_y - the yield strength, in MPa
    show - default = True; if True prints a string containing the calculated value.

    Output:

    U_r - the resilience calculated by the presented formula.

    '''

    U_r = (sig_y ** 2)/(2*E)

    if show == True:
        print(f'The resilience calculated by the formula yield²/2E is {round(U_r,2)} MJ/m³. ')

    return U_r

def resilience(strain, stress, sig_y, dx = 1.0, show = True):

    '''
    Calculates the resilience by numerical integration using the trapezoidal method up to the yield stregth point.

    Inputs:
    strain - vector containing the strain data in admensional units, if the data is provided in %, divide it by 100; e.g.: [mm/mm].
    stress - vector containing the stress data relative to the strain vector.
    sig_y - the yield strength in MPa.
    dx - default = 1.0; the step size for the integration.
    show - default = True; if true, prints the value of UTS in the command line.

    Output:

    uts - the ultimate tensile strength in the same unit of the stress input.

    '''
    
    i = find_index(stress, sig_y)
    eps = strain[0:i]
    sig = stress[0:i]
    U_r = trapz(eps, sig, dx)

    if show == True:
        print(f'The resilience calculated by trapezoidal integration with dx = {dx} is {round(U_r,2)} MJ/m³. ')

    return U_r


def aprox_toughness(strain, sig_y, uts, show = True):

    '''
    Calculates an approximation of the toughness using the formula U_t = eps_f * ((sig_y + uts)/2).

    Inputs:

    strain - the vector containing the strain values from the test.
    sig_y - the yield strength, in MPa
    uts - the ultimate tensile strength, in MPa
    show - default = True; if True prints the string containing the material toughness. 

    Output:

    U_t - the approximate toughness of the material
    '''

    eps_f = max(strain)

    U_t = eps_f * ((sig_y + uts) / 2)
    
    if show == True:
        print(f'The material toughness is approximately {round(U_t)} MJ/m³.')

    return U_t 


def toughness(strain, stress, show = True):

    '''
    Calculates the toughness of the material performing the numerical integration of the stress-strain curve.

    Inputs:

    strain - the vector containing the strain values obtained from the tests.
    stress - the vector containing the stress values that refer to the strain vector.
    show - default = True; if True prints a string containing the toughness in the command line.

    Output:

    mat_toughness - the material toughness calculated by numerical integration, in MJ/m³.
    '''

    mat_toughness = trapz(stress, strain)

    if show == True:
        print(f'The material toughness computed by Trapezoidal method is {round(mat_toughness)} MJ/m³. ')
    
    return mat_toughness

def plot_flow_curve(strain, stress, sig_y, uts, fig_label = 'Sample', show_plot = True, save = False, name = 'flow_curve'):
                                                    # TODO: deal with discontinuous yielding; how can I determine where it ends?

    '''
    Plots the flow stress curve from the material stress-strain curve with values between the yield strength and the ultimate tensile strength.

    Inputs:

    strain - the vector containing the strain values obtained from the tests.
    stress - the vector containing the stress values that refer to the strain vector.
    sig_y - the yield strength, in MPa.
    uts - the ultimate tensile strength, in MPa.
    fig_label - default = Sample; the string that identify the sample name in the output figure.
    show_plot - default = True; if True, the plot is shown in a matplotlib interface.
    save - default = False, if True, saves the figure in the folder output;
    name - default = flow_curve; the name of the file saved in the output folder.

    Outputs:    

    Figure that can be displayed in matplotlib interface and/or saved to the output folder.
    '''
    eps = strain.to_numpy()
    sig = stress.to_numpy()

    yield_index = find_index(sig, sig_y)
    uts_index = find_index(sig, uts)

    eps_c = eps[yield_index:uts_index]
    sig_c = sig[yield_index:uts_index]

    plt.figure(figsize = (8,4.5))
    plt.plot(eps_c, sig_c, 'b-', label = fig_label)
    plt.xlabel('strain [mm/mm]')
    plt.ylabel('stress [MPa]')
    plt.xlim(0, 1.05 * max(strain))
    plt.ylim(0, 1.05 * max(stress))
    plt.title(f'Flow stress curve')
    plt.legend(fontsize = 12, loc = 'lower right', frameon = False)

    if show_plot == True:
        plt.show()

    if save == True:

        save_path = os.path.abspath(os.path.join('output', name))
        plt.savefig(save_path, dpi = 300, bbox_inches = 'tight',transparent = False)

def plot_true_SSC(strain, stress, sig_y, uts, fig_label = 'Sample', show_plot = True, save = False, name = 'true_SSC'):

    '''
    Plots the true stress-strain conversion of the input data.

    Inputs:

    strain - the vector containing the strain values obtained from the tests.
    stress - the vector containing the stress values that refer to the strain vector.
    sig_y - the yield strength, in MPa.
    uts - the ultimate tensile strength, in MPa.
    fig_label - default = Sample; the string that identify the sample name in the output figure.
    show_plot - default = True; if True, the plot is shown in a matplotlib interface.
    save - default = False, if True, saves the figure in the folder output;
    name - default = true_SSC; the name of the file saved in the output folder.

    Output:

    Figure that can be displayed in matplotlib interface and/or saved to the output folder.
    '''

    eps, sig = uniform_plast(strain, stress, sig_y, uts)
    eps_t, sig_t = true_values(eps, sig)

    plt.figure(figsize = (8,4.5))
    plt.plot(eps_t, sig_t, 'b-', label = fig_label)
    plt.xlabel('true strain [mm/mm]')
    plt.ylabel('true stress [MPa]')
    plt.xlim(0, 1.05 * max(eps_t))
    plt.ylim(0, 1.05 * max(sig_t))
    plt.title(f'True stress/strain curve')
    plt.legend(fontsize = 12, loc = 'lower right', frameon = False)
    
    if save == True:

        save_path = os.path.abspath(os.path.join('output', name))
        plt.savefig(save_path, dpi = 300, bbox_inches = 'tight',transparent = False)


    if show_plot == True:

        plt.show()

def flow_model(strain, stress, sig_y, uts, func = 'Hollomon', show = True, show_plot = True, save = False, name = 'flow_model'):

    # TODO: implement functions other than Hollomon.
    '''
    Calculates the regression coefficients for a model of plasticity, i.e. Hollomon's equation.

    Inputs:

    strain - the vector containing the strain values obtained from the tests.
    stress - the vector containing the stress values that refer to the strain vector.
    sig_y - the yield strength, in MPa.
    uts - the ultimate tensile strength, in MPa.
    fig_label - default = Sample; the string that identify the sample name in the output figure.
    show_plot - default = True; if True, the plot is shown in a matplotlib interface.
    save - default = False, if True, saves the figure in the folder output;
    name - default = flow_model; the name of the file saved in the output folder.

    Output:

    shex - strain hardening coefficient, n.
    Koeff - resistance modulus K, in MPa.
    
    Figure that can be displayed in matplotlib interface and/or saved to the output folder.
    '''

    eps_c, sig_c = uniform_plast(strain, stress, sig_y, uts)

    eps_t, sig_t = true_values(eps_c, sig_c)

    eps_tl = np.log(eps_t)
    sig_tl = np.log(sig_t)

    init_guess = [300, 0.25]

    ans, cov = curve_fit(log_Hollomon, eps_tl, sig_tl, p0 = init_guess)

    Koeff = ans[0]
    shex = ans[1]

    sig_h = log_Hollomon(eps_tl, K = Koeff, n = shex)

    R2 = r_squared(eps_tl, sig_tl, log_Hollomon, ans)

    plt.figure(figsize = (8,4.5))
    plt.plot(eps_tl, sig_tl, 'b-', label = 'Stress-Strain log values')
    plt.plot(eps_tl, sig_h, 'r:', label = f'Linear Hollomon, K = {round(Koeff)} MPa, n = {round(shex, 2)}, R²={round(R2, 4)}')
    plt.xlabel('log(strain) [mm/mm]')
    plt.ylabel('log(stress) [MPa]')
    plt.title(f'{func} fitted to the data')
    plt.legend(fontsize = 12, loc = 'lower right', frameon = False)        

    if show_plot == True:

        plt.show()

    if save == True:
        
        save_path = os.path.abspath(os.path.join('output', name))
        plt.savefig(save_path, dpi = 300, bbox_inches = 'tight',transparent = False)
        
    if show == True:

        print(f'The resistance modulus is {round(Koeff)} MPa and the strain-hardening exponent is {round(shex, 2)}.')

    return shex, Koeff


        