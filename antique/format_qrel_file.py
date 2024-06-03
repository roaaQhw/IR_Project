import json

# File paths
qrel_file_path = r'C:\Users\DELL\Desktop\IR_project_final\antique\qrels.txt'
query_text_file_path = r'C:\Users\DELL\Desktop\IR_project_final\antique\queries.txt'

# Function to parse qrel file
def parse_qrel(file_path):
    qrel_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            query_id = int(parts[0])
            doc_id = parts[2]
            if query_id not in qrel_dict:
                qrel_dict[query_id] = set()
            qrel_dict[query_id].add(doc_id)
    return qrel_dict

# Function to parse query text file
def parse_query_text(file_path):
    query_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split("\t", 1)
            query_id = int(parts[0])
            query_text = parts[1]
            query_dict[query_id] = query_text
    return query_dict

# Placeholder function for URL retrieval (Assuming single URL per query)
def get_url(doc_id):
    # Dummy implementation
    return f"https://example.com/{doc_id}"

# Parse the qrel and query text files
qrel_dict = parse_qrel(qrel_file_path)
query_dict = parse_query_text(query_text_file_path)

# Combine the data into the desired JSON format
combined_data = {}
for query_id in qrel_dict:
    if query_id in query_dict:
        query_text = query_dict[query_id]
        if query_id not in combined_data:
            combined_data[query_id] = {
                "qid": query_id,
                "query": query_text,
                "url": "",  # Placeholder, assuming single URL per query
                "answer_pids": set()
            }
        for doc_id in qrel_dict[query_id]:
            combined_data[query_id]["answer_pids"].add(doc_id)
            # Assuming all doc_ids have the same base URL for the query
            if not combined_data[query_id]["url"]:
                combined_data[query_id]["url"] = get_url(doc_id)

# Assign new sequential IDs starting from 0
new_combined_data = []
new_qid = 0
for query_id, data in combined_data.items():
    data["qid"] = new_qid
    data["answer_pids"] = list(data["answer_pids"])
    new_combined_data.append(data)
    new_qid += 1

# Save the JSONL data to a file
output_file_path = r'C:\Users\DELL\Desktop\IR_project_final\antique\output.jsonl'
with open(output_file_path, 'w') as output_file:
    for entry in new_combined_data:
        json.dump(entry, output_file)
        output_file.write('\n')

print(f"JSONL data has been written to {output_file_path}")
