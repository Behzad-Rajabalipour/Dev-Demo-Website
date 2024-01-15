$(document).ready(function(){
    var ListOfElements=$('select[id^="id_product_features-"][id$="-feature"]');
    $(ListOfElements).on("change", function(){
        f_id= $(this).val();
        dropdown1=$(this).attr("id");
        dropdown2=dropdown1.replace("-feature","-filter_value");

        $.ajax({
            type:"GET",
            url: "/products/ajax_admin/?feature_id="+ f_id,
            success: function(res){
                cols=document.getElementById(dropdown2);
                cols.options.length=0;
                for (var k in res){
                    cols.options.add(new Option(k, res[k]));
                }
            }
        })
    })
})