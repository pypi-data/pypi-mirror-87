import numpy as np

#Calcuates error in functions variationally

def variational_error(func,params,error,param_id):
    
    values = []
    defualt = params # stores the default parameters
     #converts error and param_id to lists if only a single value is provided
        
    if type(error) != list and type(error) != np.array:
        error = [error]
        param_id = [param_id]
        
    # adds error to each value spesified in param_id
    
    for i in param_id:
        values.append(params[i]) 
        params[i] = values[param_id.index(i)] + error[param_id.index(i)]
        
    # calculates high error of function
    up_calc = np.abs(func(*params)-func(*defualt)) 
    
    # subtracts error from each value spesified in param_id
    for i in param_id:
        params[i] = values[param_id.index(i)] - error[param_id.index(i)]
    
    # calculates low eror of function
    down_calc = np.abs(func(*params)-func(*defualt))
    
    #returns the average of the difference between the high and low values
    return np.abs(up_calc + down_calc)/2
