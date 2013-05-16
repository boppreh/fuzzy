fuzzy
=====

Library for decision making based on fuzzy rules. The evaluation is
still a little rough, but it allows you to express cool conditions
like `ddos = all(very(parallel_requests), small_requests_interval)`
and `injection = all(bad_input, no(good_input))`.
