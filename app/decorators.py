import cProfile


def do_cprofile(func):
    # cProfile decorator function for timing function calls
    # just decorate with @do_cprofile for stats
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()

    return profiled_func