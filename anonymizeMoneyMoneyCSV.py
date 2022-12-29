import csv
import datetime
import re
import os

# This script reads in a CSV file with transactions, anonymizes the "Name" column, and
# writes the resulting data to a new CSV file with the following structure:
# | Datum        | Art       | Betrag |
# |--------------|-----------|--------|
# | 2022-12-27   | Support   | 10,00  |
# | 2022-12-27   | Mailjet   | -38,08 |

# Open the input file
with open("norden_social.csv", "r") as f:
    reader = csv.reader(f, delimiter=";")
    
    # Read the headers
    headers = next(reader)

    # Determine the column numbers for the desired columns
    date_column = headers.index("Datum")
    purpose_column = headers.index("Name")
    amount_column = headers.index("Betrag")

    # Open the output file
    with open("data.csv", "w", newline="") as g:
        writer = csv.writer(g, delimiter=';')

        # Write the headers
        writer.writerow(["Datum", "Art", "Betrag"])

        # Iterate through all rows
        for row in reader:

            # Convert the value for "Betrag" to a floating point number
            amount = row[amount_column]
            amount = amount.replace(",", ".")
            amount = float(amount)

            # Anonymize the value for "Art"
            if amount > 0:
                art = "Support"
            else:
                purpose = row[purpose_column]
                if re.search(r"\bDeepl\b", purpose):
                    art = "Deepl"
                elif re.search(r"\bmailjet\b", purpose):
                    art = "Mailjet"
                else:
                    art = "Serverkosten"

            # Convert the value for "Datum" to the desired format
            date = row[date_column]
            date = datetime.datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")

            # Convert amount to a string
            amount = row[amount_column]
            amount = str(amount)
            amount = amount.replace(".", ",")

            # Write the row
            writer.writerow([date, art, amount])

# Delete the input file
os.remove("norden_social.csv")
