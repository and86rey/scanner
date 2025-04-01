import json
from datetime import datetime

# Read flight offers from JSON
with open("flight_offers.json", "r") as f:
    offers = json.load(f)

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
        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {background-color: #f9f9f9;}
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
for offer in offers:
    # Parse times (strip 'Z' and seconds for simplicity)
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
