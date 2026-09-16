The solution was intentionally kept simple so that the pricing logic is easy to understand, test and modify.
The application has three main parts:
1. User interface
2. Pricing calculation
3. Price-list importer
## Pricing
The pricing calculation is performed in a fixed sequence.
First, the ticket price is multiplied by the number of tickets.
Next, the festival discount is applied.
If the customer is a member, the member percentage discount is calculated. The member discount is capped at the configured maximum.
After discounts, the convenience fee is added per ticket.
GST is then calculated on the resulting taxable amount.
Finally, the total is displayed with two decimal places.
## Validation
The system checks:
- Valid seat tier
- Seat availability
- Positive ticket quantity
- Valid price values
Sold-out tiers cannot be booked.
## Money
The implementation rounds displayed monetary values to two decimal places to represent paisa-level amounts consistently.
For a larger production system, monetary calculations could be moved to a backend service using decimal-based calculations throughout.
## Price Import
The importer handles messy input by:
- Removing extra spaces
- Converting tier names to lowercase
- Removing the rupee symbol
- Removing comma separators from prices
- Converting prices into numbers
- Rejecting blank values
- Rejecting invalid prices
- Rejecting negative or zero prices
- Detecting duplicate tier names
For example, `Silver`, `silver`, and ` SILVER ` are treated as the same tier.
The importer reports imported records, duplicates and rejected records separately.
## Design Choice
A lightweight HTML/CSS/JavaScript implementation was selected because the core challenge is business-rule correctness rather than framework complexity.
The pricing calculation is kept in a separate JavaScript function so it can later be moved behind a REST API without changing the main pricing rules.