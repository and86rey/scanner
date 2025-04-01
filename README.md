# Flight Bot - Cheap Flights from Berlin (BER)

This bot finds cheap, direct, same-day return flights from Berlin (BER) to any EU airport, costing less than €100, with a minimum 5-hour gap between arrival and return departure. Results are updated weekly and displayed in a price-sorted table at [and86rey.github.io/flight-bot](https://and86rey.github.io/flight-bot).

## Features
- **Origin**: Berlin (BER) only.
- **Destinations**: All EU airports (loaded from `eu_airports.json`).
- **Conditions**: Direct flights, same-day outbound/inbound, <€100, 5+ hour gap.
- **Search**: Checks tomorrow to 6 months ahead.
- **Output**: HTML table (Date, Departure Time, Destination, Return Time, Price).

## Setup
1. **Clone Repo**: `git clone https://github.com/and86rey/flight-bot.git`
2. **API Key**: 
   - Get a free key from [RapidAPI Skyscanner API](https://rapidapi.com/skyscanner/api/skyscanner-flight-search).
   - Add to GitHub Secrets: `Settings` > `Secrets and variables` > `Actions` > New secret: `RAPIDAPI_KEY`.
3. **GitHub Pages**:
   - Enable: `Settings` > `Pages` > Source: `main`, Folder: `/root` > Save.
   - View results: [and86rey.github.io/flight-bot](https://and86rey.github.io/flight-bot).
4. **Run Workflow**: 
   - Manual: `Actions` > “Check Cheap Flights” > “Run workflow.”
   - Scheduled: Runs every Monday, 8:00 UTC.

## Files
- **`flight_bot.py`**: Queries Skyscanner API, saves to `flight_offers.json`.
- **`eu_airports.json`**: Full list of EU IATA airport codes.
- **`flight-bot.yml`**: GitHub Actions workflow to run bot and generate HTML.
- **`generate_html.py`**: Creates `index.html` with sorted flight table.
- **`index.html`**: Live results (auto-generated).

## Notes
- **Times**: Mocked (8 AM outbound, 3 PM return) due to `browseroutes` API limits—real times need `live-prices/v1`.
- **API Limits**: Free tier (~100-500 calls/month)—weekly runs stay within bounds.

## Next Steps
- Replace mock times with real schedules.
- Add email alerts for deals under €50.

Contributions welcome—fork and PR!
