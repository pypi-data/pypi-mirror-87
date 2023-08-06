# DatCh
The DatCh data checker checks data files for any inconsistancies.

DatCh currently checks for:
- nan values
- white space in strings
- CAPS errors
- data types

Usage:
```python
# check a pandas DataFrame
import pandas as pd
import datch

df = pd.DataFrame({
    'id': [0,1,'x',3,4,5,'y',7,None,9],
    'name': ['Rose', 'Lily', 'Tulip', 'Orchid', 'Carnation', 'Freesia', 3.14159265, 'Gladiolus', 'Anemone', 'Daffodil'],
})

datch.errors.nan(df['id'])
>> DataError(error_type='nan error', errors=1, values=10, error_ratio=0.10)

datch.errors.dtype(df['id'])
>> DataError(error_type='data type error', errors=3, values=10, error_ratio=0.30)

datch.errors.dtype(df['name'])
>> DataError(error_type='data type error', errors=1, values=10, error_ratio=0.10)

datch.check('data/data.xlsx')
>> DatCh is done! The output file is saved as /data/data_datched.xlsx
```


Wish list as optional checks:
- zero values (or maybe not)
- outliers (np.abs(float value) > mean + 3 * np.std)
