# simple_assertion
A package offering Python functions for simple and readable assertions to be used inside code (outside of testing)

# Modules
The module assrrt_functions offers t he main functions. It uses helper functions from the comparisons module, which in turn offer functions to enable using string-formatter operators (e.g., `"less than"` alias `"less_than"` alias `"lt"`).

# doctests
The modules is covered with doctests, which you can run via

```
python -m doctests assert_functions.py
python -m doctests comparisons.py
```
