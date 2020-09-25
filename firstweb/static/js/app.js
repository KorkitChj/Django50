$(document).ready(function () {

    /* Set rates + misc */
    var taxRate = 0.05;
    var shippingRate = 15.00;
    var fadeTime = 300;
    var subtotal = 0;

    $('.product').each(function () {
        subtotal += parseFloat($(this).children('.product-line-price').text());
    });
    //$('#cart-subtotal').html(subtotal);
    var tax = subtotal * taxRate;
    var shipping = (subtotal > 0 ? shippingRate : 0);
    var total = subtotal + tax + shipping;
    $('#cart-tax').html(tax);
    $('#cart-shipping').html(shipping);
    $('#cart-total').html(total);

    /* Assign actions */
    $('.product-quantity input').change(function () {
        updateQuantity(this);
    });

    // $('.product-removal button').click(function () {
    //     removeItem(this);
    // });


    /* Recalculate cart */
    function recalculateCart() {
        var subtotal = 0;

        /* Sum up row totals */
        $('.product').each(function () {
            subtotal += parseFloat($(this).children('.product-line-price').text());
        });

        /* Calculate totals */
        var tax = subtotal * taxRate;
        var shipping = (subtotal > 0 ? shippingRate : 0);
        var total = subtotal + tax + shipping;

        /* Update totals display */
        $('.totals-value').fadeOut(fadeTime, function () {
            //$('#cart-subtotal').html(subtotal);
            $('#cart-tax').html(tax);
            $('#cart-shipping').html(shipping);
            $('#cart-total').html(total);
            if (total == 0) {
                $('.checkout').fadeOut(fadeTime);
            } else {
                $('.checkout').fadeIn(fadeTime);
            }
            $('.totals-value').fadeIn(fadeTime);
        });
    }


    /* Update quantity */
    function updateQuantity(quantityInput) {
        /* Calculate line price */
        var productRow = $(quantityInput).parent().parent();
        var price = parseFloat(productRow.children('.product-price').text());
        var quantity = $(quantityInput).val();
        var linePrice = price * quantity;

        /* Update line price display and recalc cart totals */
        productRow.children('.product-line-price').each(function () {
            $(this).fadeOut(fadeTime, function () {
                $(this).text(linePrice);
                recalculateCart();
                $(this).fadeIn(fadeTime);
            });
        });
    }


    /* Remove item from cart */
    // function removeItem(removeButton) {
    //     var productRow = $(removeButton).parent().parent();
    //     productRow.slideUp(fadeTime, function () {
    //         productRow.remove();
    //         recalculateCart();
    //     });
    // }

});