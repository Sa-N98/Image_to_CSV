import csv
from fuzzywuzzy import fuzz



def is_close(value1, value2, threshold=3):
    return abs(value1 - value2) <= threshold


def make_csv(data:list, headers_list:list):

    # Filtaring header from list of words in OCR data list
    headers=list()
    for word in data:
        best_similarity = 0
        best_match = None

        for header_word in headers_list:
            similarity = fuzz.partial_ratio(word[0], header_word)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = header_word
        # Check if the best match has sufficient similarity threshold
        if best_similarity >= 90 and len(headers)<=len(headers_list):  # You can adjust the threshold as needed
            headers.append(word)
            headers_list.remove(best_match)
            
    headers = sorted(headers, key=lambda entry: entry[1][0])
    
    # Grouping data dased on there rows
    grouped_data = []
    for entry in [word_data for word_data in data if word_data[0] not in [word[0] for word in headers]]:
        found_group = False

        for group in grouped_data:
            if is_close(group[0][1][1], entry[1][1], threshold=13):  # Adjust threshold as needed
                group.append(entry)
                found_group = True
                break

        if not found_group:
            grouped_data.append([entry])

    # Grouping data dased on there columns
    row_data=[]
    for group in grouped_data:
        dic=dict()
        for entry in group:
            min=1000000000000
            tag=None
            for header in headers:
                if abs(abs((entry[1][0]+entry[1][2])/2) - abs((header[1][0]+ header[1][2])/2))<min:
                    min=abs(abs((entry[1][0]+entry[1][2])/2) - abs((header[1][0]+ header[1][2])/2))
                    tag=header[0]
            dic[tag]=entry[0]
        row_data.append(dic.copy())
    
    
    
    # Writing CSV 
    filename = "test_output.csv"

    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[item[0] for item in headers])
        writer.writeheader()
        writer.writerows(row_data)

    return "CSV file created successfully."
