# python-module-5
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


Go crazy:
autopep8 --in-place --aggressive --aggressive ft_garden_management.py
### Instructions

You run this code by doing python3 file_name.py

## Resources

The internet

## AI Usage

Testing my code with test cases and helping me find syntax errors