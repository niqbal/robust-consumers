import multiprocessing

class DataReader:
    def read_data(self, batch_size):
        raise NotImplementedError

class FileDataReader(DataReader):
    def read_data(self, batch_size):
        # Simulate reading data from a file in batches
        for i in range(0, 100, batch_size):
            yield [f"data_{j}" for j in range(i, i + batch_size)]

class DBDataReader(DataReader):
    def read_data(self, batch_size):
        # Simulate reading data from a database in batches
        for i in range(0, 100, batch_size):
            yield [f"db_data_{j}" for j in range(i, i + batch_size)]

def data_reader(queue, data_source, batch_size, num_consumers):
    reader = None
    if data_source == "file":
        reader = FileDataReader()
    elif data_source == "db":
        reader = DBDataReader()

    for batch in reader.read_data(batch_size):
        queue.put(batch)

    # Send "STOP" messages after producing all data
    for _ in range(num_consumers):
        queue.put("STOP")


def consumer_producer(input_queue, output_queue):
    while True:
        batch = input_queue.get()
        if batch == "STOP":
            output_queue.put("STOP")
            break
        # Simulate processing
        processed_batch = [f"processed_{data}" for data in batch]
        output_queue.put(processed_batch)

def data_persister(queue, num_consumers):
    stop_count = 0
    while True:
        batch = queue.get()
        if batch == "STOP":
            stop_count += 1
            if stop_count == num_consumers:
                break
            continue
        # Simulate data persistence
        for data in batch:
            print(f"Persisted: {data}")

if __name__ == "__main__":
    batch_size = 10
    data_source = "file"  # or "db"
    num_consumers = 3

    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()

    producer = multiprocessing.Process(target=data_reader, args=(queue1, data_source, batch_size, num_consumers))
    consumers = [multiprocessing.Process(target=consumer_producer, args=(queue1, queue2)) for _ in range(num_consumers)]
    persister = multiprocessing.Process(target=data_persister, args=(queue2, num_consumers))

    producer.start()
    for consumer in consumers:
        consumer.start()
    persister.start()

    producer.join()
    for consumer in consumers:
        consumer.join()

    persister.join()
