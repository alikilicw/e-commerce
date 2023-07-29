$(document).ready(function(){
    
    var city = $("#city-input").val();
    if (city != '') {
        $('#district-input').attr('disabled', false)
    }else{
        $("#district-input").val(null).trigger('change');
    }
    $("#city-input").on("change", function() {
        var city = $("#city-input").val();
        if (city != '') {
            $('#district-input').attr('disabled', false);
            $("#district-input").val(null).trigger('change');   
        }
    });

    $('#country-input').select2({
        placeholder : 'Ülke'
    })

    $('#city-input').select2({
        placeholder: 'İl',
        ajax : {
            url : function (params) {
                var country_value = $("#country-input").val();
                if (!params.term){
                    params.term = "_empty_"
                }
                return `/products/filter/${country_value}/${params.term}/all!`
            },
            dataType : 'json',
            type : 'GET',
            delay : 250,
            processResults : function(data){
                return {
                    results : $.map(data.city_list, function(item){
                        return  {id : item['il'],text : item['il']}
                    })
                }
            },
            cache : false
        }
    });

    $('#district-input').select2({
        placeholder: 'İlçe',
        ajax : {
            url : function (params) {
                var country_value = $("#country-input").val();
                var city_value = $("#city-input").val();
                if (!params.term){
                    params.term = "_empty_"
                }
                return `/products/filter/${country_value}/${city_value}/${params.term}`
            },
            dataType : 'json',
            type : 'GET',
            delay : 250,
            processResults : function(data){
                return {
                    results : $.map(data.district_list, function(item){
                        return  {id : item, text : item}
                    })
                }
            },
            cache : true
        }
    });
})
    
// function locationUrl(){
//     var country_value = document.getElementById("country-input").value;
//     var city_value = document.getElementById("city-input").value;
//     var district_value = document.getElementById("district-input").value;

//     var locationStr=""
//     if (city_value.length < 2 && district_value.length < 2){
//         locationStr = country_value
//     }else if (district_value.length < 2){
//         locationStr = country_value + "-" + city_value
//     }else{
//         locationStr = country_value + "-" + city_value + "-" + district_value
//     }
//     locationStr += "/"

//     var action_src = "location=" + (locationStr).toString()
//     var your_form = document.getElementById('location-form');
//     your_form.action = action_src ; 
// }