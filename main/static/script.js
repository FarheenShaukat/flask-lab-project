// Health Check Button
document
  .getElementById("healthBtn")
  .addEventListener("click", async function () {
    const resultDiv = document.getElementById("healthResult");
    resultDiv.classList.remove("hidden", "error", "success");
    resultDiv.innerHTML = "<p>Loading...</p>";

    try {
      const response = await fetch("/health");
      const data = await response.json();

      if (response.ok) {
        resultDiv.classList.add("success");
        resultDiv.innerHTML = `
                <strong>✓ Status: ${data.status}</strong><br>
                Message: ${data.message}
            `;
      } else {
        resultDiv.classList.add("error");
        resultDiv.innerHTML = `<strong>✗ Error:</strong> ${data.message}`;
      }
    } catch (error) {
      resultDiv.classList.add("error");
      resultDiv.innerHTML = `<strong>✗ Error:</strong> ${error.message}`;
    }
  });

// Form Submission
document
  .getElementById("dataForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      message: document.getElementById("message").value,
    };

    const resultDiv = document.getElementById("postResult");
    resultDiv.classList.remove("hidden", "error", "success");
    resultDiv.innerHTML = "<p>Submitting...</p>";

    try {
      const response = await fetch("/data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        resultDiv.classList.add("success");
        resultDiv.innerHTML = `
                <strong>✓ ${data.message}</strong><br>
                Total items stored: ${data.total_items}
            `;
        // Reset form
        document.getElementById("dataForm").reset();
      } else {
        resultDiv.classList.add("error");
        resultDiv.innerHTML = `<strong>✗ Error:</strong> ${data.message}`;
      }
    } catch (error) {
      resultDiv.classList.add("error");
      resultDiv.innerHTML = `<strong>✗ Error:</strong> ${error.message}`;
    }
  });

// Get Data Button
document
  .getElementById("getDataBtn")
  .addEventListener("click", async function () {
    const dataTable = document.getElementById("dataTable");
    const tableBody = document.getElementById("tableBody");
    const noData = document.getElementById("noData");

    dataTable.classList.add("hidden");
    noData.classList.add("hidden");

    try {
      const response = await fetch("/data");
      const data = await response.json();

      if (response.ok && data.data.length > 0) {
        tableBody.innerHTML = "";
        data.data.forEach((item, index) => {
          const row = document.createElement("tr");
          row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${item.name}</td>
                    <td>${item.email}</td>
                    <td>${item.message}</td>
                `;
          tableBody.appendChild(row);
        });
        dataTable.classList.remove("hidden");
      } else {
        noData.classList.remove("hidden");
      }
    } catch (error) {
      noData.innerHTML = `<strong>Error loading data:</strong> ${error.message}`;
      noData.classList.remove("hidden");
    }
  });
