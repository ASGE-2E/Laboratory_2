import os
import textwrap

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def build_path(*paths):
    return os.path.join(BASE_DIR, *paths)

# ─────────────────────────────────────────────
# T1 — Presentation
# ─────────────────────────────────────────────

def generate_web_interface(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'index.html'), 'w') as f:
        f.write(textwrap.dedent(f"""
            <!DOCTYPE html>
            <html>
            <head><title>{name} — Passenger Portal</title></head>
            <body>
                <h1>ERTMS Passenger Portal</h1>
                <p>Component: {name}</p>
            </body>
            </html>
        """))

    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM nginx:alpine
            COPY index.html /usr/share/nginx/html/index.html
        """))

def generate_operator_ui(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'dashboard.html'), 'w') as f:
        f.write(textwrap.dedent(f"""
            <!DOCTYPE html>
            <html>
            <head><title>{name} — Operator Dashboard</title></head>
            <body>
                <h1>ERTMS Operator Dashboard</h1>
                <p>Component: {name}</p>
            <p>Status: Monitoring active routes...</p>
            </body>
            </html>
        """))

    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM nginx:alpine
            COPY dashboard.html /usr/share/nginx/html/index.html
        """))

def generate_driver_ui(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'driver.html'), 'w') as f:
        f.write(textwrap.dedent(f"""
            <!DOCTYPE html>
            <html>
            <head><title>{name} — Driver Interface</title></head>
            <body>
                <h1>ERTMS Driver Interface</h1>
                <p>Component: {name}</p>
            <p>Movement Authority: PENDING</p>
            </body>
            </html>
        """))

    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM nginx:alpine
            COPY driver.html /usr/share/nginx/html/index.html
        """))

def generate_display(name):
    """Genera pantallas físicas de información (estaciones/andenes)."""
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, 'display.html'), 'w') as f:
        f.write(textwrap.dedent(f"""
            <html>
            <body>
                <h1>Display: {name}</h1>
                <p>Next Train: 5 min</p>
            </body>
            </html>
        """))
    
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM nginx:alpine
            COPY display.html /usr/share/nginx/html/index.html
        """))

# ─────────────────────────────────────────────
# T2 — Communication
# ─────────────────────────────────────────────

def generate_api_gateway(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'app.py'), 'w') as f:
        f.write(textwrap.dedent(f"""
            from flask import Flask, request, jsonify
            import requests
                                
            app = Flask(__name__)
                                
            ROUTES = {{
                '/passengers': 'http://passengers_ms:80',
                '/routes': 'http://routes_ms:80',
                '/trains': 'http://trains_ms:80',
                '/position': 'http://position_time_ms:80',
                '/tickets': 'http://tickets_ms:80',
                '/authority': 'http://mas:80',
            }}
                                
            @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
                                
            def gateway(path):
                for prefix, target in ROUTES.items():
                    if ('/' + path).startswith(prefix):
                        internal_path = ('/' + path).replace(prefix, '', 1)
                        url = target + '/' + internal_path
                        resp = requests.request(
                            method=request.method,
                            url=url,
                            json=request.get_json(silent=True)
                        )
                        return jsonify(resp.json()), resp.status_code
                return jsonify(error='Route not found'), 404
            
            if __name__ == '__main__':
                app.run(host='0.0.0.0', port=80)
        """))

    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM python:3.11-slim
            WORKDIR /app
            COPY . .
            RUN pip install flask requests
            CMD ["python", "app.py"]
        """))

def generate_interface(name):
    """Componentes de integración como ETML Interface."""
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, 'interface.py'), 'w') as f:
        f.write(f"print('External Interface {name} active...')")
    
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM python:3.11-slim
            WORKDIR /app
            COPY . .
            CMD ["python", "interface.py"]
        """))

def generate_controller(name):
    """Controladores de pista como el LEU."""
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, 'controller.py'), 'w') as f:
        f.write(f"print('LEU Controller {name} processing signals...')")
    
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM python:3.11-slim
            WORKDIR /app
            COPY . .
            CMD ["python", "controller.py"]
        """))

def generate_network_node(name):
    """Nodos de red (GNSS, FRMCS, GSMR)."""
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, 'node.py'), 'w') as f:
        f.write(f"print('Network Node {name} routing packets...')")
    
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM python:3.11-slim
            WORKDIR /app
            COPY . .
            CMD ["python", "node.py"]
        """))

# ─────────────────────────────────────────────
# T3 — Logic
# ─────────────────────────────────────────────

def generate_microservice(name, database=None):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
    db_host = database if database else f'{name}_db'

    with open(os.path.join(path, 'app.py'), 'w') as f:
        f.write(textwrap.dedent(f"""
            from flask import Flask, jsonify, request
            import mysql.connector
                                
            app = Flask(__name__)
                                
            def get_conn():
                return mysql.connector.connect(
                    host='{db_host}',
                    user='root',
                    password='root',
                    database='{db_host}'
                )
            
            @app.route('/health')
            def health():
                return jsonify(status='ok', service='{name}')
            
            @app.route('/records')
            def get_records():
                conn = get_conn()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM records")
                rows = cursor.fetchall()
                cursor.close()
                conn.close()
                return jsonify(records=rows)
            
            @app.route('/records', methods=['POST'])
            def create_record():
                data = request.json
                conn = get_conn()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO records (name) VALUES (%s)",
                    (data.get('name', 'unknown'),)
                )
                conn.commit()
                cursor.close()
                conn.close()
                return jsonify(status='created'), 201
            
            if __name__ == '__main__':
                app.run(host='0.0.0.0', port=80)
        """))
    
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM python:3.11-slim
            WORKDIR /app
            COPY . .
            RUN pip install flask mysql-connector-python
            CMD ["python", "app.py"]
        """))

def generate_broker(name):
    """Genera configuración para RabbitMQ / MQTT."""
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, 'README.md'), 'w') as f:
        f.write(f"# Message Broker: {name}")

def generate_onboard_unit(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'obu.py'), 'w') as f:
        f.write(textwrap.dedent(f"""
            # Onboard Unit ({name}) — ERTMS T5
            # Simulates the main computing unit aboard the train.

            import time, random

            def read_sensors():
                return {{
                    'speed_kmh': round(random.uniform(0, 300), 1),
                    'position': f'{{random.uniform(40, 55):.4f}}, {{random.uniform(-5, 25):.4f}}'
                }}

            def send_to_ground(data):
                print(f'[OBU {name}] Sending to ground control: {{data}}')

            def receive_command(cmd):
                print(f'[OBU {name}] Command received: {{cmd}}')
                if cmd.get('action') == 'BRAKE':
                    apply_brake(cmd.get('intensity', 1.0))

            def apply_brake(intensity):
                print(f'[OBU {name}] Applying brake at intensity {{intensity}}')

            if __name__ == '__main__':
                while True:
                    data = read_sensors()
                    send_to_ground(data)
                    time.sleep(1)
        """))

def generate_translator(name):
    """Traductores como STM o TIU."""
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
   
    with open(os.path.join(path, 'translator.py'), 'w') as f:
        f.write(f"print('Translator {name} converting protocols...')")
    
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM python:3.11-slim
            WORKDIR /app
            COPY . .
            CMD ["python", "translator.py"]
        """))

def generate_authority_service(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'app.py'), 'w') as f:
        f.write(textwrap.dedent(f"""
        from flask import Flask, jsonify, request
                                
        app = Flask(__name__)
                                
        @app.route('/health')
        def health():
            return jsonify(status='ok', service='{name}')

        @app.route('/authority', methods=['POST'])
        def request_authority():
            data = request.json
            train_id = data.get('train_id')
            corridor = data.get('corridor')
            # Placeholder: real logic would query position-time-ms and routes-ms
            granted = True
            return jsonify(
                train_id=train_id,
                corridor=corridor,
                movement_authority='GRANTED' if granted else 'DENIED'
            )
        
        if __name__ == '__main__':
            app.run(host='0.0.0.0', port=80)
        """))

    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(textwrap.dedent("""
            FROM python:3.11-slim
            WORKDIR /app
            COPY . .
            RUN pip install flask
            CMD ["python", "app.py"]
        """))

# ─────────────────────────────────────────────
# T4 — Data
# ─────────────────────────────────────────────

def generate_database(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, 'init.sql'), 'w') as f:
        f.write(textwrap.dedent(f"""
            CREATE TABLE IF NOT EXISTS records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """))
    
def generate_data_lake(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'README.md'), 'w') as f:
        f.write(textwrap.dedent(f"""
            # {name} — ERTMS Data Lake

            Aggregated operational and historical data lake.

            ## Schemas
            - operational/ : real-time ingestion from position-time-ms
            - historical/ : archived train movement records
            - audit/ : movement authority logs
        """))

    with open(os.path.join(path, 'ingest.py'), 'w') as f:
        f.write(textwrap.dedent(f"""
            # Placeholder ingestion script for the ERTMS Data Lake ({name})
            
            import json, datetime
            
            def ingest(event: dict):
                record = {{
                    'timestamp': datetime.datetime.utcnow().isoformat(),
                    'payload': event
                }}
                print(json.dumps(record))

            if __name__ == '__main__':
                ingest({{'train_id': 'T-001', 'position': '48.8566,2.3522', 'speed_kmh': 220}})
        """))

# ─────────────────────────────────────────────
# T5 — Physical
# ─────────────────────────────────────────────

def generate_control_unit(name):
    """Unidades de control físico (TIMS, TCMS)."""
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, 'control.py'), 'w') as f:
        f.write(f"print('Control Unit {name} managing train bus...')")

def generate_antenna(name):
    """Antenas de comunicación física."""
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, 'antenna.py'), 'w') as f:
        f.write(f"print('Antenna {name} receiving signal...')")

def generate_sensor(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'sensor.py'), 'w') as f:
        f.write(textwrap.dedent(f"""
            # Train Sensor ({name}) — ERTMS T5
            # Simulates speed, position, and physical condition detection.

            import time, random

            def read():
                return {{
                    'speed_kmh': round(random.uniform(0, 300), 1),
                    'position': f'{{random.uniform(40, 55):.4f}}, {{random.uniform(-5, 25):.4f}}',
                    'door_closed': random.choice([True, True, True, False]),
                    'pantograph': 'UP'
                }}
            
            if __name__ == '__main__':
                while True:
                    print(f'[SENSOR {name}]', read())
                    time.sleep(0.5)
        """))

def generate_actuator(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)
    
    with open(os.path.join(path, 'actuator.py'), 'w') as f:
        f.write(textwrap.dedent(f"""
            # Brake Actuator ({name}) — ERTMS T5
            # Receives control commands and acts on the physical train.

            def execute(command):
                action = command.get('action')
                intensity = command.get('intensity', 1.0)
                if action == 'BRAKE':
                    print(f'[ACTUATOR {name}] Emergency brake — intensity {{intensity}}')
                elif action == 'RELEASE':
                    print(f'[ACTUATOR {name}] Brake released')
                else:
                    print(f'[ACTUATOR {name}] Unknown command: {{action}}')
            
            if __name__ == '__main__':
                execute({{'action': 'BRAKE', 'intensity': 0.8}})
        """))

def generate_balise(name):
    path = build_path('skeleton', name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'balise.py'), 'w') as f:
        f.write(textwrap.dedent(f"""
        # Balise ({name}) — ERTMS T5
        # Track-side transponder transmitting position reference data to passing trains.

        BALISE_ID = '{name}'
        POSITION_M = 12500 # metres from reference point

        def transmit():
            return {{
                'balise_id': BALISE_ID,
                'position_m': POSITION_M,
                'track_id': 'CORRIDOR-A',
                'signal': 'EUROBALISE-STM'
            }}
        
        if __name__ == '__main__':
            print('[BALISE]', transmit())
        """))

# ─────────────────────────────────────────────
# docker-compose
# ─────────────────────────────────────────────

TIER_ORDER = {
    'data': 0,
    'physical': 1,
    'logic': 2,
    'communication':3,
    'presentation': 4,
}

DB_IMAGES = {'database', 'data_lake'}

def generate_docker_compose(components, dependencies):
    """Genera un docker-compose.yml válido con indentación de 2 espacios y puertos dinámicos."""
    path = build_path('skeleton')
    os.makedirs(path, exist_ok=True)

    sorted_items = sorted(components.items(), key=lambda kv: TIER_ORDER.get(kv[1][0], 5))
    db_port_offset = 0 # Contador para asignar puertos únicos 

    with open(os.path.join(path, 'docker-compose.yml'), 'w') as f:
        f.write("version: '3.8'\nservices:\n")
        
        for i, (name, (tier, ctype)) in enumerate(sorted_items):
            service_port = 8000 + i # Puerto para servicios web/microservicios (8001, 8002...)
            f.write(f"  {name}:\n") 

            if ctype == 'database':
                host_db_port = 3306 + db_port_offset
                f.write("    image: mysql:8\n") # 4 espacios de indentación
                f.write("    environment:\n")
                f.write("      - MYSQL_ROOT_PASSWORD=root\n")
                f.write(f"      - MYSQL_DATABASE={name}\n")
                f.write("    volumes:\n")
                f.write(f"      - ./{name}/init.sql:/docker-entrypoint-initdb.d/init.sql\n")
                f.write("    ports:\n")
                f.write(f"      - '{host_db_port}:3306'\n")
                db_port_offset += 1

            elif ctype == 'broker':
                f.write("    image: rabbitmq:3-management\n")
                f.write("    ports:\n")
                f.write("      - '5672:5672'\n")
                f.write("      - '15672:15672'\n")

            elif ctype == 'data_lake':
                f.write("    image: python:3.11-slim\n")
                f.write(f"    volumes:\n      - ./{name}:/app\n")
                f.write("    working_dir: /app\n")
                f.write("    command: python ingest.py\n")

            elif ctype in {
                'onboard_unit', 'sensor', 'actuator', 'balise', 
                'translator', 'network_node', 'controller',
                'control_unit', 'antenna'
            }:
                f.write(f"    image: python:3.11-slim\n")
                f.write(f"    volumes:\n      - ./{name}:/app\n")
                f.write(f"    working_dir: /app\n")

                scripts = {
                    'onboard_unit': 'obu.py', 'sensor': 'sensor.py', 'actuator': 'actuator.py', 
                    'balise': 'balise.py', 'translator': 'translator.py', 
                    'network_node': 'node.py', 'controller': 'controller.py',
                    'control_unit': 'control.py', 'antenna': 'antenna.py'
                }
                f.write(f"    command: python {scripts.get(ctype, 'main.py')}\n")

            else: # Web interfaces, microservices, API Gateway etc.
                f.write(f"    build: ./{name}\n")
                f.write(f"    ports:\n      - '{service_port}:80'\n")
                
            my_deps = dependencies.get(name, [])
            if my_deps:
                f.write("    depends_on:\n")
                for dep in my_deps:
                    f.write(f"      - {dep}\n")

            f.write(f"\n") 

        f.write("\nnetworks:\n  default:\n    driver: bridge\n")

# ─────────────────────────────────────────────
# Dispatcher
# ─────────────────────────────────────────────

GENERATORS = {
    'web_interface': generate_web_interface,
    'operator_ui': generate_operator_ui,
    'driver_ui': generate_driver_ui,
    'display': generate_display,
    'api_gateway': generate_api_gateway,
    'interface': generate_interface,
    'controller': generate_controller,
    'network_node': generate_network_node,
    'microservice': generate_microservice,
    'broker': generate_broker,
    'onboard_unit': generate_onboard_unit,
    'translator': generate_translator, 
    'authority_service':generate_authority_service,
    'database': generate_database,
    'data_lake': generate_data_lake,
    'control_unit': generate_control_unit,
    'antenna': generate_antenna,
    'sensor': generate_sensor,
    'actuator': generate_actuator,
    'balise': generate_balise,
}

def apply_transformations(model):
    components = {} # name -> (tier, type)
    dependencies = {} # name -> list of names

    # First pass: collect all components
    for e in model.elements:
        if e.__class__.__name__ == 'Component':
            components[e.name] = (e.tier, e.type)
            dependencies[e.name] = []

    # Second pass: collect dependencies
    for e in model.elements:
        if e.__class__.__name__ == 'Connector':
            source = e.from_.name
            target = e.to_.name
            if target not in dependencies[source]:
                dependencies[source].append(target)

    # Generate skeletons
    for name, (tier, ctype) in components.items():
        gen = GENERATORS.get(ctype)
        if gen:
            if ctype == 'microservice':
                # Buscamos en sus dependencias si alguna es de tipo 'database'
                my_dbs = [d for d in dependencies[name] if components[d][1] == 'database']
                # Pasamos la primera que encuentre (o la lista si soportas varias)
                gen(name, database=my_dbs[0] if my_dbs else None)
            else:
                gen(name)
    
    generate_docker_compose(components, dependencies)
