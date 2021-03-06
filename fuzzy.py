from __future__ import division

def modifier(m):
    """
    Converts a numeric function into one that can wrap another function.
    Example: modifier(lambda x: x * 2)(lambda x: x + 1)(4) -> 10.
    """
    def wrapper(*fns):
        def caller(*args, **kwargs):
            return m(*[fn(*args, **kwargs) for fn in fns])
        return caller
    return wrapper

@modifier
def very(x): return x ** 2

@modifier
def extremely(x): return x ** 3

@modifier
def some(x): return x ** (1/2.0)

@modifier
def all(*xs): return min(*xs)

@modifier
def any(*xs): return max(*xs)

@modifier
def no(x): return 1 - x


from collections import defaultdict
def evaluate(rules, *parameters):
    """
    Makes a decision from `rules` applied to `parameters`.

    `rules` is a dictionary mapping fuzzy functions to dictionaries of numeric
    outcomes. For example: {very(far): {'acceleration': 50, 'breaks': 0.0}}

    All rules are evaluated to the given parameter, and the "center of mass" of
    the total membership graphs is taken. The result is a composite rule.
    """
    combined_command = defaultdict(lambda: 0.0)
    max_command = defaultdict(lambda: 0.0)
    for fuzzy_function, command in rules.items():
        fuzzy_value = fuzzy_function(*parameters)
        for key, value in command.items():
            combined_command[key] += fuzzy_value * value
            max_command[key] += value

    final_command = defaultdict(lambda: 0.0)
    for key in combined_command:
        if not max_command[key]:
            continue
        final_command[key] = combined_command[key] / max_command[key]
    return final_command


def triangle(x, a, b, c):
    """
    Returns the membership of x in a triangle made of a, b and c.
    
    The triangle has height 1 and peak at b.
    """
    return max(0, min((x - a) / (b - a), (c - x) / (c - b)))

def left_slope(x, a, b):
    """
    Returns the membership of x in a right facing slope graph.
    _
     \_
    """
    return min(1, max(x - a, 0) / (b))

def right_slope(x, a, b):
    """
    Returns the membership of x in a left facing slope graph.
      _
    _/
    """
    return 1 - left_slope(x, a, b)

if __name__ == '__main__':
    ################
    # Road example #
    ################

    angle = 25
    snow_amount = 2

    def straight():
        return triangle(angle, -90, 0, 90)

    def slippery():
        return left_slope(snow_amount, 0, 3)
        

    rules = {
        very(straight): {'acceleration': 0.9, 'brake': 0.0},
        some(slippery): {'acceleration': 0.1, 'brake': 0.5}
    }

    results = evaluate(rules)
    print 'Target acceleration:', results['acceleration']
    print 'Target braking:', results['brake']


    ##################
    # Hacker Example #
    ##################

    def parallel_requests(user):
        return left_slope(user['parallel requests'], 0, 5)

    def small_requests_interval(user):
        return right_slope(user['requests interval'], 0.3, 0.01)

    def bad_input(user):
        return user['bad input'] / user['all input']

    def good_input(user):
        return user['good input'] / user['all input']

    def found_in_blacklists(user):
        return user['in blacklists'] / user['total blacklists']

    ddos = all(very(parallel_requests), small_requests_interval)
    injection = all(bad_input, no(good_input))
    hijacked = some(found_in_blacklists)

    rules = {
        ddos: {'rate limit': 1.0, 'ban': 0.4},
        injection: {'rate limit': 0.6, 'ban': 0.9},
        hijacked: {'rate limit': 0.3, 'ban': 0.3}
    }

    test_user = {'parallel requests': 3,
                 'requests interval': 0.5,
                 'bad input': 100,
                 'good input': 50,
                 'all input': 150,
                 'in blacklists': 1,
                 'total blacklists': 15,
                }

    evaluation = evaluate(rules, test_user)
    print 'Should ban?', evaluation['ban']
    print 'Should rate limit?', evaluation['rate limit']
