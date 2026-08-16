/*
 * js/dashboard.js
 * --------------------------------------------------------
 * Module owner : 2203137
 * Feature branch: feature/frontend-module
 * --------------------------------------------------------
 * Fetches /api/dashboard/summary (built by 2203138) and
 * renders the stat cards and recent-bills table.
 */

function renderStats(stats) {
    document.getElementById("statResidents").textContent = stats.total_residents;
    document.getElementById("statBills").textContent = stats.total_bills;
    document.getElementById("statUnpaid").textContent = stats.unpaid_count;
    document.getElementById("statPaid").textContent = stats.paid_count;
    document.getElementById("statDue").textContent = "৳ " + stats.total_due.toFixed(2);
    document.getElementById("statCollected").textContent = "৳ " + stats.total_collected.toFixed(2);
}

function renderRecentBills(bills) {
    const tbody = document.getElementById("recentBillsBody");
    tbody.innerHTML = "";

    if (bills.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="muted">No bills generated yet.</td></tr>';
        return;
    }

    bills.forEach((b) => {
        const badgeClass = b.status === "Paid" ? "badge-ok" : "badge-warn";
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>#${b.id}</td>
            <td>${b.resident_name}</td>
            <td>${b.billing_month}</td>
            <td>৳ ${b.amount.toFixed(2)}</td>
            <td><span class="badge ${badgeClass}">${b.status}</span></td>
        `;
        tbody.appendChild(row);
    });
}

async function loadDashboard() {
    try {
        const summary = await api.get("/api/dashboard/summary");
        renderStats(summary);
        renderRecentBills(summary.recent_bills);
    } catch (err) {
        console.error(err);
    }
}

document.addEventListener("DOMContentLoaded", loadDashboard);
