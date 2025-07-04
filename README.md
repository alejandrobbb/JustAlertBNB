# BNB/USDT MA99 Monitor

A script that monitors the BNB/USDT price in relation to its 99-period Moving Average on a 15-minute timeframe.

## Features

- Monitors BNB/USDT pair every 30 seconds
- Calculates the 99-period Simple Moving Average (MA99) on 15-minute timeframe
- Displays current price, MA99 value, and percentage difference
- Indicates whether the price is above or below MA99
- Plays a sound alert when price is within 15% of MA99
- Alert repeats every minute while price remains in range

## Requirements

- Python 3.x
- `.env` file with Binance credentials:
  ```
  API_KEY=your_api_key
  API_SECRET=your_api_secret
  ```
- Sound file `alterbnb.wav` in the same directory
- Required libraries:
  ```
  python-binance
  pandas
  ta
  python-dotenv
  ```

## Usage

1. Make sure you have the `.env` file with your credentials
2. Place the `alterbnb.wav` file in the same directory
3. Run the script:
   ```
   python MA99Alert.py
   ``` 
