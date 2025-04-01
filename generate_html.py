import json
from datetime import datetime

# Read flight offers from JSON
try:
    with open("flight_offers.json", "r") as f:
        offers = json.load(f)
except FileNotFoundError:
    offers = []  # Fallback if no data yet

# Sort by price (lowest to highest)
offers.sort(key=lambda x: x["price"])

# Generate HTML
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cheap Flights from BER</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        table {
            width: 90%;
            margin: 20px auto;
            border-collapse: collapse;
            background-color: #fff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
    </style>
</head>
<body>
    <h1>Cheap Flights from Berlin (BER)</h1>
    <table>
        <tr>
            <th>Date</th>
            <th>Departure Time (BER)</th>
            <th>Destination Airport</th>
            <th>Return Time</th>
            <th>Price (€)</th>
        </tr>
"""

# Add rows to table
if not offers:
    html += "<tr><td colspan='5' style='text-align:center;'>No flights found yet</td></tr>"
else:
    for offer in offers:
        # Parse times (strip seconds and 'Z' for readability)
        out_time = datetime.strptime(offer["outbound_departure"], "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M")
        in_time = datetime.strptime(offer["inbound_departure"], "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M")
        
        html += f"""
            <tr>
                <td>{offer["date"]}</td>
                <td>{out_time}</td>
                <td>{offer["destination"]}</td>
                <td>{in_time}</td>
                <td>{offer["price"]}</td>
            </tr>
        """

html += """
    </table>
</body>
</html>
"""

# Write to index.html
with open("index.html", "w") as f:
    f.write(html)
print("HTML table generated in index.html")
