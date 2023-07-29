(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:3
            },
            768:{
                items:4
            },
            992:{
                items:5
            },
            1200:{
                items:6
            }
        }
    });


    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:4
            }
        }
    });


    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });
    
})(jQuery);

$("#category-search").keyup(function(){
    var value = $("#category-search").val();

    if (!value){
        value = "_empty_"
    }
    const categoryDataBox = document.getElementById("category-list")
    $.ajax({
        type: 'GET',
        url: `/category/${value}`,
        success: function(response){
            categoryDataBox.innerHTML = ""
            const categories = response.data
            categories.map(item=>{
                const category = document.createElement('a')
                category.textContent = item.name
                category.setAttribute('href', `/products/category=${item.slug}`)
                category.setAttribute('class', "nav-item nav-link")
                categoryDataBox.appendChild(category)
            });
        },
        error: function(error){
            console.log(error)
        }
    })
});

$(document).on('submit', '#review-to-product-form', function(e){
    e.preventDefault()

    $.ajax({
        type: 'POST',
        url: 'review/to-product',
        data:{
            current_product_slug: $('#current-product-slug').val(),
            review_to_product: $('#review-to-product-input').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response){
            alert('Yorumunuz incelendikten sonra yayına alınacaktır.')
        },
        error: function(error) {
            alert("basarisiz")
        }
    })
})

$(document).on('submit', '#review-to-seller-form', function(e){
    e.preventDefault()

    $.ajax({
        type: 'POST',
        url: 'review/to-seller',
        data:{
            current_seller_slug: $('#current-seller-slug').val(),
            review_to_seller: $('#review-to-seller-input').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response){
            alert('Yorumunuz incelendikten sonra yayına alınacaktır.')
        },
        error: function(error) {
            alert("basarisiz")
        }
    })
})


function yourFunction() {
    if (document.getElementById("search_product_company").value != ''){
        var _value = document.getElementById("search_product_company").value;
        var action_src = "/products/search/search-word=" + _value

        var your_form = document.getElementById('search_product_company_form');
        your_form.action = action_src ;
    } 
}

function deleteFilter(a){

    if (a == 'location'){
        $("#city-input").val(null).trigger('change');
        $("#district-input").val(null).trigger('change');
    }
    else if (a == 'searchby_word')
    document.getElementById('searchby_word').value = null

    document.getElementById('filter-submit').click()
}


$("#filter-form").submit(function() {
    $(this).find(":input").filter(function(){ return !this.value; }).attr("disabled", "disabled");
    return true; // ensure form still submits
});

$('#add-favorites').on('click', function(){
    prod_name = $(this).attr('name')
    $.ajax({
        url: `/products/add-favorites/${prod_name}`,
        type: 'GET',
        success: function(response){
            if (response.success){   
                $('#add-favorites').css('display', 'none')
                $('#discard-favorites').css('display', 'block')
                Swal.fire({
                    position: 'top-end',
                    icon: 'success',
                    title: response.success,
                    showConfirmButton: false,
                    timer: 1500
                })
            }else if (response.error){
                Swal.fire({
                    position: 'top-end',
                    icon: 'error',
                    title: response.error,
                    showConfirmButton: false,
                    timer: 1500
                })
            }
        }
    })
})

$('#discard-favorites').on('click', function(){
    prod_name = $(this).attr('name')
    $.ajax({
        url: `/products/discard-favorites/${prod_name}`,
        type: 'GET',
        success: function(response){
            if (response.success){   
                $('#add-favorites').css('display', 'block')
                $('#discard-favorites').css('display', 'none')
                Swal.fire({
                    position: 'top-end',
                    icon: 'success',
                    title: response.success,
                    showConfirmButton: false,
                    timer: 1500
                })
            }else if (response.error){
                Swal.fire({
                    position: 'top-end',
                    icon: 'error',
                    title: response.error,
                    showConfirmButton: false,
                    timer: 1500
                })
            }
        }
    })
})

// $(document).ready(function () {
//     checker = $('#favorites_check').textContent

//     if (checker == 'favorite'){
//         $('#add-favorites').css('display', 'none')
//     }else{
//         $('#discard-favorites').css('display', 'none')
//     }
// })
