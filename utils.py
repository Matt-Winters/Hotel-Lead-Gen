from fuzzywuzzy import fuzz

def find_best_matching_link(all_links, search_query):
    best_match = None
    best_match_score = 80
    # link_text_before_dash: str
    for link in all_links:
        link_text_parts = link.text.split('-', 1)
        link_text_before_dash = link_text_parts[0] if len(link_text_parts) > 0 else link.text
        if len(link_text_before_dash.split(' ')) < 2:
            continue 
        similarity_score = fuzz.partial_ratio(search_query.lower(), link_text_before_dash.lower())
        
        if similarity_score > best_match_score:
            best_match_score = similarity_score
            best_match = link
    
    return best_match

def find_best_matching_link_word_split(all_links, search_query):
    best_match = None
    best_match_score = 0

    for link in all_links:
        link_text_parts = link.text.split('-', 1)
        link_text_before_dash = link_text_parts[0] if len(link_text_parts) > 0 else link.text

        words_in_search_query = search_query.lower().split()
        words_in_link_text = link_text_before_dash.lower().split()

        total_score = 0

        for word_query in words_in_search_query:
            for word_link in words_in_link_text:
                word_score = fuzz.partial_ratio(word_query, word_link)
                total_score += word_score

        average_score = total_score / (len(words_in_search_query) * len(words_in_link_text))

        if average_score > best_match_score:
            best_match_score = average_score
            best_match = link

    return best_match

