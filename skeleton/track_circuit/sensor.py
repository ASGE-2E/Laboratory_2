
# Train Sensor (track_circuit) — ERTMS T5
# Simulates speed, position, and physical condition detection.

import time, random

def read():
    return {
        'speed_kmh': round(random.uniform(0, 300), 1),
        'position': f'{random.uniform(40, 55):.4f}, {random.uniform(-5, 25):.4f}',
        'door_closed': random.choice([True, True, True, False]),
        'pantograph': 'UP'
    }

if __name__ == '__main__':
    while True:
        print(f'[SENSOR track_circuit]', read())
        time.sleep(0.5)
