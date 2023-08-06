import pandas as pd

class DataError():
    def __init__(self,
                 error_type=None,
                 errors=None,
                 index=None,
                 values=None,
                 suggestions=None,
                 error_ratio=None,
                 ):
        self.error_type = error_type
        self.errors = errors
        self.index = index
        self.values = values
        self.suggestions = suggestions
        self.error_ratio = sum(errors)/len(values)

    def __repr__(self):
        return (f'{self.__class__.__name__}(error_type={self.error_type!r}, errors={sum(self.errors):1.0f}, values={len(self.values)}, error_ratio={self.error_ratio:1.2f})')

def any(s):
    
    errors = pd.DataFrame({
        'nan': nan(s).errors,
        'caps': caps(s).errors,
        'whitespace': whitespace(s).errors,
        'dtype': dtype(s).errors,
    }).any(axis=1)
    
    return DataError(error_type='any', errors=errors, values=s.values)

# possible errors

def nan(s):
    if isinstance(s, pd.Series):
        
        # errors
        errors = s.isnull()

        return DataError(error_type='nan error', errors=errors, values=s.values)
    else:
        return None
    
def caps(s):

    if isinstance(s, pd.Series):

        # create DataFrame with value counts
        df = pd.DataFrame({
            'check': s.apply(str).str.lower(),
            'original': s,
            'count': 1,
        })

        # find the most common original values when grouped bij check values and make a value map
        value_map = df.groupby(['check'])['original'].agg(pd.Series.mode).to_dict()

        # build suggestions
        suggestions = df['check'].map(value_map)

        # errors are suggestions that do not match the original series
        errors = (suggestions != s)

        return DataError(error_type='caps error', errors=errors, values=s.values, suggestions=suggestions)    
    else:
        return None
    
def whitespace(s):

    if isinstance(s, pd.Series):
    
        # create DataFrame with value counts
        df = pd.DataFrame({
            'check': s.apply(lambda x: ' '.join(str(x).split())),
            'original': s,
            'count': 1,
        })

        # find the most common original values when grouped bij check values and make a value map
        value_map = df.groupby(['check'])['original'].agg(pd.Series.mode).to_dict()

        # build suggestions
        suggestions = df['check'].map(value_map)

        # errors are suggestions that do not match the original series
        errors = (suggestions != s)

        return DataError(error_type='white space error', errors=errors, values=s.values, suggestions=suggestions)   
    else:
        return None

def dtype(s):

    if isinstance(s, pd.Series):

        # get errors list: data type is not the most common data type
        data_type = s.apply(type).mode()[0]
        errors = s.apply(type)!=data_type

        suggestions = pd.Series([pretty_data_type(data_type)]*len(s))

        return DataError(error_type='data type error', errors=errors, values=s.apply(type).apply(pretty_data_type), suggestions=suggestions)
    else:
        return None

# helpers
def pretty_data_type(t):
    pretty = {
        int: "integer",
        float: "float", 
        str: "string",
        bool: "boolean",
        pd.Timestamp: "timestamp", 
    }
    if t in pretty.keys():
        return pretty[t]
    else:
        return str(t)