#!/usr/bin/env python3

# Small script to parse a messy text file.

import re
import csv

with open('sample.txt', 'r') as f:
    contents = f.read()

# Massage data. :)
# Ensure that headers are separated from data consistently.
contents = re.sub(r'(\w+)\n(\d{5})', r'\1|\2', contents, count=1)
contents = re.sub(r"(\'\w*\')\n(\d{5})", r'\1|\2', contents)
contents = re.sub(r'\n', r'', contents)

# Get the first InvoiceKey field, which is where our record
# data beings.
first_id_match = re.search(r'\d{5}', contents)
current_id = first_id_match.group(0)

# Separate headers from data, and store as lists.
headers = contents[:first_id_match.start()]

data = contents[first_id_match.start():]

# Remove trailing pipe to avoid gaining
# an extra field with an empty string.
headers = headers.rstrip('|')

# Split everything into lists.
split_headers = headers.split('|')

split_data = data.split('|')

# Alternative implementation, but messy.
def parse_count(split_headers, split_data):
    data_dict = {}
    final_list = []
    temp = []
    for i, f in enumerate(split_data, 1):
        temp.append(f)
        record_size = len(split_headers)
        if i % record_size == 0:
            for h, f in zip(split_headers, temp):
                data_dict[h] = f
            final_list.append(data_dict)
            data_dict = {}
            temp = []
    return final_list

def parse_slice(headers, data):
    record_size = len(headers)
    record_num = len(data) // record_size

    records = []
    start = 0
    for i in range(record_num):
        end = start + record_size

        records.append(
            {h: f for h, f in zip(headers, data[start:end])})

        start = start + record_size

    return records

final_list = parse_slice(split_headers, split_data)

# Write out the results.
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.DictWriter(csvfile, split_headers)

    spamwriter.writeheader()
    spamwriter.writerows(final_list)
