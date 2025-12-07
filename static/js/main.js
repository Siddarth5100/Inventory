// add products
 
const productInput = document.getElementById('product-Input');      
const addProductBtn = document.getElementById('add-Product-Btn');
const viewProductBtn = document.getElementById('view-Product-Btn');

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

    })

    .catch(error => {
        console.error("error:", error);
    })
});


// add locations

const locationInput = document.getElementById('location-Input');
const addLocationBtn = document.getElementById('add-Location-Btn');
const viewLocationBtn = document.getElementById('view-Location-Btn');

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

    })

    .catch(error => {
        console.error("error:", error);
    })
});

