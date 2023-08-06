# Dialectic

Mathematical logic implementation using python.

### Installation

```
pip install dialectic
```

### Usage

```python
# Import Atomic class
from dialectic import Atomic

# Build Atomic objects
a = Atomic('a')
b = Atomic('b')

# Invert
invert = ~a

# Conjunction
conjunction = (a & b)

# Disjunction
disjunction = (a | b)

# Implication
implication = (a > b)

# Equality (iff)
equality = (a == b)

# Validation with given sentence set
disjunction.validate({a})

# Parsing a sentence list
from dialectic import parse_sentences
parsed_set = parse_sentences([implication, a])
```