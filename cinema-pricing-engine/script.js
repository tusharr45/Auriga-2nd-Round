// Simple API/configuration
const prices = {
    silver: 150.00,
    gold: 250.00,
    recliner: 500.00
};

const available = {
    silver: true,
    gold: true,
    recliner: false
};

function money(value) {
    return Number(value).toFixed(2);
}


// Pricing API
function calculatePrice(tier, quantity, member) {

    if (!prices[tier]) {
        throw new Error("Invalid seat tier");
    }

    if (!available[tier]) {
        throw new Error(tier.toUpperCase() + " seats are sold out");
    }

    if (quantity <= 0) {
        throw new Error("Quantity must be greater than 0");
    }

    // 1. Base price
    const base = prices[tier] * quantity;

    // 2. Festival discount
    const festivalDiscount = Math.min(50, base);

    let amount = base - festivalDiscount;

    // 3. Member discount - 10%, maximum ₹100
    let memberDiscount = 0;

    if (member) {
        memberDiscount = Math.min(amount * 0.10, 100);
        amount -= memberDiscount;
    }

    // 4. Convenience fee
    const convenienceFee = quantity * 20;

    // 5. GST
    const taxable = amount + convenienceFee;
    const gst = taxable * 0.18;

    // 6. Final total
    const total = taxable + gst;

    return {
        base,
        festivalDiscount,
        memberDiscount,
        convenienceFee,
        gst,
        total
    };
}


function calculate() {

    const tier = document.getElementById("tier").value;
    const quantity = Number(document.getElementById("quantity").value);
    const member = document.getElementById("member").checked;

    try {

        const result = calculatePrice(tier, quantity, member);

        document.getElementById("bill").innerHTML = `
            <div class="bill-row">
                <span>Tickets</span>
                <span>${quantity}</span>
            </div>

            <div class="bill-row">
                <span>Base Amount</span>
                <span>₹${money(result.base)}</span>
            </div>

            <div class="bill-row">
                <span>Festival Discount</span>
                <span>-₹${money(result.festivalDiscount)}</span>
            </div>

            <div class="bill-row">
                <span>Member Discount</span>
                <span>-₹${money(result.memberDiscount)}</span>
            </div>

            <div class="bill-row">
                <span>Convenience Fee</span>
                <span>₹${money(result.convenienceFee)}</span>
            </div>

            <div class="bill-row">
                <span>GST (18%)</span>
                <span>₹${money(result.gst)}</span>
            </div>

            <div class="bill-row total">
                <span>Final Total</span>
                <span>₹${money(result.total)}</span>
            </div>
        `;

    } catch (error) {

        document.getElementById("bill").innerHTML =
            `<p class="error">${error.message}</p>`;
    }
}


// Import messy price list
function importPrices() {

    const text = document.getElementById("priceInput").value;

    const lines = text.split("\n");

    const cleaned = {};
    const imported = [];
    const duplicates = [];
    const rejected = [];

    lines.forEach(line => {

        if (!line.trim()) return;

        const parts = line.split(",");

        const rawName = parts[0]?.trim();
        const rawPrice = parts.slice(1).join(",").trim();

        if (!rawName || !rawPrice) {
            rejected.push(line + " → blank value");
            return;
        }

        const name = rawName.toLowerCase();

        // Remove currency symbol and commas
        const priceText = rawPrice
            .replace("₹", "")
            .replace(/,/g, "")
            .trim();

        const price = Number(priceText);

        if (isNaN(price) || price <= 0) {
            rejected.push(
                line + " → invalid/negative price"
            );
            return;
        }

        if (cleaned[name]) {
            duplicates.push(
                rawName + " → duplicate"
            );
            return;
        }

        cleaned[name] = price;

        imported.push(
            `${name} → ₹${money(price)}`
        );
    });


    document.getElementById("importResult").innerHTML = `
        <h3>Import Report</h3>

        <b>Imported:</b>
        <p class="success">
            ${imported.join("<br>") || "None"}
        </p>

        <b>Duplicates:</b>
        <p>
            ${duplicates.join("<br>") || "None"}
        </p>

        <b>Rejected:</b>
        <p class="error">
            ${rejected.join("<br>") || "None"}
        </p>
    `;
}