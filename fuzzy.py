from __future__ import division

def modifier(m):
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
def evaluate(rules, parameter):
    combined_command = defaultdict(lambda: 0.0)
    max_command = defaultdict(lambda: 0.0)
    for fuzzy_function, command in rules.items():
        fuzzy_value = fuzzy_function(parameter)
        for key, value in command.items():
            combined_command[key] += fuzzy_value * value
            max_command[key] += value

    final_command = defaultdict(lambda: 0.0)
    for key in combined_command:
        final_command[key] = combined_command[key] / max_command[key]
    return final_command


def triangle(x, a, b, c):
    return max(0, min((x - a) / (b - a), (c - x) / (c - b)))

def left_slope(x, a, b):
    return min(1, max(x - a, 0) / (b))

def right_slope(x, a, b):
    return 1 - left_slope(x, a, b)

if __name__ == '__main__':
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
