# Overview

Flexceptions (Flexible Exceptions) is an error handling library for Python3.

If you want to achieve something more with Exceptions than just being screamed at, this is your library.

Flexceptions provides a BaseFlexception object with a *handle* method that can be used to create another object 
out of data stored in it when the Exception was raised, or to do whatever you like (such as activating a fallback 
mechanism, etc.). 

This simplifies sending relevant data back when an error happens, and processing it where you need or should, rather 
than having parts of your code deal with different types of unrelated return values or nested callbacks to avoid 
propagating an error.   

en lugar de subclassear excepcións porque sí, define excepcións habilmente

# Requirements

* Python (>=3.8)

# Installation

`pip install transformable-exceptions`


# Examples
#### Basic
```python

```

#### Inheritance
```python

```

#### Decorator