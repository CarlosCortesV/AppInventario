function fetchProductDetails() {
    const productId = document.getElementById("product_id").value;
    if (!productId) {
        alert("Ingrese un ID de producto.");
        return;
    }

    fetch(`http://127.0.0.1:5000/product/${productId}`) // Cambia el puerto si es necesario
        .then((response) => {
            if (!response.ok) {
                throw new Error("Producto no encontrado");
            }
            return response.json();
        })
        .then((product) => {
            // Rellenar los campos del formulario con los datos del producto
            document.getElementById("name").value = product.name || "";
            document.getElementById("category").value = product.category || "";
            document.getElementById("quantity").value = product.quantity || "";
            document.getElementById("price").value = product.price || "";
        })
        .catch((error) => {
            alert(error.message);
        });
}

function deleteProduct() {
    const productId = document.getElementById("product_id").value;
    if (!productId) {
        alert("Ingrese un ID de producto.");
        return;
    }

    fetch(`/delete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: parseInt(productId) }), // Asegúrate de enviar un número
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("No se pudo eliminar el producto.");
            }
            return response.json();
        })
        .then((data) => {
            alert(data.message || "Producto eliminado exitosamente.");
            document.getElementById("product-details").innerHTML = "";
        })
        .catch((error) => {
            console.error("Error al eliminar el producto:", error);
            alert("Error al eliminar el producto: " + error.message);
        });
}
document.getElementById("confirmDelete").addEventListener("click", function () {
    const productId = document.getElementById("product_id").value;
    if (!productId) {
        alert("Ingrese un ID de producto.");
        return;
    }

    fetch(`/delete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: productId }),
    })
        .then((response) => response.json())
        .then((data) => {
            alert(data.message || "Producto eliminado exitosamente.");
            location.reload();
        })
        .catch((error) => {
            alert("Error al eliminar el producto: " + error.message);
        });
});