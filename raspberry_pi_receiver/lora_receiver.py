#!/usr/bin/env python3
"""
LeakSense LoRa Receiver for Raspberry Pi
Receives sensor data via LoRa and stores in PostgreSQL database
"""

import time
import json
import sys
from datetime import datetime
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from database import Database

# LoRa Configuration
LORA_FREQUENCY = 915  # MHz (must match transmitter)
LORA_SPREADING_FACTOR = 7
LORA_BANDWIDTH = BW.BW125
LORA_CODING_RATE = CODING_RATE.CR4_5
LORA_SYNC_WORD = 0x12

class LoRaReceiver(LoRa):
    """LoRa receiver class for handling incoming packets"""
    
    def __init__(self, db, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.db = db
        self.packet_count = 0
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        
    def start(self):
        """Initialize and start receiving"""
        print("=" * 60)
        print("LeakSense LoRa Receiver Starting...")
        print("=" * 60)
        
        # Configure LoRa parameters
        self.set_freq(LORA_FREQUENCY)
        self.set_spreading_factor(LORA_SPREADING_FACTOR)
        self.set_bw(LORA_BANDWIDTH)
        self.set_coding_rate(LORA_CODING_RATE)
        self.set_sync_word(LORA_SYNC_WORD)
        self.set_rx_crc(True)
        
        print(f"Frequency: {LORA_FREQUENCY} MHz")
        print(f"Spreading Factor: {LORA_SPREADING_FACTOR}")
        print(f"Bandwidth: 125 kHz")
        print(f"Coding Rate: 4/5")
        print("=" * 60)
        print("Listening for packets...\n")
        
        # Start receiving
        self.set_mode(MODE.RXCONT)
        
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n\nShutting down receiver...")
            self.set_mode(MODE.SLEEP)
            BOARD.teardown()
            sys.exit(0)
    
    def on_rx_done(self):
        """Callback when packet is received"""
        print("\n" + "=" * 60)
        print(f"📡 Packet #{self.packet_count} Received")
        print("=" * 60)
        
        # Get payload
        payload = self.read_payload(nocheck=True)
        
        # Convert bytes to string
        try:
            message = bytes(payload).decode('utf-8', errors='ignore')
            print(f"Raw Payload: {message}")
            
            # Parse JSON data
            data = json.loads(message)
            
            # Extract sensor values
            packet_id = data.get('id', 0)
            pressure = data.get('pressure', 0.0)
            moisture = data.get('moisture', 0.0)
            acoustic = data.get('acoustic', 0.0)
            timestamp = datetime.now()
            
            # Get RSSI and SNR
            rssi = self.get_pkt_rssi_value()
            snr = self.get_pkt_snr_value()
            
            print(f"\n📊 Sensor Data:")
            print(f"  Packet ID: {packet_id}")
            print(f"  Pressure:  {pressure:.2f} PSI")
            print(f"  Moisture:  {moisture:.2f} %")
            print(f"  Acoustic:  {acoustic:.2f} dB")
            print(f"  RSSI:      {rssi} dBm")
            print(f"  SNR:       {snr:.2f} dB")
            print(f"  Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Check for alerts
            alerts = []
            if moisture > 70.0:
                alerts.append("⚠️  High moisture level!")
            if acoustic > 75.0:
                alerts.append("⚠️  High acoustic level!")
            if pressure < 20.0 or pressure > 80.0:
                alerts.append("⚠️  Abnormal pressure!")
            
            if alerts:
                print(f"\n🚨 ALERTS:")
                for alert in alerts:
                    print(f"  {alert}")
            
            # Store in database
            try:
                self.db.insert_sensor_data(
                    pressure=pressure,
                    moisture=moisture,
                    acoustic=acoustic,
                    rssi=rssi,
                    snr=snr,
                    timestamp=timestamp
                )
                print(f"\n✅ Data stored in database successfully")
            except Exception as e:
                print(f"\n❌ Database error: {e}")
            
            self.packet_count += 1
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            print(f"Raw data: {payload}")
        except Exception as e:
            print(f"❌ Error processing packet: {e}")
        
        print("=" * 60)
        
        # Reset to receive mode
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)


def main():
    """Main entry point"""
    print("\n🚀 Initializing LeakSense Receiver...\n")
    
    # Initialize board
    BOARD.setup()
    
    # Initialize database
    try:
        db = Database()
        db.connect()
        db.create_tables()
        print("✅ Database connected and initialized\n")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("Please ensure PostgreSQL is running and configured correctly.")
        sys.exit(1)
    
    # Initialize and start LoRa receiver
    try:
        lora = LoRaReceiver(db, verbose=False)
        lora.start()
    except Exception as e:
        print(f"❌ LoRa initialization failed: {e}")
        print("Please check LoRa module connections.")
        BOARD.teardown()
        sys.exit(1)


if __name__ == "__main__":
    main()
