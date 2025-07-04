import time
import os
from datetime import datetime
import pandas as pd
import ta
from binance.client import Client
from dotenv import load_dotenv
import winsound

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
client = Client(api_key, api_secret)

# Configuración
symbol = 'BNBUSDT'
interval = '15m'
limit = 100  
threshold = 15.0  # Porcentaje de cercanía a la MA (15%)
check_interval = 30  # Verificar cada 30 segundos
alert_interval = 60  # Intervalo entre alertas sonoras (1 minuto)
sound_file = 'alterbnb.wav'  # Archivo de sonido para la alerta

# Variables de control
last_alert_time = 0
is_in_range = False

def get_ma99():
    # Obtener datos históricos
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    
    # Convertir a DataFrame
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
                                     'quote_volume', 'trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'])
    
    # Convertir precios a float
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    
    # Calcular MA99
    df['ma99'] = ta.trend.sma_indicator(df['close'], window=99)
    
    return float(df['close'].iloc[-1]), float(df['ma99'].iloc[-1])

def play_alert_sound(position):
    try:
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)
        print(f"🔊(Precio {position} de MA99)")
    except Exception as e:
        print(f"Error al reproducir el sonido: {e}")

def check_price_near_ma():
    global last_alert_time, is_in_range
    current_time = time.time()
    
    try:
        current_price, ma99_value = get_ma99()
        
        # Calcular la diferencia porcentual (sin valor absoluto)
        diff_percentage = ((current_price - ma99_value) / ma99_value) * 100
        
        # Determinar si está por encima o por debajo
        position = "por encima" if diff_percentage > 0 else "por debajo"
        
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        print(f"Precio actual: {current_price:.2f} USDT")
        print(f"MA99: {ma99_value:.2f} USDT")
        print(f"Diferencia: {abs(diff_percentage):.2f}% {position} de MA99")
        print("-" * 50)
        
        # Verificar si está dentro del rango
        if abs(diff_percentage) <= threshold:
            if not is_in_range:
                # Primera vez que entra en el rango
                is_in_range = True
                last_alert_time = current_time
                play_alert_sound(position)
            elif current_time - last_alert_time >= alert_interval:
                # Ya estaba en el rango y ha pasado el tiempo de intervalo
                last_alert_time = current_time
                play_alert_sound(position)
        else:
            # Fuera del rango
            if is_in_range:
                print("📊 Precio fuera del rango de alerta")
                is_in_range = False
            
    except Exception as e:
        print(f"Error: {e}")

print("🔄 Iniciando monitoreo de MA99 para BNB/USDT en timeframe 15m...")
print(f"🔊 Se reproducirá sonido cada minuto mientras el precio esté a {threshold}% o menos de la MA99 (arriba o abajo)")
print(f"⏱️  Actualizando cada {check_interval} segundos")
print("=" * 50)

while True:
    try:
        check_price_near_ma()
        time.sleep(check_interval)
    except Exception as e:
        print(f"Error en el ciclo principal: {e}")
        time.sleep(check_interval) 