/*
 * js/residents.js
 * --------------------------------------------------------
 * Module owner : 2203137
 * Feature branch: feature/frontend-module
 * --------------------------------------------------------
 * Talks to the resident CRUD endpoints built by 2203138
 * (/api/residents). The same form is reused for both create
 * and edit - clicking "Edit" loads the resident into the form
 * and switches it into update mode.
 */

let editingResidentId = null;

function residentRow(r) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
        <td>${r.holding_number}</td>
        <td>${r.name}</td>
        <td>${r.address}</td>
        <td>${r.phone || ""}</td>
        <td>${r.category}</td>
        <td>
            <button class="link-btn" data-edit="${r.id}">Edit</button>
            <button class="link-btn danger" data-delete="${r.id}">Delete</button>
        </td>
    `;
    return tr;
}

async function loadResidents() {
    const residents = await api.get("/api/residents");
    const tbody = document.getElementById("residentsBody");
    tbody.innerHTML = "";

    if (residents.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="muted">No residents registered yet.</td></tr>';
        return;
    }

    residents.forEach((r) => tbody.appendChild(residentRow(r)));

    tbody.querySelectorAll("[data-edit]").forEach((btn) => {
        btn.addEventListener("click", () => startEdit(btn.dataset.edit, residents));
    });
    tbody.querySelectorAll("[data-delete]").forEach((btn) => {
        btn.addEventListener("click", () => deleteResident(btn.dataset.delete));
    });
}

function startEdit(id, residents) {
    const resident = residents.find((r) => String(r.id) === String(id));
    if (!resident) return;

    editingResidentId = resident.id;
    document.getElementById("formTitle").textContent = "Edit Resident";
    document.getElementById("name").value = resident.name;
    document.getElementById("holding_number").value = resident.holding_number;
    document.getElementById("address").value = resident.address;
    document.getElementById("phone").value = resident.phone || "";
    document.getElementById("category").value = resident.category;
    document.getElementById("cancelEdit").style.display = "inline-block";
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function resetForm() {
    editingResidentId = null;
    document.getElementById("formTitle").textContent = "Register New Resident";
    document.getElementById("residentForm").reset();
    document.getElementById("cancelEdit").style.display = "none";
}

async function deleteResident(id) {
    if (!confirm("Delete this resident?")) return;
    try {
        await api.del(`/api/residents/${id}`);
        loadResidents();
    } catch (err) {
        alert(err.message);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadResidents();

    document.getElementById("residentForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            name: document.getElementById("name").value.trim(),
            holding_number: document.getElementById("holding_number").value.trim(),
            address: document.getElementById("address").value.trim(),
            phone: document.getElementById("phone").value.trim(),
            category: document.getElementById("category").value,
        };

        try {
            if (editingResidentId) {
                await api.put(`/api/residents/${editingResidentId}`, payload);
            } else {
                await api.post("/api/residents", payload);
            }
            resetForm();
            loadResidents();
        } catch (err) {
            alert(err.message);
        }
    });

    document.getElementById("cancelEdit").addEventListener("click", resetForm);
});
