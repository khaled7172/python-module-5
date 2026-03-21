from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    """
    This classs is an abstract class
    methods with the abstract decorator must be overridden by the child classes
    that extend from this class
    """
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return result


class NumericProcessor(DataProcessor):
    """
    We expect a list of numbers that contains ints or floats
    If not validated we return a string
    """

    def process(self, data: Any) -> str:
        if not self.validate(data):
            return "Numeric data has not been verified"
        count = len(data)
        total = sum(data)
        avg = total / count
        result = f"Processed {count} numeric values, sum={total}, avg={avg}"
        return self.format_output(result)

    def validate(self, data: Any) -> bool:
        if not isinstance(data, list):
            return False
        for elem in data:
            if not isinstance(elem, (int, float)):
                return False
        return True


class TextProcessor(DataProcessor):
    """
    We expect to receive a string
    """

    def process(self, data: Any) -> str:
        if not self.validate(data):
            return "Text data has not been verified"
        char_count = len(data)
        word_count = len(data.split())
        result = f"Processed text: {char_count} characters, {word_count} words"
        return self.format_output(result)

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)


class LogProcessor(DataProcessor):
    """
    We expect to receive a string with ERROR: or INFO: inside of it
    and we split it accordingly to return the log message
    """

    def process(self, data: Any) -> str:
        if not self.validate(data):
            return "Log data has not been verified"
        if "ERROR:" in data:
            log = data.split("ERROR: ")
            return f"[ALERT] ERROR level detected: {log[1]}"
        elif "INFO:" in data:
            log = data.split("INFO: ")
            return f"[INFO] INFO level detected: {log[1]}"
        return ""

    def validate(self, data: Any) -> bool:
        return isinstance(data, str) and ("ERROR:" in data or "INFO:" in data)


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    print()
    data_numeric = [1, 2, 3, 4, 5]
    data_text = "Hello Nexus World"
    data_log = "ERROR: Connection timeout"
    processors = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor()
    ]
    p = NumericProcessor()
    t = TextProcessor()
    log = LogProcessor()
    print("Initializing Numeric Processor...")
    print("Processing data: ", end="")
    print(f"{data_numeric}")
    print("Validation: Numeric data verified")
    print("Output: ", end="")
    print(p.process(data_numeric))
    print()
    print("Initializing Text Processor...")
    print("Processing data: ", end="")
    print(f'"{data_text}"')
    print("Validation: Text data verified")
    print("Output: ", end="")
    print(t.process(data_text))
    print()
    print("Initializing Log Processor...")
    print("Processing data: ", end="")
    print(f'"{data_log}"')
    print("Validation: Log entry verified")
    print("Output: ", end="")
    print(log.process(data_log))
    print()
    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    demo_numeric = [1, 2, 3]
    demo_text = "Hello Nexus!"
    demo_log = "INFO: System ready"
    processors_2 = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor()
    ]
    i = 1
    """
    using zip pairs each processor with its matching data
    """
    for processor, data in zip(
            processors_2, [demo_numeric, demo_text, demo_log]):
        print(f"Result {i}: {processor.process(data)}")
        i += 1
    print()
    print("Foundation systems online. Nexus ready for advanced streams.")
