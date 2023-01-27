import warnings
warnings.simplefilter("ignore", UserWarning)

import re
from pulp import LpProblem
import pandas as pd

def get_values_from_sum(file_name, sum_val):
    """
    This function selects lines from the file named 'file_name',
    of type '.xlsx', where the sum of values in column 'Value'
    are exactly equal to the value of 'sum_val'.

    Parameters
    ----------
    file_name: string
        .xlsx file name without the type at the end.

    sum_val: float
        Sum value.

    Returns
    -------
    'file_name'_values.xlsx: A .xlsx file with just the values selected.
    
    """
    
    data = pd.read_excel(f'{file_name}.xlsx')
    prob = LpProblem("Get elements from sum", LpMaximize)

    x = LpVariable.dicts('v', data.Value, 0, cat= 'Binary')

    prob += lpSum(val*var for val, var in x.items())
    prob += lpSum(val*var for val, var in x.items()) == sum_val
    prob.solve()

    values = []
    for v in prob.variables():
        if v.varValue == 1:
        values.append(float(re.findall("\d+\.\d+", v.name)[0]))

    selected_data = data.loc[data['Value'].isin(values)]
    selected_data.to_excel(f'{file_name}_values.xlsx', index=False)