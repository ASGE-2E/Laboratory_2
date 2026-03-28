
# Balise (balise) — ERTMS T5
# Track-side transponder transmitting position reference data to passing trains.

BALISE_ID = 'balise'
POSITION_M = 12500 # metres from reference point

def transmit():
    return {
        'balise_id': BALISE_ID,
        'position_m': POSITION_M,
        'track_id': 'CORRIDOR-A',
        'signal': 'EUROBALISE-STM'
    }
if __name__ == '__main__':
    print('[BALISE]', transmit())
