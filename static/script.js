// Function to open the update form
function openUpdateForm(productId) {
    document.getElementById(`updateForm_${productId}`).style.display = "table-row";
}

// Function to close the update form
function closeUpdateForm(productId) {
    document.getElementById(`updateForm_${productId}`).style.display = "none";
}

// Function to handle product deletion
function deleteProduct(event, productId) {
    event.preventDefault();  // Prevent the default form submission

    const confirmation = confirm("Are you sure you want to delete this product?");
    if (!confirmation) {
        return; // User canceled, do nothing
    }

    fetch(`/delete/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'  // Ensure CSRF token is passed
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();  // Response is assumed to be plain text
    })
    .then(data => {
        // Remove the deleted product row from the table
        document.querySelector(`tr[data-product-id="${productId}"]`).remove();
        alert("Product deleted successfully!");
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error deleting product. Please try again.");
    });
}

// Search functionality to filter product rows based on search input
document.getElementById('search-bar').addEventListener('input', function () {
    const filter = this.value.toLowerCase().trim();
    const rows = document.querySelectorAll('.product-row');
    const noResultsBox = document.getElementById('no-results-search-box'); // Ensure this element exists
    const productTable = document.querySelector('.product-table');
    let visibleProductCount = 0;

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const searchableText = Array.from(cells)
            .slice(1, -1) // Exclude ID and Actions columns
            .map(cell => cell.textContent.toLowerCase())
            .join(' ');

        if (searchableText.includes(filter)) {
            row.style.display = ''; // Show matching rows
            visibleProductCount++;
        } else {
            row.style.display = 'none'; // Hide non-matching rows
        }
    });

    if (visibleProductCount === 0) {
        // Show no results box
        noResultsBox.style.display = 'block';
        noResultsBox.textContent = filter ? `No products found matching "${filter}"` : 'No products found.';
        console.log(noResultsBox)
        if (productTable) {
            productTable.style.display = 'none'; // Hide table if no results
        }
    } else {
        noResultsBox.style.display = 'none'; // Hide no results box if there are results
        if (productTable) {
            productTable.style.display = 'table'; // Show table if there are results
        }
    }
});

// Form validation example (use wherever form submission needs validation)
document.querySelector('form').addEventListener('submit', function (event) {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!username || !password) {
        event.preventDefault();  // Prevent form submission if fields are empty
        alert('Please fill in both fields.');
    }
});
