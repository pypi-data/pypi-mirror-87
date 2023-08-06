def check_h_align(h_align: str):

    if h_align not in ('left', 'center', 'right'):
        raise ValueError("h_align not in ('left', 'center', 'right')")
