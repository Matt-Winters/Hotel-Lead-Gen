from fuzzywuzzy import fuzz

def find_best_matching_link(all_links, search_query):
    best_match = None
    best_match_score = 0

    for link in all_links:
        link_text_parts = link.text.split('-', 1)
        link_text_before_dash = link_text_parts[0] if len(link_text_parts) > 0 else link.text

        similarity_score = fuzz.partial_ratio(search_query.lower(), link_text_before_dash.lower())

        if similarity_score > best_match_score:
            best_match_score = similarity_score
            best_match = link

    return best_match