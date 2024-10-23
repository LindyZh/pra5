import requests
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "http://pra5-env-1.eba-mxwmqe2x.us-east-2.elasticbeanstalk.com"

def record_latency(endpoint, payload, csv_filename):
    latencies, start_times, end_times = [], [], []
    for _ in range(100):
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/{endpoint}", json=payload)
        end_time = time.time()
        latency = end_time - start_time
        latencies.append(latency)
        start_times.append(start_time)
        end_times.append(end_time)
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['start_time', 'end_time', 'latency'])
        for start_time, end_time, latency in zip(start_times, end_times, latencies):
            writer.writerow([start_time, end_time, latency])
    avg_latency = sum(latencies) / len(latencies)
    return avg_latency

def generate_boxplot(csv_filenames, output_image):
    data = {}
    for filename in csv_filenames:
        df = pd.read_csv(filename)
        data[filename] = df['latency']
    
    plt.figure(figsize=(10, 6))
    plt.boxplot(data.values(), labels=data.keys())
    plt.ylabel('Latency (seconds)')
    plt.title('API Latency Performance')
    plt.savefig(output_image)

def main():
    test_cases = [
        {"name": "fake_news_1", "payload": {'text': 'my cat can eat a dinansour'}},
        {"name": "fake_news_2", "payload": {'text': 'garlic prevent cancers.'}},
        {"name": "real_news_1", "payload": {'text': 'UofT is a University'}},
        {"name": "real_news_2", "payload": {'text': 'printer prints things'}}
    ]

    csv_filenames = []
    for case in test_cases:
        csv_filename = f"{case['name']}_latency.csv"
        avg_l = record_latency("predict", case['payload'], csv_filename)
        csv_filenames.append(csv_filename)
        print(f"{case['name']} avg latency: {avg_l}")
    
    generate_boxplot(csv_filenames, "boxplot.png")
    print("Boxplot generated.")

if __name__ == "__main__":
    main()