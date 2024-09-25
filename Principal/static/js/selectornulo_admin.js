document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todos los dropdowns con valor nulo al cargar la página
    document.querySelectorAll('.category_product, .category_product1, .category_product2, .category_product3').forEach(function(select) {
        select.value = '';  // Establece el valor nulo en todos los dropdowns
    });

    // Permitir la selección en cada dropdown sin reiniciar los otros
    document.querySelectorAll('.category_product, .category_product1, .category_product2, .category_product3').forEach(function(select) {
        select.addEventListener('change', function() {
            // Aquí puedes agregar lógica si necesitas hacer algo con el cambio de selección
        });
    });
});
