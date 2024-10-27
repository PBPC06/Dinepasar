// edit_modal.js

async function openEditModal(foodId) {
    const modal = document.getElementById('editModal');
    modal.classList.remove('hidden');

    try {
        const response = await fetch(`/food/${foodId}/edit/`); // Endpoint to get food data
        const result = await response.json();
        console.log(result); // Debugging log

        if (response.ok) {
            // Populate the modal form with data
            document.getElementById('gambar').value = result.food.gambar;
            document.getElementById('nama_makanan').value = result.food.nama_makanan;
            document.getElementById('restoran').value = result.food.restoran;
            document.getElementById('kategori').value = result.food.kategori;
            document.getElementById('harga').value = result.food.harga;
            document.getElementById('rating').value = result.food.rating;
            document.getElementById('deskripsi').value = result.food.deskripsi;

            // Store foodId in the form for submission
            document.getElementById('editFoodForm').dataset.foodId = foodId; 
        } else {
            alert('Failed to retrieve food data.');
        }
    } catch (error) {
        console.error("Error loading data:", error);
    }
}


document.getElementById('editFoodForm').onsubmit = async function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const foodId = this.dataset.foodId; // Use dataset to store foodId

    try {
        const response = await fetch(`/food/${foodId}/edit/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Fetch CSRF token dynamically
                'X-Requested-With': 'XMLHttpRequest',
            },
        });

        const data = await response.json();
        if (data.success) {
            // Optionally refresh the food cards here or update the UI
            closeModal(); // Close modal after success
        } else {
            const responseMessage = document.getElementById('responseMessage');
            responseMessage.innerHTML = ''; // Clear previous messages

            // Display error messages if any
            for (const [field, errors] of Object.entries(data.errors)) {
                errors.forEach(error => {
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'text-red-500'; // Style your error message
                    errorMessage.innerText = `${field}: ${error}`;
                    responseMessage.appendChild(errorMessage);
                });
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

function closeModal() {
    document.getElementById('editModal').classList.add('hidden');
}

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}