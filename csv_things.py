import unicodecsv

def import_csv_to_list(filename, headers = False, astuple = False):
    data = []
    with open(filename, 'rb') as file:
        reader = unicodecsv.reader(file, delimiter = ',', quotechar = '"')
        if headers == True:
            next(reader, None) # Skip header row.
        for row in reader:
            if(astuple):
                data.append(tuple(row))
            else:
                data.append(row)
    return data

def import_csv_to_dict(filename, params = None, headers = False):
    data = []
    with open(filename, 'rU') as file:
        reader = unicodecsv.reader(file, delimiter = ',', quotechar = '"')
        if(headers):
            params = reader.next()
        for row in reader:
            data.append(dict(zip(params, row)))
    return data

def export_list_to_csv(filename, data, headers = None):
    with open(filename, 'wb') as file:
        writer = unicodecsv.writer(file, delimiter = ',', quotechar = '"')
        if headers != None:
            writer.writerow(headers)
        for i in range(len(data)):
            writer.writerow(data[i])
    return

def export_dict_to_csv(filename, data):
    with open(filename, 'wb') as file:
        writer = unicodecsv.writer(file, delimiter = ',', quotechar = '"')
        writer.writerow(data[0].keys())
        for i in range(len(data)):
            writer.writerow(data[i].values())
    return