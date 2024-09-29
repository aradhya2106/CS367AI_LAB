import heapq
import re
from docx import Document

def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return ' '.join(full_text)

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def heuristic(remaining_sents1, remaining_sents2):
    if not remaining_sents1 or not remaining_sents2:
        return 0
    return sum(min(levenshtein_distance(sent1, sent2) for sent2 in remaining_sents2) for sent1 in remaining_sents1)

def a_star_search(doc1_sents, doc2_sents):
    start_state = (0, 0, 0)  # (index in doc1_sents, index in doc2_sents, accumulated cost)
    goal_state = (len(doc1_sents), len(doc2_sents))
    
    open_set = []
    heapq.heappush(open_set, (0, start_state))
    came_from = {}
    g_score = {start_state: 0}
    f_score = {start_state: heuristic(doc1_sents, doc2_sents)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if (current[0], current[1]) == goal_state:
            return reconstruct_path(came_from, current)
        
        for next_state in get_neighbors(current, doc1_sents, doc2_sents):
            tentative_g_score = g_score[current] + next_state[2]
            if next_state not in g_score or tentative_g_score < g_score[next_state]:
                came_from[next_state] = current
                g_score[next_state] = tentative_g_score
                f_score[next_state] = tentative_g_score + heuristic(doc1_sents[next_state[0]:], doc2_sents[next_state[1]:])
                heapq.heappush(open_set, (f_score[next_state], next_state))
    
    return None

def get_neighbors(state, doc1_sents, doc2_sents):
    neighbors = []
    i, j, cost = state
    
    if i < len(doc1_sents) and j < len(doc2_sents):
        neighbors.append((i + 1, j + 1, cost + levenshtein_distance(doc1_sents[i], doc2_sents[j])))
    if i < len(doc1_sents):
        neighbors.append((i + 1, j, cost + levenshtein_distance(doc1_sents[i], "")))
    if j < len(doc2_sents):
        neighbors.append((i, j + 1, cost + levenshtein_distance("", doc2_sents[j])))
    
    return neighbors

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def tokenize_and_normalize(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [re.sub(r'[^\w\s]', '', sentence).lower() for sentence in sentences]
    return sentences

def detect_plagiarism(doc1_text, doc2_text):
    doc1_sents = tokenize_and_normalize(doc1_text)
    doc2_sents = tokenize_and_normalize(doc2_text)
    
    alignment = a_star_search(doc1_sents, doc2_sents)
    
    plagiarism_pairs = []
    for (i, j, cost) in alignment:
        if i < len(doc1_sents) and j < len(doc2_sents) and cost < len(doc1_sents[i]) * 0.3:  # Example threshold
            plagiarism_pairs.append((doc1_sents[i], doc2_sents[j]))
    
    return plagiarism_pairs

def run_test_cases():
    test_cases = [
        {
            "name": "Identical Documents",
            "doc1": "This is a sample document. It contains several sentences.",
            "doc2": "This is a sample document. It contains several sentences.",
            "expected": [
                ("this is a sample document", "this is a sample document"),
                ("it contains several sentences", "it contains several sentences")
            ]
        },
        {
            "name": "Slightly Modified Document",
            "doc1": "This is a sample document. It contains several sentences.",
            "doc2": "This is a sample text. It includes several phrases.",
            "expected": [
                ("this is a sample document", "this is a sample text"),
                ("it contains several sentences", "it includes several phrases")
            ]
        },
        {
            "name": "Completely Different Documents",
            "doc1": "This is a sample document. It contains several sentences.",
            "doc2": "The quick brown fox jumps over the lazy dog.",
            "expected": []
        },
        {
            "name": "Partial Overlap",
            "doc1": "This is a sample document. It contains several sentences.",
            "doc2": "This is a sample document. It has some different sentences.",
            "expected": [
                ("this is a sample document", "this is a sample document")
            ]
        }
    ]
    
    for test in test_cases:
        print(f"Running test case: {test['name']}")
        plagiarism_pairs = detect_plagiarism(test["doc1"], test["doc2"])
        for pair in plagiarism_pairs:
            print(f"Plagiarized: {pair[0]} <-> {pair[1]}")
        print()

# Example usage for reading documents from user
doc1_path = 'path_to_doc1.docx'
doc2_path = 'path_to_doc2.docx'

doc1_text = read_docx(doc1_path)
doc2_text = read_docx(doc2_path)

plagiarism_pairs = detect_plagiarism(doc1_text, doc2_text)
for pair in plagiarism_pairs:
    print(f"Plagiarized: {pair[0]} <-> {pair[1]}")

# Run the test cases
run_test_cases()