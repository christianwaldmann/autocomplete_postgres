from timeit import default_timer


"""
Functions tic() and toc() providing similar functionality like Matlab's tic toc.
Nested tic tocs are supported.
"""


start_times_for_tic_toc = []


def tic(reset_all_timers=False):
    """
    Start timer.
    :param reset_all_timers: Flag for resetting all timers. (All times are stored inside a list so nested tic-tocs work too. This flag is for resetting all.) (Default value = False)
    :type reset_all_timers: bool
    """
    start = default_timer()
    if reset_all_timers:
        # start_times_for_tic_toc.clear()       # only supported after py 3.3, so del will be used for the same effect
        del start_times_for_tic_toc[:]
    start_times_for_tic_toc.append(start)
    return start


def toc(msg='Elapsed time is', restart=False, hide_output=False):
    """
    End timer and print out elapsed time.
    :param msg: Message before printing out the elapsed seconds (Default value = 'Elapsed time is')
    :type msg: str
    :param restart: Flag for restarting the timer (Default value = False)
    :type restart: bool
    :param hide_output: Flag for hiding the print output (Default value = False)
    :type hide_output: bool
    """
    end = default_timer()
    elapsed = end - start_times_for_tic_toc[-1]
    start_times_for_tic_toc.pop()
    if not hide_output:
        print("%s %f seconds." % (msg, elapsed))
    if restart:
        start_times_for_tic_toc.append(end)
    return elapsed
