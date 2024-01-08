# OhmOracle

A CLI voltage divider calculator to simplify the process of picking resistor values.
It works by calculating a range of possible resistor values given Vin and Vout and picking values with the closest match to Vout with standard E3-192 resistor values or values from a user defined CSV file.

## Usage
`python ohmoracle.py [-h] --vin(-i) VIN --vout(-o) VOUT [--standard(-s) STANDARD]  [--csv(-c) CSV_FILE]`

### Required
`--vin`/`-i`: Voltage input value

`--vout`/`-o`: Voltage output value

### Optional
`--standard`/`-s`: Standard resistor value E series (E6-E192)

`--csv`/`-c`: File path/name of a CSV file containing user defined resistor values
    
* Note: Values in the CSV file can contain K or M as shorthands for multiples of 1000 and 1000000.

If both arguments are omitted, the E6 series is chosen by default.

### Examples
`python ohmoracle.py -i 5 -o 3.3`

Finds the closest E6 resistor values for an input of 5v and and an output of 3.3v.

`python ohmoracle.py -i 12 -o 5 -s E192` 

Finds the closest E192 resistor values for an input of 12v and an output of 5v.

`python ohmoracle.py -i 9 -o 3.3 -c resistor_values.csv`

Finds the closest resistor values for an input of 9v and an output of 3.3v using values from resistor_values.csv.

## Output
The output of this program is formatted as a markdown table.

### Explanation  

`R1`: Resistor 1 (top resistor connected to Vin) resistance value

`R2`: Resistor 2 (bottom resistor connected to GND) resistance value

`Vout`: Voltage output of a voltage divider with R1 and R2 as resistor values

`Error`: Percent error between the `Vout` specified as an argument and the `Vout` of `R1` and `R2`

### Example
| Parameter | Value              |
|-----------|--------------------|
| R1        | 33 ohms            |
| R2        | 68 ohms            |
| Vout      | 3.366336633663366V |
| Error     | 2.010201020102012% |

## License
Licensed under the [MIT license](https://mit-license.org/)

## Credits
* **Programming:** [sebsky808](https://github.com/sebsky808)

## Support
If you find this project interesting or helpful, consider supporting me on [ko-fi](https://ko-fi.com/sebsky808), it would be much appreciated!