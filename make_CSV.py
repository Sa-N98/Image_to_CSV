import csv
import Levenshtein



def is_close(value1, value2, threshold=3):
    return abs(value1 - value2) <= threshold


def make_csv(data:list, headers_list:list):

    # Filtaring header from list of words in OCR data list
    headers_list=['Description', 'Type', 'Units', 'Per Unit', 'FxRate', 'Total']
    list_len=len(headers_list)
    headers=list()
    for header in headers_list:
        best_similarity=0
        best_match_pair=None
        for words in data:
            similarity = 1 - Levenshtein.distance(header,words[0]) / max(len(words[0]), len(header))
            if best_similarity <  similarity:
                best_similarity =  similarity
                best_match_pair = words
        # print(header,best_match_pair,best_similarity)
        headers.append(best_match_pair)
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
