# DatCh
The DatCh data checker checks data files in multiple formats for values and consistancy.

DatCh currently checks for:
- nan values
- white space in strings
- CAPS errors
- data types

Wish list as optional checks:
- zero values (or maybe not)
- outliers (np.abs(float value) > mean + 3 * np.std)
