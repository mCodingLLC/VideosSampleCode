import csv
from unidecode import unidecode

def is_good_char(c):
    return ord(c) <= 127

def clean_str(s):
    return ''.join(filter(is_good_char,s))

def main():
    with open('names.csv', newline='', encoding='utf-8') as dirty, open('names-cleaned.csv', 'w', newline='') as clean:
        reader = csv.reader(dirty)
        writer = csv.writer(clean)
        for row in reader:
            print(row)
            writer.writerow(map(clean_str, row))

if __name__ == '__main__':
    main()
