function openUpdateForm(productId) {
    document.getElementById(`updateForm_${productId}`).style.display = "table-row";
}

function closeUpdateForm(productId) {
    document.getElementById(`updateForm_${productId}`).style.display = "none";
}
function deleteProduct(event, productId) {
    event.preventDefault();  // Prevent the default form submission

    const confirmation = confirm("Are you sure you want to delete this product?");
    if (!confirmation) {
        return;
    }

    fetch(`/delete/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'  // Include CSRF token if you have CSRF protection
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        // Optionally update the UI to reflect the deletion
        document.querySelector(`tr[data-product-id="${productId}"]`).remove();
        alert("Product deleted successfully!");
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error deleting product. Please try again.");
    });
}

document.querySelector('form').addEventListener('submit', function (event) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username.trim() === '' || password.trim() === '') {
        event.preventDefault(); // Prevent form submission
        alert('Please fill in both fields.');
    }
});
