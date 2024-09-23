# Identify to whom a sequence of DNA belongs.

import sys
import csv
import re


# Check for correct number of args.
if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py [CSV] DNA")
# Open CSV file and read its contents into memory.
CSV_file = sys.argv[1]
persons = []
with open(CSV_file) as csvfile:
    reader = csv.DictReader(csvfile)
    # Get the list of STRs.
    STRlist = reader.fieldnames[1:]
    for name in reader:
        for column in reader.fieldnames[1:]:
            # Cast STR values into integers.
            name[column] = int(name[column])
        persons.append(name)
# Open DNA sequence text file and read its contents into memory.
DNA_file = sys.argv[2]
with open(DNA_file) as txtfile:
    DNA = txtfile.read()

# For each STR, compute the longest run of consecutive repeats in the DNA sequence.
counts = {}
for STR in STRlist:
    pattern = "(?=(("+re.escape(STR)+")+))"
    matches = re.findall(pattern, DNA)
    if len(matches) != 0:
        # Save STR counts in the dictionary.
        counts[STR] = max(len(match[0]) // len(STR) for match in matches)
# Compare the STR counts against each row in the CSV file.
for name in persons:
    name_copy = dict(name)
    name_copy.pop('name')
    # Print person's name if their DNA matches the DNA sequence.
    if counts == name_copy:
        print(name['name'])
        sys.exit(0)
print("No match")
