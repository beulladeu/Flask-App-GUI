import os

CFG = {
    'port': '5000',
    'debug': True,
    'secret_key': '12345678',
    'users': {
        'admin': {'password': '120'}
    },
    'mqtt': {
        'host': os.getenv('MQTT_BROKER_HOST', 'localhost'),
        'port': int(os.getenv('MQTT_BROKER_PORT', '20021')),
        'login': os.getenv('MQTT_LOGIN', ''),
        'password': os.getenv('MQTT_PSWD', '')
    }
}

print(CFG)
