//------------------------------------------------------------
// vaghti page load shod
document.addEventListener('DOMContentLoaded',function(){            // DOMContentLoaded baraye ineke caghti page load shod
    document.querySelectorAll('.decrement-button').forEach(function(button){
        button.addEventListener('click',function(){
            var inputField= this.parentNode.parentNode.querySelector('input[type=number]');     // ba parentNode.parentNode 2ta vald mirim bala
            var currentValue = parseInt(inputField.value);
            if (currentValue > 1){
                inputField.value = currentValue - 1;        // inja type inputField ro ham avaz mikoni be int
            }
        });
    });

    document.querySelectorAll('.increment-button').forEach(function(button){
        button.addEventListener('click',function(){
            var inputField= this.parentNode.parentNode.querySelector('input[type=number]');
            var currentValue = parseInt(inputField.value);
            inputField.value = currentValue + 1;        // inja type inputField ro ham avaz mikoni be int
            
        });
    });
})

//------------------------------------------------------------
// neshun dadan va "," gozashtan value
function showValue(x){
    x=x.toString().replace(/\B(?=(\d{3})+(?!\d))/g,",")
    document.getElementById("sel_price").innerText=x;
    // document.getElementById("inputVal").value=x;
}

//------------------------------------------------------------
// remove va adde sort_type az url 
function removeURLParam(url, parameter){
    var urlparts=url.split('?');
    if (urlparts.length >=2){
        var prefix=encodeURIComponent(parameter) + '=';
        var pars=urlparts[1].split(/[&;]/g);                    //pars = parameters
        for (var i=pars.length;i-->0;){
            if (pars[i].lastIndexOf(prefix, 0) !== -1){
                pars.splice(i,1)
            }
        }
        return urlparts[0]+(pars.length>=0 ? '?'+ pars.join('&') : '')
    }
    return url;
}

// Sort
function select_sort(){
    var select_sort_value=$("#select_sort").val();
    if (window.location.href.indexOf("?") !== -1){                          // window.location = URL. If we don't put href, indexOf() will not work. get indexOf "?" in the URL. If it doesn't exists it returns -1
        // this two below line, rewrite URL with Ajax
        var url=removeURLParam(window.location.href,"sort_type");           // this line removes sort_type parameter from URL if it already exists
        window.location= url+"&sort_type="+select_sort_value;
    }
    else{
        window.location= window.location+"?sort_type="+select_sort_value;   // window.location = URL
    }
}

// Number of Product shows 
function AdjustNumberOfProducts(){
    var products_per_page_value=$('#productsPerPage').val();
    if(window.location.href.indexOf("?") !== -1 ){
        var url=removeURLParam(window.location.href,"productsPerPage");
        window.location= url+"&productsPerPage="+products_per_page_value;
        // $("#productsPerPage option").removeClass("active");              // option hayi ke farzande id productsPerPage
        // $(`#option_${products_per_page_value}`).addClass("active");
    }
    else{
        window.location= window.location+"?productsPerPage="+products_per_page_value;
    }
}

// Paginator
function AdjustPage(page){
    var page_value = $(`#page_${page}`).text()
    if(window.location.href.indexOf("?") !== -1 ){
        var url=removeURLParam(window.location.href,"page");
        window.location= url+"&page="+page_value;
    }
    else{
        window.location= window.location+"?page="+page_value;
    }
}

//------------------------------------------------------------
// zakhire checked shodehaye filter ghabli
$(document).ready(
    function(){
        //Part 3
        var urlparams= new URLSearchParams(window.location.search);
        if (urlparams == ""){
            localStorage.clear();
            $("#filter_state").css("display", "none");                      // alamate X zamane filter shodan hast
            
            var counterTag = $('#counter');
            var counter = parseInt(counterTag.text());
            if (counter === 1 ){
                alert("Welcome to Behzad Rajabalipour's website. \n" +
                  "For this website, I've used Django for the coding aspect, \n" +
                  "Amazon S3 buckets for image storage, and \n" +
                  "Amazon RDS (MySQL) for record database");
            }
        }
        else{
            $("#filter_state").css("display", "inline-block");
        }
        // Part1. set on click
        $("input:checkbox").on("click", function(){
            var fav,favs=[];                                                  // favs = favorites
            $("input:checkbox").each(function(){
                fav={id: $(this).attr("id"),value: $(this).prop("checked")};
                favs.push(fav);
            })
            localStorage.setItem("favorites",JSON.stringify(favs))                  // inja az localStorage estefade kardim. az Url ham mishod begirim.
        })
        // Part2. get automatically
        var favorites=JSON.parse(localStorage.getItem("favorites"));                // localStorage => {favorites: [{23:"1"}, {65:"3"}]}
        for (var i=0;i<favorites.length;i++){
            $("#"+favorites[i].id).prop("checked", favorites[i].value)
        }
    }
);

//------------------------------------------------------------
function status_of_shop_cart(){
    $.ajax({                                                                
        type:"GET",
        url:"/orders/status_of_shop_cart/",                               
        success:function(res){
            $("#indicator__value").text(res);
        }
    })
}

status_of_shop_cart()                                // in function vaghti safhe load mishe ejra mishe

function add_to_shop_cart(product_id,qty){           // products.html
    if (qty===0){                                    // product_detail.html
        qty=$("#product-quantity").val();
    }
    var color = '';

    var selectedColorRadioInput = $('input[type=radio][name=color]:checked');

    if (selectedColorRadioInput.length > 0) {
        var color = selectedColorRadioInput.closest('label').attr('data');
    } else {
        var color ="White";
    }

    $.ajax({
        type:"GET",
        url:"/orders/add_to_shop_cart/",
        data:{
            product_id:product_id,
            qty:qty,
            color:color
        },
        success: function(res){
            alert("Item is added");
            status_of_shop_cart();              // in baraye update kardane addad dar navbar hast
        }
    })
}

function delete_from_shop_cart(product_id){
    $.ajax({                                                                // Ajax = bedune in ke safe reload beshe send kon
        type:"GET",
        url:"/orders/delete_from_shop_cart/",                               // hatman / aval va akhar ro bezar
        data:{
            product_id:product_id,
        },
        success:function(res){
            $("#shop_cart_list").html(res);                                 // show_shop_cart.html
            status_of_shop_cart();                            // in baraye update kardane addad dar navbar hast
        }
    })
}

function update_shop_cart(){
    //jquery
    var product_id_list=[];                                         
    var qty_list=[];
    $("input[id^='item3_']").each(function(index){                  // foreach ham mishe. index 6 be bad product.id
        product_id_list.push($(this).attr("id").slice(6))           // slice mikone va az index 6 be bad miyare
        qty_list.push($(this).val())
    });
    //ajax
    $.ajax({                                                                
        type:"GET",
        url:"/orders/update_shop_cart/",                               
        data:{
            product_id_list: product_id_list,
            qty_list: qty_list,
        },
        success:function(res){
            $("#shop_cart_list").html(res);
            status_of_shop_cart();                          // in baraye update kardane addad dar navbar hast
        }
    })
}

function showCreateCommentForm(productId,commentId,slug){
    $.ajax({
        type:"GET",
        url:"/csf/create_comment/"+slug,                             // slug be sorate params(querystring) mire
        data:{                                                       // be sorate data mire
            productId: productId,
            commentId: commentId,
        },
        success: function(res){                                     // to bargash buttone response ro hide mikone va form ro neshun mide
            $("#btn_"+commentId).hide();
            $("#comment_form_"+commentId).html(res);                // form bargashte. res=form(). formi bargashte ke comment_id va product_id esh pore. ref to csf_app/partials/create_comment.html
        }
    });

}

//----------------------------------------------------------------
function addScore(score, productId){
    var starRating=document.querySelectorAll(".fa-star");

    starRating.forEach(element =>{
        element.classList.remove("checked");
    })

    for (let i=1; i<=score; i++){
        const element=document.getElementById("star_"+ i);
        element.classList.add("checked");
    }

    $.ajax({
        type:"GET",
        url:"/csf/add_score/",                             
        data:{                                                       
            productId: productId,
            score: score,
        },
        success: function(res){                                     
            alert(res);
        }
    });   
}



function addToFavorites(productId){
    $.ajax({
        type:"GET",
        url:"/csf/add_to_favorite/",                             
        data:{                                                       
            productId: productId,
        },
        success: function(res){                                     
            alert(res);
            // we used class(.) because I used this favorite in two different place
            $(`.icon_${productId}`).addClass("fa-heart redHeart").removeClass("fa-heart-broken");    
            // location.reload();                          // It reloads the page
            $(`.btn_${productId}`).attr('onclick',`removeFromFavorites(${productId})`);  // change attribute named onclick=""

        }
    });   
}

function removeFromFavorites(productId){
    $.ajax({
        type: "GET",
        url:"/csf/remove_from_favorite/",
        data:{
            productId: productId,
        },
        success: function(res){
            alert(res);             // answer comeback from views.py => HttpResponse()
            // we used class(.) because I used this favorite in two different place
            $(`.icon_${productId}`).addClass("fa-heart-broken").removeClass("fa-heart redHeart");
            // location.reload();                      // reload the page
            $(`.btn_${productId}`).attr('onclick',`addToFavorites(${productId})`);  // change attribute named onclick=""
            
        },
        error: function(xhr, status, error){
            alert(error);
        }
    })
}

//------------------------------------------------------------------
status_of_compare_list();                               // age fun dakhele fun darim bayad fune dakheli ro injuri seda bezanim 

function status_of_compare_list(){
    $.ajax({
        type:"GET",
        url:"/products/status_of_compare_list/",
        success: function(res){
            if (Number(res) === 0){
                $("#compare_count_icon").hide();        // hide and show compare icon in navbar.html
            }
            else{
                $("#compare_count_icon").show();
                $("#compare_count").text(res);          // shows count of items in compare list
            }
        }
    });
}

function addToCompareList(productId,productGroupId){
    $.ajax({
        type:"GET",
        url:"/products/add_to_compare_list/",
        data:{
            productId:productId,
            productGroupId:productGroupId
        },
        success: function(res){
            alert(res);
            status_of_compare_list();
        }
    })
}

function deleteFromCompareList(productId){
    $.ajax({
        type:"GET",
        url:"/products/delete_from_compare_list/",
        data:{
            productId:productId,
        },
        success: function(res){                                 // res inja redirect bargashte
            alert("product is deleted");
            $("#compare_list").html(res)
            status_of_compare_list();
        }
    })
}

//------------------------------------------------------------------

