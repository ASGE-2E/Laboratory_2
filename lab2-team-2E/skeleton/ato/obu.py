
# Onboard Unit (ato) — ERTMS T5
# Simulates the main computing unit aboard the train.

import time, random

def read_sensors():
    return {
        'speed_kmh': round(random.uniform(0, 300), 1),
        'position': f'{random.uniform(40, 55):.4f}, {random.uniform(-5, 25):.4f}'
    }

def send_to_ground(data):
    print(f'[OBU ato] Sending to ground control: {data}')

def receive_command(cmd):
    print(f'[OBU ato] Command received: {cmd}')
    if cmd.get('action') == 'BRAKE':
        apply_brake(cmd.get('intensity', 1.0))

def apply_brake(intensity):
    print(f'[OBU ato] Applying brake at intensity {intensity}')

if __name__ == '__main__':
    while True:
        data = read_sensors()
        send_to_ground(data)
        time.sleep(1)
