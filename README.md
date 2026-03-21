*This project has been created as part of the 42 curriculum by khhammou*

## Description
abstract base class:
cannot be used directly
defines the interface
child classes must implement required methods
syntax:
class ClassName(ABC):
abstract methods are declared by parent class
and must be implemented by all child classes
syntax example:
@abstractmethod #tells python any subclass must implement this function
def method_name(self, data: Any) -> str:
self refers to object calling the method
data: Any is a type hint
meaning data can be any type
-> str means functions must return a string
default methods can be overridden by child classes but they dont have to
child classses inherit from parent class
it allows for overriding behavior
class Numeric(Data): means Numeric IS A Data
overriding methods is each subclass implementing the methods again in the children changing what it does
Polymorphism:
for example you can create a list of all the children of the parent class
and loop on them and call a specific method
and python would choose the correct implementation since this method does a diff thing in each child
method overriding is a subclass provides its own implementation of a method defined in the parent class
polymorphism is using the same method call on different objects that behave differently

# Code Nexus — Polymorphic Data Streams in the Digital Matrix

## Overview

A Python OOP project demonstrating **method overriding** and **subtype polymorphism** through a data processing pipeline system. Three exercises build progressively from a basic processor foundation to a full enterprise pipeline.

---

## Project Structure

```
.
├── ex0/
│   └── stream_processor.py
├── ex1/
│   └── data_stream.py
├── ex2/
│   └── nexus_pipeline.py
└── README.md
```

---

## Exercises

### Exercise 0 — Data Processor Foundation (`ex0/`)

Builds the base processor architecture using an abstract base class and method overriding.

**Classes:**
- `DataProcessor` — ABC with abstract `process()` and `validate()`, default `format_output()`
- `NumericProcessor` — processes lists of numbers, computes sum and average
- `TextProcessor` — processes strings, counts characters and words
- `LogProcessor` — parses ERROR/INFO log entries and formats alerts

**Run:**
```bash
python3 ex0/stream_processor.py
```

---

### Exercise 1 — Polymorphic Streams (`ex1/`)

Builds adaptive data streams that handle multiple data types simultaneously.

**Classes:**
- `DataStream` — ABC with abstract `process_batch()`, default `filter_data()` and `get_stats()`
- `SensorStream` — processes environmental sensor readings, computes averages
- `TransactionStream` — processes buy/sell operations, tracks net flow
- `EventStream` — processes system events, tracks error count
- `StreamProcessor` — orchestrates multiple stream types through a unified interface

**Run:**
```bash
python3 ex1/data_stream.py
```

---

### Exercise 2 — Nexus Integration (`ex2/`)

Integrates everything into a complete enterprise-scale pipeline system.

**Classes:**
- `ProcessingStage` — Protocol (duck typing) interface requiring a `process()` method
- `InputStage`, `TransformStage`, `OutputStage` — concrete stage implementations
- `ProcessingPipeline` — ABC managing a list of stages, orchestrates data flow
- `JSONAdapter` — handles JSON dict input, validates temperature range
- `CSVAdapter` — handles CSV string input, parses column structure
- `StreamAdapter` — handles real-time stream dicts, computes averages
- `NexusManager` — registers and runs multiple pipelines, supports chaining

**Run:**
```bash
python3 ex2/nexus_pipeline.py
```

---

## Key Concepts Demonstrated

**Method Overriding** — subclasses override parent methods to provide specialized behavior while maintaining the same interface signature.

**Subtype Polymorphism** — `StreamProcessor` and `NexusManager` handle any subtype through their base class reference without knowing the specific implementation.

**ABC vs Protocol** — Exercise 0 and 1 use `ABC` with `@abstractmethod` to enforce implementation. Exercise 2 introduces `Protocol` for duck typing, where no explicit inheritance is required.

**Pipeline Chaining** — `NexusManager.chain()` feeds the output of one pipeline as the input of the next, demonstrating composable polymorphic design.

---

## Standards

- Python 3.10+
- flake8 compliant (max line length 79)
- Full type annotations using `typing` module (`Any`, `List`, `Dict`, `Union`, `Optional`)
- ABC and `@abstractmethod` used throughout
- Exception handling on all data processing methods
- Standard library only

### Instructions

You run this code by doing python3 file_name.py

## Resources

The internet

## AI Usage

Testing my code with test cases and helping me find syntax errors