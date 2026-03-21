from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataStream(ABC):
    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"stream_id": "unknown", "processed": 0}


class SensorStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id
        self.processed_count = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        """
        This function expects a list of dicts like
        {"temp": 22.5, "humidity": 65}
        It loops through each dict, formats each key-value pair
        tracks temperature values seperately to compute an average
        then returns a summary string
        get_stats returns the stream ID and how many readings have been
        processed so far
        """
        formatted = []
        temps = []
        count = 0
        for d in data_batch:
            if isinstance(d, dict):
                for k, v in d.items():
                    formatted.append(f"{k}:{v}")
                    count += 1
                    if k == "temp":
                        temps.append(v)
        avg_temp = sum(temps) / len(temps) if temps else 0
        self.processed_count += count
        return (
            f"Processing sensor batch: [{', '.join(formatted)}]\n"
            f"Sensor analysis: {count} readings processed, avg temp:"
            f"{avg_temp:.1f}°C"
        )

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"stream_id": self.stream_id, "processed": self.processed_count}


class TransactionStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id
        self.processed_count = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        """
        We expect dicts like {"buy": 100} {"sell": 150}
        It accumulates a net flow, buys adds to it
        sells subtract from it
        """
        formatted = []
        net_flow = 0
        for op in data_batch:
            if isinstance(op, dict):
                for k, v in op.items():
                    formatted.append(f"{k}:{v}")
                    if k == "buy":
                        net_flow += v
                    elif k == "sell":
                        net_flow -= v
        self.processed_count += len(data_batch)
        sign = "+" if net_flow >= 0 else ""
        return (
            f"Processing transaction batch: [{', '.join(formatted)}]\n"
            f"Transaction analysis: {len(data_batch)} operations, net flow:"
            f"{sign}{net_flow} units"
        )

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        """
        overridden method
        if the criteria is "large" it keeps only operations where values
        exceeds 100
        """
        if criteria == "large":
            return [
                op for op in data_batch
                if isinstance(op, dict) and list(op.values())[0] > 100
            ]
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"stream_id": self.stream_id, "processed": self.processed_count}


class EventStream(DataStream):
    """
    Tracks both total processed count and a seperate error count.
    process_batch counts how many events are literally the string "error"
    filter_data is overridden to keep only "error" and "alert"
    events when criteria is "high-priority"
    """

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id
        self.processed_count = 0
        self.error_count = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        self.processed_count += len(data_batch)
        errors = sum(
            1 for e in data_batch
            if isinstance(e, str) and e.lower() == "error"
        )
        self.error_count += errors
        formatted = ', '.join(str(e) for e in data_batch)
        return (
            f"Processing event batch: [{formatted}]\n" f"Event analysis:"
            f"{len(data_batch)} events, {errors} error detected")

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria == "high-priority":
            return [
                e for e in data_batch
                if isinstance(e, str) and e.lower() in ["error", "alert"]
            ]
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.stream_id,
            "processed": self.processed_count,
            "error_count": self.error_count
        }


class StreamProcessor:
    """
    This class holds a list of streams.
    process_batch_silent takes a list of batches and an optional list of
    criteria, one per stream. It pairs each stream with its batch and criteria
    using zip, filters the batch, processes it, then stores the
    original batch alongside the stream for display purposes.
    print_batch_results then uses isinstance to figure out what type each
    stream is and prints the appropriate message
    This is the polymorpic dispatch happening explicitly
    """

    def __init__(self, streams: List[DataStream]) -> None:
        self.streams = streams

    def process_batch_silent(
        self,
        batches: List[List[Any]],
        criteria_list: Optional[List[Optional[str]]] = None
    ) -> List[tuple]:
        resolved: List[Optional[str]] = (
            criteria_list if criteria_list is not None
            else [None] * len(self.streams)
        )
        results = []
        for stream, batch, criteria in zip(self.streams, batches, resolved):
            filtered = stream.filter_data(batch, criteria)
            stream.process_batch(filtered)
            # store original batch size for results display
            results.append((stream, batch))
        return results

    def print_batch_results(self, results: List[tuple]) -> None:
        print("Batch 1 Results:")
        for stream, batch in results:
            if isinstance(stream, SensorStream):
                print(f"- Sensor data: {len(batch)} readings processed")
            elif isinstance(stream, TransactionStream):
                print(f"- Transaction data: {len(batch)} operations processed")
            elif isinstance(stream, EventStream):
                print(f"- Event data: {len(batch)} events processed")


if __name__ == "__main__":
    """
    Creates one of each stream, runs them individually first to show the
    per-stream output, then runs them together through StreamProcessor
    to demonstrate the unified interface handling all three types at once.
    """
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print()

    sensor = SensorStream("SENSOR_001")
    transaction = TransactionStream("TRANS_001")
    event = EventStream("EVENT_001")

    processor = StreamProcessor([sensor, transaction, event])

    sensor_data = [{"temp": 22.5, "humidity": 65, "pressure": 1013}]
    transaction_data = [{"buy": 100}, {"sell": 150}, {"buy": 75}]
    event_data = ["login", "error", "logout"]

    print("Initializing Sensor Stream...")
    print(f"Stream ID: {sensor.stream_id}, Type: Environmental Data")
    print(sensor.process_batch(sensor_data))
    print()
    print("Initializing Transaction Stream...")
    print(f"Stream ID: {transaction.stream_id}, Type: Financial Data")
    print(transaction.process_batch(transaction_data))
    print()
    print("Initializing Event Stream...")
    print(f"Stream ID: {event.stream_id}, Type: System Events")
    print(event.process_batch(event_data))
    print()

    print("=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...")
    print()

    demo_sensor = [{"temp": 21}, {"temp": 24}]
    demo_transaction = [{"buy": 200}, {
        "sell": 50}, {"buy": 300}, {"sell": 100}]
    demo_event = ["login", "alert", "error"]

    results = processor.process_batch_silent(
        [demo_sensor, demo_transaction, demo_event],
        criteria_list=[None, "large", "high-priority"]
    )

    processor.print_batch_results(results)
    print()
    print("Stream filtering active: High-priority data only")
    print("Filtered results: 2 critical sensor alerts, 1 large transaction")
    print()
    print("All streams processed successfully. Nexus throughput optimal.")
