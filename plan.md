# Detailed Video Presentation Plan: Metaprogramming

Estimated duration: ~**50 minutes**.


## Step 1: Introduction – What Is Metaprogramming in Python? (`00:00–04:30`, ~4.5 min)
- **Definition of metaprogramming in practice:**
  - Writing code that treats other code (objects, functions, classes, modules, expressions, signatures, or syntax trees) as data.
  - Distinguishing between regular application code (processing domain data) and metaprogramming code (inspecting, modifying, or generating other parts of a program).
- **Roadmap of mechanisms in Python (from simplest to most advanced):**
  - **Introspection** – reading information about objects, types, attributes, signatures, and inheritance relationships without altering their state.
  - **Reflection** – dynamically checking, getting, changing, deleting, or creating attributes and classes while the program runs.
  - **Decorators** – wrapping and modifying functions, methods, and classes declaratively.
  - **Dynamic code and AST** – loading modules on the fly (`importlib`), compiling/executing code (`compile`, `exec`, `eval`), and inspecting/transforming syntax trees (`ast`).
  - **Metaclasses** – controlling the class creation process and class namespaces themselves (along with simpler alternatives such as `__init_subclass__`).
- **Reflection in C++26:**
  - Independent coverage of the C++26 reflection library (the `^^` operator, `std::meta::info`, functions in `consteval`, and splicing `[: ... :]`)


## Step 2: Introspection and Reflection in Python ( ~10 min)
- **1. Introspection – built-in functions:**
  - `type(obj)` and `isinstance(obj, cls_or_tuple)` – differences, inheritance, type tuples, working with `abc` (*Abstract Base Classes*) and `@runtime_checkable` protocols from `typing`.
  - `issubclass(cls, cls_or_tuple)` – inspecting class hierarchies.
  - `dir([obj])`, `vars([obj])`, `globals()`, `locals()` – exploring namespaces and attributes; explaining the difference between `dir()` and `vars()`, and why mutating `locals()` inside a function is unreliable.
  - `callable(obj)` – checking whether an object can be called (functions, methods, classes, objects implementing `__call__`).
- **2. Dunder attributes and the object model:**
  - `__dict__` and `__slots__` – how instance and class attributes are stored, what `__slots__` changes, and when `__dict__` still appears alongside `__slots__`.
  - `__class__`, `__bases__`, `__mro__` – how *Method Resolution Order* (*C3 linearization*) works under multiple inheritance and how to inspect attribute lookup order.
  - `__subclasses__()` – retrieving current direct subclasses (e.g., for lightweight registries).
  - `__annotations__` and `typing.get_type_hints()` – reading type annotations and why `get_type_hints()` matters.
- **3. The `inspect` module in action:**
  - Object classification predicates: `inspect.isfunction()`, `ismethod()`, `isclass()`, `ismodule()`, `iscoroutinefunction()`, `isgeneratorfunction()`, `isroutine()`.
  - `inspect.signature()`, `Parameter`, and `BoundArguments`:
    - inspecting parameter kinds (`.kind`: positional-only, positional-or-keyword, `*args`, keyword-only, `**kwargs`), defaults (`.default`, `Parameter.empty`), and annotations (`.annotation`),
    - using `sig.bind(*args, **kwargs)` / `sig.bind_partial()` and `.apply_defaults()` for automatic argument binding in decorators, validators, or command parsers.
  - `inspect.getsource()`, `inspect.getsourcelines()`, `inspect.getdoc()`, `inspect.cleandoc()`, `inspect.getfile()`.
  - `inspect.currentframe()`, `inspect.stack()`, `inspect.getouterframes()` – inspecting the call stack and caller context.
- **4. Reflection – dynamic operations on attributes and classes:**
  - `getattr(obj, name[, default])`, `setattr(obj, name, value)`, `hasattr(obj, name)`, `delattr(obj, name)` – dynamically querying, modifying, and deleting attributes using string names.
  - Three-argument `type(name, bases, namespace)` – creating a new class on the fly without `class ...:` syntax.
- **5. Pitfalls and technical nuances:**
  - `hasattr()` calls `getattr()` under the hood and catches `AttributeError` – it can execute code inside a `@property` or mask an internal `AttributeError` inside a getter.
  - Stack frames (`inspect.currentframe()` / `stack()`) can create reference cycles if not cleaned up properly (`del frame` in a `finally` block).


## Step 3: Decorators in Python ( ~10 min)
- **1. How decorators work:**
  - What `@decorator` syntax means – syntactic sugar for `func = decorator(func)` (and analogously for classes).
  - The difference between code executed at decoration time (function/class definition) and code executed on each call to the wrapped callable.
- **2. Function decorators – from simple to advanced:**
  - Simple logging or timing decorator using `*args` and `**kwargs`.
  - Parameterized decorators (decorator factories – e.g., `@retry(times=3)` or `@require_role("admin")`) and the pattern for a decorator that works both as `@dec` and `@dec(arg)`.
  - Combining decorators with `inspect.signature()` and `sig.bind()` – e.g., automatic validation of argument types or values before calling the function.
- **3. Critical role of `functools.wraps` and `functools.update_wrapper`:**
  - What happens without `@functools.wraps(func)` – the function takes the name `wrapper`, losing its docstring, annotations, and original signature in `help()` and documentation/testing tools.
  - What `@functools.wraps(func)` does – copies key attributes (`__name__`, `__qualname__`, `__doc__`, `__annotations__`, `__dict__`) and sets `__wrapped__`, enabling `functools.unwrap()` or `inspect.signature(fn, follow_wrapped=False)`.
- **4. Class decorators:**
  - How a class decorator receives a class and returns a class (modified or newly constructed).
  - Practical scenarios: automatically registering classes in a dictionary (e.g., mapping commands or events to handler classes), adding helper methods, or attaching metadata attributes.
- **5. Brief look at descriptors behind built-in decorators:**
  - Why `@property`, `@classmethod`, and `@staticmethod` work the way they do (the descriptor protocol: `__get__`, `__set__`, `__delete__`).


## Step 4: Dynamic Code, `importlib`, and `ast` in Python ( ~9 min)
- **1. Dynamic module loading with `importlib`:**
  - `importlib.import_module()` – loading modules or packages by name at runtime (e.g., a plugin system).
  - `importlib.reload()` and loading from a file path (`importlib.util.spec_from_file_location()` + `module_from_spec()`) – when and how to use them.
- **2. Compiling and executing code: `compile()`, `exec()`, `eval()`:**
  - `compile(source, filename, mode)` – compiling source code or an AST into a `code object` in `'exec'`, `'eval'`, and `'single'` modes.
  - `exec(object, globals=None, locals=None)` – executing blocks of statements, function definitions, or classes.
  - `eval(expression, globals=None, locals=None)` – evaluating a single expression and returning its result; the role of `globals` and `locals` dictionaries.
- **3. Abstract syntax trees – the `ast` module:**
  - `ast.parse()` – turning source code into an *Abstract Syntax Tree* and inspecting nodes (`ast.dump()`, `ast.walk()`).
  - `ast.NodeVisitor` and `ast.NodeTransformer` – analyzing code (e.g., detecting specific calls or structures) and transforming the tree before calling `ast.fix_missing_locations()`, `compile()`, and `exec()`.
- **4. Security and safe alternatives:**
  - Why running `eval()` or `exec()` on external or untrusted input is dangerous.
  - Why attempting to "sandbox" `eval`/`exec` by passing empty `__builtins__` or naive name blocklists fails (e.g., traversal chains via `__class__`, `__mro__`, `__subclasses__()`).
  - `ast.literal_eval()` – safely parsing Python literals (dicts, lists, tuples, numbers, strings, booleans, `None`) without executing arbitrary code.


## Step 5: Metaclasses in Python (~10 min)
- **1. What a metaclass is and how `type` works:**
  - In Python, classes are objects (instances of their metaclasses); the default metaclass for most classes is `type`.
  - The relationship between instance, class, and metaclass (`obj` → `cls` → `type`).
- **2. Full class creation lifecycle through a metaclass:**
  - Selecting the metaclass from `metaclass=...` in the class definition and from base classes (and what happens on metaclass conflicts in multiple inheritance).
  - `meta.__prepare__(name, bases, **kwds)` – creating the mapping (default `dict`, or a custom mapping such as one detecting duplicates or recording attribute order) used while executing the class body.
  - Executing the class body inside the prepared namespace.
  - `meta.__new__(mcs, name, bases, namespace, **kwds)` – creating and returning the new class object (e.g., modifying `namespace` or `bases` before the class is created).
  - `meta.__init__(cls, name, bases, namespace, **kwds)` – configuring, registering, or validating the newly created class.
- **3. Practical use cases for metaclasses:**
  - Enforcing design conventions right at class definition time (e.g., required attributes, methods, or naming rules).
  - Automatic component registration or enriching/shaping class structure.
- **4. Modern, simpler alternatives to metaclasses:**
  - `__init_subclass__(cls, **kwargs)` – hook automatically called on the base class when a subclass is created; handles subclass registration and validation without writing a metaclass or risking metaclass conflicts.
  - `__set_name__(self, owner, name)` on descriptors – letting a descriptor learn the attribute name on the class without a metaclass.


## Step 6: Summary of the Python Section and Best Practices ( ~3 min)
- **1. Choosing the right mechanism for the problem size:**
  - Plain functions, classes, dictionaries, and simple polymorphism – when they suffice, keep the code simple.
  - Decorators (`@functools.wraps`) and `inspect` – for wrapping, logging, validation, and registration without repeating logic.
  - `__init_subclass__` and descriptors with `__set_name__` – for behaviors tied to inheritance or class fields.
  - `importlib`, `ast`, `exec`/`eval`, and custom metaclasses – only when they provide clear architectural value that justifies the added complexity.
- **2. Key code hygiene rules:**
  - Readability and predictability for teammates (as well as IDEs and static type checkers).
  - Awareness of costs (execution time, memory overhead, harder debugging with deep metaprogramming) and security risks when executing dynamic code.
- **3. Hands-on exercise for participants:**
  - Concrete practice task combining mechanisms covered in Python (e.g., a decorator using `functools.wraps` and `inspect.signature()` paired with class registration via `__init_subclass__` or a class decorator).

---

## Step 7: Bonus – Reflection Mechanism in C++26 (`<meta>`) ( ~4 min)
- **1. Introducing the bonus segment:**
  - Clearly positioning this as a standalone bonus segment for viewers curious about how reflection works in the C++26 standard via the `<meta>` library.
- **2. Core concepts and syntax in C++26 `<meta>`:**
  - The `<meta>` header and the `std::meta` namespace.
  - The `^^` operator – produces a `std::meta::info` reflection value representing a compile-time entity (such as a type, class/struct member, variable, or function).
- **3. Working with metadata and the splice operator `[: ... :]`:**
  - Calling functions from `std::meta` inside `consteval` / `constexpr` functions and expressions to inspect a type and its members (e.g., names, types, fields).
  - The splice operator `[: ... :]` – splicing a reflected entity back into C++ source code at compile time (e.g., as a type, member/name, or expression).
- **4. Practical purpose of this mechanism:**
  - Enables writing code that adapts to type structure (such as serialization, comparisons, mappings, or field inspection) directly in C++ without manually duplicating repetitive code snippets.
