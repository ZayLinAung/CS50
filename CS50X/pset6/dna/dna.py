import sys
import csv


def main():

    if len(sys.argv) != 3:
        sys.exit("Usage: dna.py CSVFile TextFile")
    Database = []

    STR_dic = {}
    # read csv file into memory
    file = open(sys.argv[1])
    reader = csv.DictReader(file)

    for database in reader:
        Database.append(database)
    
    for STR in Database[0]:
        if not STR == "name":
            STR_dic[STR] = 0

    # read STR txt file into memory
    txt = open(sys.argv[2])
    reader_txt = txt.read()

    for STR in STR_dic:
        STR_dic[STR] = compute(reader_txt, STR)
    
    count = 0
    
    for i in range(len(Database)):
        for STR in STR_dic:
            if (int(Database[i][STR]) == STR_dic[STR]):
                count += 1
        if (count == len(STR_dic)):
            sys.exit(Database[i]["name"])
        else:
            count = 0
    print("No match")
    file.close()
    txt.close()
    

def compute(DNA, STR):
    counter = 0
    tmp_counter = 0
    i = 0
    add = len(STR)
    while i < len(DNA):
        j = i + add
        if (DNA[i: j] == STR):
            tmp_counter += 1
            i = j
        elif (not DNA[i: j] == STR):
            if (tmp_counter > counter):
                counter = tmp_counter
            tmp_counter = 0
            i += 1
    return counter
    
    
main()