from scipy.signal import find_peaks
from numpy import*

from .utilities import ConstantDeriv, ConstantPoints, ESR_ls, Cap_ls, Half_pt_ind


#Capacitance analysis (given x and y dataset, current and masses)
#Recieve current in mA and mass in mg and convert to A and g for calculations
def CC_Cap(xset, yset, current, m1 = False, m2 = False, ESR_method = True, setting = False, cap_method = False, filename = False, cap_grav = True):
    """
        Data manipulation
        
        
        Notes
        -----
        Capacitance and ESR analysis
       
        Parameters
        ----------
        xset : :class:`list`
            List of time reading   
            
        yset : :class:`list`
            List of corresponding voltage reading  
        
        current : :class:`float`
            The current under which the GCD is operated. The current is in mA. 
        
        m1 : :class:`float`, optional
            The mass of electrode 1 of the supercapacitor. The mass is in mg.

        m2 : :class:`float`, optional
            The mass of electrode 2 of the supercapacitor. The mass is in mg.
            
        ESR_method : :class:`int`, optional
            The method for ESR analysis.
            ESR_method = 1 (default constant point analyis using the first point after the peak for calculating voltage drop) 
                       = 101 (constant point analysis using the nth point after the peak, where n is specified using setting)
                       = 2 or True (default constant second derivative method using the point where the second derivative is greater than 0.01)
                       = 201 (constant second derivative method where the cut off derivative is specified using setting)
        
        setting : :class:`float`, optional
            The setting for ESR analysis
            setting = False for ESR_method = 1, 2 or True
            setting = nth point/cut off second derivative depending on the ESR_method
            
        cap_method : :class:`int`, optional
            The method for capacitance analysis
            cap_method = 1 (default method where the lower voltage range is used)
                       = 2 (upper voltage range is used)
  
 
        filename : :class:`string`, optional
            Name of the text file being analysed
        

        cap_grav : :class:`bool` 
            cap_grav = False, output non-gravimetric capacitance
            cap_grav = True, output gravimetric capacitance

        returns
        -------
        : :class:`list, list, list, list, int` 
            [list of capacitance], [list of ESR], [list of peak indices], [list of trough indices], number of cycles
                
            
    """

    if filename != False:
        print('The file currently being analysed is:', filename)
        
    else:
        pass 
    

    
    troughs, _= find_peaks(-yset)
    peaks, _= find_peaks(yset)
    N_cycle=0
    
    #Checking the number of cycle(s)
    if len(peaks) == len(troughs):
        N_cycle = len(peaks)
        
    else:
        peaks = peaks[:-1]
        if len(peaks) == len(troughs):
            N_cycle = len(peaks)
        else:
            print('Error! The number of peaks cannot match the number of troughs')
                        
    
    mid_ind = [Half_pt_ind(yset[peaks[i]:troughs[i]],(yset[peaks[i]]+yset[troughs[i]])/2) for i in range(len(peaks))]
    
    
    cc_grad = []
    faulty_cyc_ind = []
    for i in range(len(peaks)):
        if len(xset[peaks[i]:troughs[i]]) > len(xset[peaks[i-5]:troughs[i-5]])*0.5/5:
            if cap_method is 1 or cap_method is False:
                try:
                    cc_grad += [polyfit(xset[peaks[i]:troughs[i]][mid_ind[i]:], yset[peaks[i]:troughs[i]][mid_ind[i]:],1, cov=False)[0]]
                except:
                    faulty_cyc_ind += [i]
                    print('Error found in cycle ' + str(i+1)+ '. Skipped for capacitance calculation')
                  
            if cap_method is 2:
                try:
                    cc_grad += [polyfit(xset[peaks[i]:troughs[i]][:mid_ind[i]], yset[peaks[i]:troughs[i]][:mid_ind[i]],1, cov=False)[0]]
                except:
                    faulty_cyc_ind += [i]
                    print('Error found in cycle ' + str(i+1)+ '. Skipped for capacitance calculation')         
            
        
        else:
            faulty_cyc_ind += [i]
            print('Cycle ' + str(i+1)+ ' has insufficient data points. Skipped for capacitance calculation')
            #data points in this cycle is 50% than the avarage data points in the 5 cycles before it.   
         
                        
    
    if ESR_method == 1 or ESR_method == 101:
        esr_v = [ConstantPoints(yset, peaks[i], set_n = setting) for i in range(len(peaks))]
      
    elif ESR_method is True or ESR_method == 2 or ESR_method == 201:
        esr_v = [ConstantDeriv(xset, yset, peaks[i], troughs[i], set_deriv = setting)[0] for i in range(len(peaks))]
                      
    elif ESR_method is False:
        esr_v = False
        
    else:
        print('ESR method not specified. ESR values will not be calculated.')
        esr_v= False
        
    if cap_grav is True and m1 is not False and m2 is not False:
        cap_ls_calc = Cap_ls(cc_grad, current*10**(-3), m1*10**(-3), m2*10**(-3))
        
    else:
        cap_ls_calc = Cap_ls(cc_grad, current*10**(-3), cap_grav = False)

    
    esr_ls_calc = ESR_ls(esr_v, current*10**(-3))
    
    return cap_ls_calc, esr_ls_calc, peaks, troughs, N_cycle, faulty_cyc_ind


