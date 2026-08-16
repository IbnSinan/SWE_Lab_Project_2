/*
 * js/bills.js
 * --------------------------------------------------------
 * Module owner : 2203137
 * Feature branch: feature/frontend-module
 * --------------------------------------------------------
 * Talks to the bill CRUD endpoints built by 2203138
 * (/api/bills). Loads the resident dropdown from
 * /api/residents so a bill can only be generated for an
 * existing resident.
 */

async function loadResidentOptions() {
    const residents = await api.get("/api/residents");
    const select = document.getElementById("resident_id");
    select.innerHTML = "";

    if (residents.length === 0) {
        select.innerHTML = '<option value="">No residents registered yet</option>';
        return;
    }

    residents.forEach((r) => {
        const option = document.createElement("option");
        option.value = r.id;
        option.textContent = `${r.name} (${r.holding_number})`;
        select.appendChild(option);
    });
}

function billRow(b) {
    const badgeClass = b.status === "Paid" ? "badge-ok" : "badge-warn";
    const toggleLabel = b.status === "Paid" ? "Mark Unpaid" : "Mark Paid";
    const tr = document.createElement("tr");
    tr.innerHTML = `
        <td>#${b.id}</td>
        <td>${b.resident_name}</td>
        <td>${b.billing_month}</td>
        <td>৳ ${b.amount.toFixed(2)}</td>
        <td>${b.due_date || ""}</td>
        <td><span class="badge ${badgeClass}">${b.status}</span></td>
        <td>
            <button class="link-btn" data-toggle="${b.id}">${toggleLabel}</button>
            <button class="link-btn danger" data-delete="${b.id}">Delete</button>
        </td>
    `;
    return tr;
}

async function loadBills() {
    const bills = await api.get("/api/bills");
    const tbody = document.getElementById("billsBody");
    tbody.innerHTML = "";

    if (bills.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="muted">No bills generated yet.</td></tr>';
        return;
    }

    bills.forEach((b) => tbody.appendChild(billRow(b)));

    tbody.querySelectorAll("[data-toggle]").forEach((btn) => {
        btn.addEventListener("click", async () => {
            await api.patch(`/api/bills/${btn.dataset.toggle}/toggle-status`);
            loadBills();
        });
    });
    tbody.querySelectorAll("[data-delete]").forEach((btn) => {
        btn.addEventListener("click", async () => {
            if (!confirm("Delete this bill?")) return;
            await api.del(`/api/bills/${btn.dataset.delete}`);
            loadBills();
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadResidentOptions();
    loadBills();

    document.getElementById("billForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            resident_id: document.getElementById("resident_id").value,
            billing_month: document.getElementById("billing_month").value.trim(),
            amount: document.getElementById("amount").value,
            due_date: document.getElementById("due_date").value.trim(),
        };

        try {
            await api.post("/api/bills", payload);
            document.getElementById("billForm").reset();
            loadResidentOptions();
            loadBills();
        } catch (err) {
            alert(err.message);
        }
    });
});
