console.log("main.js loaded and running");

document.addEventListener('DOMContentLoaded', () => {

// add products
 
    const productInput = document.getElementById('product-Input');      
    const addProductBtn = document.getElementById('add-Product-Btn');
    const viewProductBtn = document.getElementById('view-Product-Btn');

    if (addProductBtn && productInput) {
        addProductBtn.addEventListener('click', function() {
            const newProductName = productInput.value;
            console.log("Product to add:", newProductName);  // for debugging

            fetch('add_new_product', {                      // request (sending data to backend)
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({"product_name": newProductName})
            })

            .then(response => {
                return response.json();

            })
            .then(data => {
                if (data.status && data.status.includes("added successfully")) {
                    const alertBox = document.getElementById('productAlert');
                    alertBox.style.display = 'block';   
                    setTimeout(() => {
                        alertBox.style.display = 'none'; 
                    }, 3000);

                    productInput.value = ''; 
                } else {
                    alert("Error: " + (data.status || "unknown error"));
                }
            })
            .catch(error => {
                console.error("error:", error);
            }) 
        });
    }

// add locations

    const locationInput = document.getElementById('location-Input');
    const addLocationBtn = document.getElementById('add-Location-Btn');
    const viewLocationBtn = document.getElementById('view-Location-Btn');

    if (addLocationBtn && locationInput) {
        addLocationBtn.addEventListener('click', function() {
            const newLocationName = locationInput.value;
            console.log("Location to add:", newLocationName);

            fetch('add_new_location', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({"location_name": newLocationName})
            })

            .then(response => {
                return response.json();

            })
            .then(data => {
                if (data.status && data.status.includes("successfully added")) {
                    const alertBox = document.getElementById('locationAlert');
                    alertBox.style.display = 'block';
                    setTimeout(() => {
                        alertBox.style.display = 'none';
                    }, 3000);

                    locationInput.value = '';
                } else {
                    alert("Error: " + (data.status || "unknow error"));
                }
            })
            .catch(error => {
                console.error("error:", error);
            })
        });
    }

// product edit button

    const editButtons = document.querySelectorAll('.edit-btn');

     
    editButtons.forEach(button => {
        button.addEventListener('click', () => {
        
            const productId = button.getAttribute('data-product-id');
            const currentName = button.getAttribute('data-product-name');

            const newName = prompt("Edit Product Name:", currentName);

            if (newName && newName !== currentName) {
                fetch('/product_name_edit', {
                    method: 'PATCH',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ product_id: productId, product_name: newName})
                })
                .then(response => response.json())
                .then(data => {

                    if (data.message) {
                        button.closest('tr').children[1].textContent =data.updated_name;
                        alert(data.message);
                    }
                })
                .catch(err => console.error(err));
            }
        });
    });
});


// locations edit button

    const locationEditButtons = document.querySelectorAll('.edit-location-btn');

    if (locationEditButtons.length > 0) {
        locationEditButtons.forEach(button => {
            button.addEventListener('click', () => {

                const locationId = button.getAttribute('data-location-id');
                const currentName = button.getAttribute('data-location-name');

                const newName = prompt("Edit Location Name:", currentName);

                if (newName && newName !== currentName) {
                    fetch('/location_name_edit', {
                        method: 'PATCH',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ location_id: locationId, location_name: newName})
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message) {
                            button.closest('tr').children[1].textContent = data.location_name;
                            alert(data.message);
                        }
                    })
                    .catch(err => console.error(err))
                }
            });
        });
    }


// update from_location drop_down
    
    const fromLocationDropdown = document.getElementById('fromLocation');

    if (fromLocationDropdown) {
        fetch('/get_locations')
            .then(response => response.json())
            .then(data => {
                fromLocationDropdown.innerHTML = '<option value="placeholder" disabled selected>From Location</option><option value="">None</option>';
                data.locations.forEach(loc => {
                    const option = document.createElement('option');
                    option.value = loc.location_id;
                    option.textContent = loc.location_name;
                    fromLocationDropdown.appendChild(option);
                });
            })
            .catch(err => console.error(err));

        fromLocationDropdown.addEventListener('change', () => {
            const selectedLocation = fromLocationDropdown.value;
            let fromLocationValue;

            if (selectedLocation === "") {
                fromLocationValue = null;
            } else {
                fromLocationValue = selectedLocation;
            }

            console.log("From Location to use in movement:", fromLocationValue);
        });
    }


// update to_location drop_down

    const toLocationDropdown = document.getElementById('toLocation');

    if (toLocationDropdown) {
        fetch('/get_locations')
            .then(response => response.json())
            .then(data => {
                toLocationDropdown.innerHTML = '<option value="placeholder" disabled selected>To Location</option><option value="">None</option>';
                data.locations.forEach(loc => {
                    const option = document.createElement('option');
                    option.value = loc.location_id;
                    option.textContent = loc.location_name;
                    toLocationDropdown.appendChild(option);
                });
            })
            .catch(err => console.error(err));

        toLocationDropdown.addEventListener('change', () => {
            const selectedLocation = toLocationDropdown.value;
            let toLocationValue;

            if (selectedLocation === "") {
                toLocationValue = null;
            } else {
                toLocationValue = selectedLocation;
            }

            console.log("To Location to use in movement:", toLocationValue);
        });
    }

// update product drop_down

    const productDropdown = document.getElementById('productSelect');

    if (productDropdown) {
        
        fetch('/get_products')
            .then(response => response.json())
            .then(data => {
                productDropdown.innerHTML = '<option value="" disabled selected>Select Product</option><option value="">None</option>';
                data.products.forEach(prod => {
                    const option = document.createElement('option');
                    option.value = prod.product_id;
                    option.textContent = prod.product_name;
                    productDropdown.appendChild(option);
                });
            })
            
            .catch(err => console.error(err));

        productDropdown.addEventListener('change', () => {
            const selectedProduct = productDropdown.value;
            let productValue = selectedProduct === "" ? null : selectedProduct;
            console.log("Selected Product:", productValue);
        });
    }


// product movement

    document.getElementById('makeMovementBtn').addEventListener('click', function() {
        const fromLocation = document.getElementById('fromLocation').value || null;
        const toLocation = document.getElementById('toLocation').value || null;
        const product = document.getElementById('productSelect').value;
        const qty = document.getElementById('movementQty').value;

        if (!product || !qty) {
            alert("Select product and enter quantity");
            return;
        }

        const data = {
            from_location: fromLocation,
            to_location: toLocation,
            product: product,
            qty: parseInt(qty)
        };

        fetch('/add_product_movement', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })

        .then(response => response.json())
        .then(result => {
            if (result.status && result.status === "success") {
                const alertBox = document.getElementById('movementAlert');
                alertBox.style.display = 'block'; 
                setTimeout(() => {
                    alertBox.style.display = 'none'; 
                }, 3000);

                document.getElementById('fromLocation').value = '';
                document.getElementById('toLocation').value = '';
                document.getElementById('productSelect').value = '';
                document.getElementById('movementQty').value = '';
            } else {
                alert(result.message || "Unknown error");
            }
        })
        .catch(err => alert("Error: " + err));
    });

    function loadStock() {
    fetch('/get_stock')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('stockTableBody');
            tbody.innerHTML = ''; 
            data.stock.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${item.product_name}</td>
                    <td>${item.location_name}</td>
                    <td>${item.qty}</td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(err => console.error("Error loading stock:", err));
}


loadStock();


document.getElementById('makeMovementBtn').addEventListener('click', function() {
    
    fetch('/add_product_movement', {
        
    }).then(response => response.json())
      .then(result => {
          alert(result.status || result.message);
          loadStock();
      });
});


