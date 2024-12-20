def view_subterms_at_level(filename, search_terms, target_level=0, main_terms=None, current_path=None):
    """
    Shows subterms at any specified level for given search terms.
    
    Parameters:
    - filename: str, path to XML file
    - search_terms: list of str, terms to explore
    - target_level: int, the level at which to show detailed information (0-9)
                   0 = main terms, 1 = level 1 subterms, etc.
    - main_terms: str or list, the main term(s) to start from (required for levels > 0)
    - current_path: list, keeps track of the term hierarchy path (internal use)
    
    Returns:
    - dict: {search_term: [subterms_at_target_level]}
    """
    def print_term_details(element, prefix=""):
        """Helper function to print common term details"""
        code = element.find('code')
        if code is not None:
            print(f"{prefix}Code: {code.text}")
        
        see = element.find('see')
        if see is not None:
            print(f"{prefix}See Reference: {see.text}")
        
        see_also = element.find('seeAlso')
        if see_also is not None:
            print(f"{prefix}See Also Reference: {see_also.text}")
    
    def get_subterms_info(element):
        """Helper function to get subterms count and list"""
        subterms = element.findall('term')
        return len(subterms), [term.find('title').text for term in subterms]
    
    if current_path is None:
        current_path = []
    
    # Convert main_terms to list if it's a string
    if isinstance(main_terms, str):
        main_terms = [main_terms]
    
    tree = ET.parse(filename)
    root = tree.getroot()
    results = {}
    
    if target_level == 0:
        # Search for main terms
        for letter in root.findall('letter'):
            for main in letter.findall('mainTerm'):
                title = main.find('title').text
                if any(search_term.lower() in title.lower() for search_term in search_terms):
                    subterm_count, subterms = get_subterms_info(main)
                    
                    print(f"\nFound Main Term: {title}")
                    print(f"Level 1 Subterms: {subterm_count}")
                    print_term_details(main)
                    print("---")
                    results[title] = subterms
        
        print(f"\nTotal matching terms found: {len(results)}")
        return results
    
    if target_level == 1:
        # Special handling for level 1: show all immediate subterms of main terms
        for main_term in main_terms:
            for letter in root.findall('letter'):
                for main in letter.findall('mainTerm'):
                    if main.find('title').text == main_term:
                        print("\n" + "="*50)
                        print(f"MAIN TERM: {main_term}")
                        print("="*50)
                        
                        print_term_details(main)
                        print("\nLevel 1 Subterms:")
                        subterms = []
                        
                        for i, term in enumerate(main.findall('term'), 1):
                            title = term.find('title').text
                            subterms.append(title)
                            level2_count, _ = get_subterms_info(term)
                            
                            print(f"\n{i}. Subterm: {title}")
                            print(f"   Level 2 Subterms: {level2_count}")
                            print_term_details(term, "   ")
                        
                        print("\n" + "-"*50)
                        print(f"Total Level 1 Subterms found: {len(subterms)}")
                        results[main_term] = subterms
        
        return results
    
    def find_terms(element, current_level=0, path=None):
        if path is None:
            path = []
            
        if current_level == target_level - 1:
            # We're at the parent level of our target
            for term in element.findall('term'):
                term_title = term.find('title').text
                if term_title in search_terms:
                    subterms = []
                    
                    print("\n" + "="*50)
                    print(f"LEVEL {target_level-1} TERM: {term_title}")
                    print(f"Path: {' → '.join(path + [term_title])}")
                    print("="*50)
                    
                    print_term_details(term)
                    print(f"\nLevel {target_level} Subterms:")
                    
                    for i, subterm in enumerate(term.findall('term'), 1):
                        subtitle = subterm.find('title').text
                        subterms.append(subtitle)
                        next_level_count, _ = get_subterms_info(subterm)
                        
                        print(f"\n{i}. Subterm: {subtitle}")
                        print(f"   Level {target_level + 1} Subterms: {next_level_count}")
                        print_term_details(subterm, "   ")
                    
                    results[term_title] = subterms
                    print("\n" + "-"*50)
                    print(f"Total Level {target_level} Subterms found: {len(subterms)}")
            return
        
        # Continue searching deeper in the hierarchy
        for term in element.findall('term'):
            term_title = term.find('title').text
            find_terms(term, current_level + 1, path + [term_title])
    
    if main_terms is None and target_level > 0:
        raise ValueError("main_terms is required for levels > 0")
    
    # Start search from main terms for levels > 0
    for main_term in main_terms:
        for letter in root.findall('letter'):
            for main in letter.findall('mainTerm'):
                if main.find('title').text == main_term and target_level > 1:
                    find_terms(main, 1, [main_term])
    
    return results
