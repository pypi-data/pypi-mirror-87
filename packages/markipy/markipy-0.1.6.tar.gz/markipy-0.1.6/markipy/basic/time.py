from time import gmtime, strftime, time_ns

# Now
now = lambda: gmtime()

# Time Now Formatted
datetime = lambda: strftime('%Y.%m.%d.%H.%M.%S', now())

# Time Now Formatted
date = lambda: strftime('%Y.%m.%d', now())

# Time clock
clock = lambda: strftime('%H:%M:%S', now())
