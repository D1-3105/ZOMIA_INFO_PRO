def get_tree() -> dict:
    """
    Stub for tree
    """
    return {
        1: {
            'link_to': [2, 3, 4],
            'pos': (130, 25)
        },
        2: {
            'link_to': [3],
            'pos': (150, 100)
        },
        3: {
            'link_to': [],
            'pos': (250, 130)
        },
        4: {
            'link_to': [1],
            'pos': (400, 500)
        }
    }
