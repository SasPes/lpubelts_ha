# LPU Belts HA

![SasPes](ss/ss2.png)

A Home Assistant integration for displaying LPU Belts leaderboard data.

## Features

- Fetches and displays user metrics from the LPU Belts leaderboard.
- Provides sensors for dan level, points, black belt count, and more.
- Diagnostic sensors for API connectivity and last update time.

## Installation

1. Copy the `lpubelts_ha` directory to your Home Assistant `custom_components` folder.
2. Restart Home Assistant.

## Configuration

1. Go to **Settings** > **Devices & Services** > **Add Integration**.
2. Search for **LPU Belts HA**.
3. Enter your LPU Belts display name.

## Sensors

- Display name
- Dan level
- Dan points
- Black belt count
- Black belt awarded at

## Diagnostic

- API connectivity status
- Last updated time