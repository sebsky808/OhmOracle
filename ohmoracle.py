# ohmoracle.py v1.0

# A CLI voltage divider calculator to simplify the process of picking resistor values.
# It works by calculating a range of possible resistor values given Vin and Vout and 
# picking values with the closest match to Vout with standard E3-192 resistor values or 
# values from a user defined CSV file.

# MIT License

# Copyright (c) 2024 sebsky808

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import csv

# constants
STANDARD_RESISTORS = {
    "E3": [10, 22, 47],
    "E6": [10, 15, 22, 33, 47, 68],
    "E12": [10, 12, 15, 18, 22, 27, 33, 29, 47, 56, 68, 82],
    "E24": [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91],
    "E48": [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 196, 205, 215, 226, 237, 249, 261, 274, 287, 301, 316, 332, 348, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715, 750, 787, 825, 866, 909, 953],
    "E96": [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174, 178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309, 316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732, 750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976],
    "E192": [100, 101, 102, 104, 105, 106, 107, 109, 110, 111, 113, 114, 115, 117, 118, 120, 121, 123, 124, 126, 127, 129, 130, 132, 133, 135, 137, 138, 140, 142, 143, 145, 147, 149, 150, 152, 154, 156, 158, 160, 162, 164, 165, 167, 169, 172, 174, 176, 178, 180, 182, 184, 187, 189, 191, 193, 196, 198, 200, 203, 205, 208, 210, 213, 215, 218, 221, 223, 226, 229, 232, 234, 237, 240, 243, 246, 249, 252, 255, 258, 261, 264, 267, 271, 274, 277, 280, 284, 287, 291, 294, 298, 301, 305, 309, 312, 316, 320, 324, 328, 332, 336, 340, 344, 348, 352, 357, 361, 365, 370, 374, 379, 383, 388, 392, 397, 402, 407, 412, 417, 422, 427, 432, 437, 442, 448, 453, 459, 464, 470, 475, 481, 487, 493, 499, 505, 511, 517, 523, 530, 536, 542, 549, 556, 562, 569, 576, 583, 590, 597, 604, 612, 619, 626, 634, 642, 649, 657, 665, 673, 681, 690, 698, 706, 715, 723, 732, 741, 750, 759, 768, 777, 787, 796, 806, 816, 825, 835, 845, 856, 866, 876, 887, 898, 909, 920, 931, 942, 953, 965, 976, 988]
}
SHORTHAND_MULTIPIERS = {
    "K": 1000,
    "M": 1000000
}
PARAMETER_COLUMN_LENGTH = 10
VALUE_COLUMN_LENGTH = 6

# prints error message and exits
def error(message:str):
    print(f"error: {message}")
    exit()

# takes a string with a resistor value shorthand
# like 2.2K or 1M and converts it to a float,
# or just simply casts the value to an float
# if it does not contain any shorthand values
def convert_value_shorthand(value:str) -> float:
    for shorthand in SHORTHAND_MULTIPIERS.keys():
        if value.upper().find(shorthand) != -1:
            converted = float(value.upper().strip(shorthand))
            converted *= SHORTHAND_MULTIPIERS[shorthand]
            return converted
    if value.replace(".", "", 1).isdigit():
        return float(value)
    else:
        error(f"{value} is not a valid resistor value! Only use numbers with optional shorthands for multiples (K and M).")

# reads a csv file with resistor values and
# generates a list of values
def file_to_resistor_list(filename:str) -> list:
    if filename == "":
        return None
    resistor_list = []
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                for column in row:
                    resistor_list.append(convert_value_shorthand(column))
    except FileNotFoundError:
        error(f"{filename} was not found!")
    if resistor_list == []:
        error(f"{filename} is empty! Add some resistor values.")
    return resistor_list

# get command line arguments from sys.argv and return vin, vout, and a list of resistor values
def get_arguments() -> tuple:
    parser = argparse.ArgumentParser(description="A CLI voltage divider calculator to simplify the process of picking resistor values.")
    parser.add_argument("--vin", "-i", type=float, required=True, help="Voltage input value")
    parser.add_argument("--vout", "-o", type=float, required=True, help="Voltage output value")
    parser.add_argument("--standard", "-s", type=str, required=False, default="E6", help="Resistor value standard (E6-E192)")
    parser.add_argument("--csv", "-c", type=str, required=False, default="", metavar="CSV_FILE", help="Resistor value file")
    args = parser.parse_args()
    args.standard = args.standard.upper()
    if not args.standard in STANDARD_RESISTORS:
        error(f"{args.standard} is not a vaild standard E series name")
    user_csv = file_to_resistor_list(args.csv)
    return (args.vin, args.vout, STANDARD_RESISTORS[args.standard] if user_csv == None else user_csv)

# generates and returns a list of r2 values 
# using a variant of the voltage divider formula
def generate_r2_list(vin:float, vout:float, r1_list:list) -> list:
    r2_list = []
    if vin == vout:
        error("Vin and Vout cannot be equal! Try making Vout lower than Vin.")
    if vin < vout:
        error("Vout cannot be greater than Vin! Try making Vout lower than Vin.")
    for r1 in r1_list:
        r2 = (vin * r1) / (vin - vout) # voltage divider formula, solving for r2
        r2_list.append(r2)
    return r2_list

# iterate through r1 and r2 values to calculate closest approximation to
# standard r2 values and the resulting vout value from that approximation
def find_approximations(vin:float, vout:float, r2_list:list, resistors:list) -> list:
    results = []
    for r1 in resistors:
        for r2 in r2_list:
            r2_closest = closest_resistor(resistors, int(r2))
            vout_closest = (vin * r2_closest) / (r1 + r2_closest) # voltage divider formula, solving for vout
            vout_error = ((vout_closest - vout) / vout) * 100 # percent error formula
            results.append({"r1": r1, "r2": r2_closest, "vout": vout_closest, "error": vout_error})
    return results

# find closest standard resistor value
def closest_resistor(resistors:list, ohms:float) -> int:
    closest = 0
    for i in resistors:
        if i > ohms:
            continue
        if ohms - closest > ohms - i:
            closest = i
    return closest

# iterate through results to find closest match to desired vout
def find_closest_match(vout:float, results:list) -> dict:
    closest_match = results[0]
    for result in results:
        if abs(closest_match["vout"] - vout) > abs(result["vout"] - vout):
            closest_match = result
    return closest_match

# generates padding spaces based on length of the string
# being padded and the total length of the string
# that it should be padded to
def generate_padding(string_length:int, total_length:int) -> str:
    return " " * (total_length - string_length)

# format and print values for the closest match
# in the format of a markdown table
def print_table(closest_match:dict):
    parameter_value_dict = {
        "R1": f"{closest_match['r1']} ohms", 
        "R2": f"{closest_match['r2']} ohms", 
        "Vout": f"{closest_match['vout']}V",
        "Error": f"{closest_match['error']}%",
    }
    # find longest string length for each column
    longest_parameter_length = PARAMETER_COLUMN_LENGTH
    longest_value_length = VALUE_COLUMN_LENGTH
    for key, value in parameter_value_dict.items():
        if longest_parameter_length < len(key):
            longest_parameter_length = len(key)
        if longest_value_length < len(value):
            longest_value_length = len(value)
    # add some padding
    longest_value_length += 1
    # print table
    print(f"| Parameter{generate_padding(PARAMETER_COLUMN_LENGTH, longest_parameter_length)} | Value{generate_padding(VALUE_COLUMN_LENGTH, longest_value_length)} |")
    print(f"|-{'-' * longest_parameter_length}|-{'-' * longest_value_length}|")
    for key, value in parameter_value_dict.items():
        print(f"| {key}{generate_padding(len(key), longest_parameter_length)}| {value}{generate_padding(len(value), longest_value_length)}|")

if __name__ == "__main__":
    vin, vout, resistors = get_arguments()
    r2_list = generate_r2_list(vin, vout, resistors)
    results = find_approximations(vin, vout, r2_list, resistors)
    closest_match = find_closest_match(vout, results)
    print_table(closest_match)