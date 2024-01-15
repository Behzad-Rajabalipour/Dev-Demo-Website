from apps.products.models import Product

# self.shop_cart = {
#         "24":{"qty:3","price":20000},                                     
#         "13":{},
#
# }
 
# in class ro to view estefade mikonim
class ShopCart:
    def __init__(self,request):
        self.session= request.session                   # session client dar web ro miyare. az tarighe cookies ham mishe 
        temp=self.session.get("shop_cart")
        if not temp:
            self.session["shop_cart"]={}
            temp=self.session["shop_cart"]
        self.shop_cart=temp
        self.count=len(self.shop_cart.keys())            

    def add_to_shop_cart(self,product,qty,color):             
        product_id=str(product.id)
        if product_id not in self.shop_cart:            # mire to keys migarde
            self.shop_cart[product_id]={"qty":0,"price":product.price,"colors":[color],"final_price":product.get_price_by_discount()}
        elif color not in self.shop_cart[product_id]["colors"]:         # if color is not in colors list, then add it
            self.shop_cart[product_id]["colors"].append(color)
            
        self.shop_cart[product_id]["qty"]+=int(qty)
        self.count=len(self.shop_cart.keys())
        self.session.modified=True                  # vaghti session ro taghir midi bayad in line ro benevisi
        
    def delete_from_shop_cart(self,product):
        product_id=str(product.id)
        del self.shop_cart[product_id]
        self.session.modified=True
    
    def calc_total_price(self):
        sum=0
        for item in self.shop_cart.values():
            sum+=int(item["final_price"])*item["qty"]
        return sum
    
    def update(self,product_id_list,qty_list):
        i=0
        for product_id in product_id_list:
            self.shop_cart[product_id]['qty']=int(qty_list[i])           # chon product id dar product_id_list va qty dar qty_list dar index hamsan hastan
            i+=1
        self.session.modified=True
            
    #    {"qty:3", "price":20000, "product":product1, "total_price":60000}                                     
    #    {"qty":2, "price":50000, "product":product2, "total_price":10000}
    #    ...
    def __iter__(self):                             # in class ro iterable mikone va mitunim rosh ba for harekat konim
        list_product_id=self.shop_cart.keys()
        products=Product.objects.filter(id__in=list_product_id)
        temp=self.shop_cart.copy()
        for product in products:
            temp[str(product.id)]["product"]=product        # kole un product dakheleshe
            
        for item in temp.values():                  # inja migim roye chi iterable bashe
            item["total_price"]=int(item["final_price"])*item["qty"]
            yield item
            
        
        
        