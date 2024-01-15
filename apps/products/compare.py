# modulehaye joda mesle compare.py ya shop_cart.py(dakhele apps.orders) ba session kar daran

# yek list(compare_product) az product.id bar migardunes
class CompareProduct:
    def __init__(self,request):
        self.session=request.session
        compare_product=self.session.get('compare_product')
        if not compare_product:
            compare_product=self.session['compare_product']=[]              # yek list khali miyare
        self.compare_product=compare_product
        self.count=len(self.compare_product)
        
    def add_to_compare_product(self,productId):
        productId=int(productId)
        if productId not in self.compare_product:
            self.compare_product.append(productId)
        self.count=len(self.compare_product)
        self.session.modified=True
        
    def delete_from_compare_product(self, productId):
        self.compare_product.remove(int(productId))
        self.session.modified=True
        
    def clear_compare_product(self):
        del self.session['compare_product']
        self.session.modified=True
        
    def __iter__(self):
        compare_product=self.compare_product.copy()
        for item in compare_product:
            yield item