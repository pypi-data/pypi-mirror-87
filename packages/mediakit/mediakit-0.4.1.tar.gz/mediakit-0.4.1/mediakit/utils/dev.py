def append_to_debug_output(debug_data, end='\n'):
    with open('debug.txt', 'a') as debug:
        debug.write(debug_data + end)
