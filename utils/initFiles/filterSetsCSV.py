import csv

def filter_csv(input_filename, output_filename):
    with open(input_filename, 'r') as input_file, open(output_filename, 'w', newline='') as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            if len(row['set_num']) == 7 and row['set_num'][-2] == '-' and row['set_num'][-1]=='1':
                #remove the "-1" at the end of the set_num
                row['set_num'] = row['set_num'][:-2]
                writer.writerow(row)

if __name__ == "__main__":
    filter_csv('sets.csv', 'goodSets.csv')
    print("Filtered CSV created successfully.")