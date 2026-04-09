
# Brake Actuator (brake_actuator) — ERTMS T5
# Receives control commands and acts on the physical train.

def execute(command):
    action = command.get('action')
    intensity = command.get('intensity', 1.0)
    if action == 'BRAKE':
        print(f'[ACTUATOR brake_actuator] Emergency brake — intensity {intensity}')
    elif action == 'RELEASE':
        print(f'[ACTUATOR brake_actuator] Brake released')
    else:
        print(f'[ACTUATOR brake_actuator] Unknown command: {action}')

if __name__ == '__main__':
    execute({'action': 'BRAKE', 'intensity': 0.8})
