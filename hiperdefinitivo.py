import requests
import json
import csv
import re
import pandas as pd

class Product:
    def __init__(self, name, description, category, price, list_price, stock, url, sku):
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.list_price = list_price
        self.stock = stock
        self.url = url
        self.sku = sku

class Sucursal:
    def __init__(self, num):
        self.num = num
        self.products = []
    
    def get_products(self):
        for i in range(0, 50):
            response = requests.get(f"https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/?&_from={i*50}&_to={(i+1)*50-1}&ft&sc={self.num}").text 
            objeto = json.loads(response)
            for item in objeto:
                name = item['productName']
                description = item['description']
                category = item['categoryId']
                price = item['items'][0]["sellers"][0]["commertialOffer"]["Price"]
                list_price = item['items'][0]["sellers"][0]["commertialOffer"]["PriceWithoutDiscount"]
                stock = item['items'][0]["sellers"][0]["commertialOffer"]["AvailableQuantity"]
                url = item['link']
                sku = item['items'][0]['itemId']
                product = Product(name, description, category, price, list_price, stock, url, sku)
                self.products.append(product)
    
    def to_dict(self):
        products_dict = []
        for product in self.products:
            product_dict = {'sku': product.sku,
                            'producto': product.name,
                            'categoria': product.category,
                            'precio': product.price,
                            'precio_lista': product.list_price,
                            'stock': product.stock,
                            'url': product.url,
                            'descripcion': product.description}
            products_dict.append(product_dict)
        return {'sucursal': self.num, 'productos': products_dict}

suc_num = input("ingrese sucursal de 1 a 16: ")
sucursal = Sucursal(suc_num)
sucursal.get_products()
sucursal_total = sucursal.to_dict()

# Convertir sucursal_total a dataframe
df = pd.DataFrame(sucursal_total['productos'])

# Exportar el dataframe a archivo CSV con el ID de la sucursal dado en el input
filename = f"productos_sucursal_{suc_num}.csv"
df.to_csv(filename, index=False)

# Exportar el dataframe a archivo Excel con el ID de la sucursal dado en el input
filename = f"productos_sucursal_{suc_num}.xlsx"
df.to_excel(filename, index=False)
