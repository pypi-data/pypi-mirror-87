import requests, json, datetime, sys
from .utils import Utils
from .models.product import Product
from .models.product import StoreProduct
from .models.order import OrderProductPackageDimensions
from .models.order import OrderProduct
from .models.order import OrderAddress
from .models.order import OrderPayment
from .models.order import OrderCustomerAddress
from .models.order import OrderCustomer
from .models.order import OrderShippingAddress
from .models.order import OrderShippingItem
from .models.order import OrderShipping
from .models.order import InvoiceItem
from .models.order import Invoice
from .models.order import Order

class HubController:
    @classmethod
    def authenticate(self, server_url='', user='', passwd=''):
        # create headers
        headers = dict()
        headers['Content-Type'] = 'application/json'

        # authenticate payload
        payload = dict()
        payload['username'] = user
        payload['password'] = passwd

        # do login request
        r = requests.post(f'{server_url}/signin/', headers=headers, data=json.dumps(payload))
        
        # catch error
        if r.status_code != 200:
            raise Exception(f'Failed to login on NappHUB...try again... {r.content.decode("utf-8")}')

        # get and return token
        token = json.loads(r.content.decode('utf8'))['token']
        return token

    @classmethod
    def get_all_attributes(self, server_url='', token=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # do request
        r = requests.get(f'{server_url}/attributes/', headers=headers)
        r = r.content.decode('utf-8')
        
        # create products object
        attributes = None
        
        # check if exists products on this server
        if r != 'null':
            attributes = json.loads(r)
        
        # return
        return attributes

    @classmethod
    def get_product_by_id(self, server_url='', token='', product_id=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # do request
        r = requests.get(f'{server_url}/products/{product_id}', headers=headers)
        r = r.content.decode('utf-8')
        
        # create products object
        product = None
        
        # check if exists products on this server
        if r != 'null':
            product = json.loads(r)
        
        # return
        return product

    @classmethod
    def get_all_products(self, server_url='', token=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # do request
        r = requests.get(f'{server_url}/products/', headers=headers)
        r = r.content.decode('utf-8')
        
        # create products object
        products = None
        
        # check if exists products on this server
        if r != 'null':
            products = json.loads(r)
        
        # return
        return products

    @classmethod
    def get_all_store_products(self, server_url='', token='', store_id=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # do request
        r = requests.get(f'{server_url}/storeProductsByStore/{store_id}', headers=headers)
        r = r.content.decode('utf-8')
        
        # create products object
        store_products = None
        
        # check if exists products on this server
        if r != 'null':
            store_products = json.loads(r)
        
        # return
        return store_products

    @classmethod
    def get_product_by_ean(self, server_url='', token='', ean=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # do request
        r = requests.get(f'{server_url}/productsByEan/?ean={ean}', headers=headers)
        r = r.content.decode('utf-8')

        # create id object
        product = None
        
        # find store product
        if r != 'null':
            product = json.loads(r)
        
        # return
        return product

    @classmethod
    def get_store_product_by_id(self, server_url='', token='', id='', store_id=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # do request
        r = requests.get(f'{server_url}/storeProducts/{id}', headers=headers)
        r = r.content.decode('utf-8')
        
        # create id object
        store_product = None
        
        # find store product
        if r != 'null':
            store_product = json.loads(r)
        
        # return
        return store_product

    @classmethod
    def get_store_product_by_erpCode(self, server_url='', token='', erp_code='', store_id=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # do request
        r = requests.get(f'{server_url}/storeProductsByErpCodeAndStore/{erp_code}/{store_id}', headers=headers)
        r = r.content.decode('utf-8')

        # create id object
        store_product = None
        
        # find store product
        if r != 'null':
            store_product = json.loads(r)
        
        # return
        return store_product

    @classmethod
    def get_store_product_by_productCodeOrEan(self, server_url='', token='', store_id='', product_code='', ean=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # do request
        r = None
        if product_code != '':
            r = requests.get(f'{server_url}/storeProducts/?storeId={store_id}&productCode={product_code}', headers=headers)
        elif ean != '':
            r = requests.get(f'{server_url}/storeProducts/?storeId={store_id}&ean={ean}', headers=headers)
        r = r.content.decode('utf-8')
        print(r)

        # create object
        store_product = None
        
        # find store product
        if r != 'null':
            store_product = json.loads(r)['data']
        
        # return
        return store_product

    @classmethod
    def get_store_product_marketplace(self, server_url='', token='', marketplace_id='', store_id='', store_product_id=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        r = requests.get(f'{server_url}/storeProductsMarketplace/?marketplaceId={marketplace_id}&storeId={store_id}&storeProductId={store_product_id}', headers=headers)
        r = r.content.decode('utf-8')

        # find store product marketplace
        store_product_marketplace = json.loads(r)['data']

        # return
        return store_product_marketplace

    @classmethod
    def create_store_product_marketplace(self, server_url, token, store_product_marketplace=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # create 'store product marketplace' payload
        payload_store_product_marketplace = json.dumps(store_product_marketplace, ensure_ascii=False)

        # do request on POST/storeProductsMarketplace
        r = requests.post(f'{server_url}/storeProductsMarketplace/', headers=headers, data=payload_store_product_marketplace)
        print(f'Creating store product marketplace...{r.status_code} - {r.content.decode("utf-8")}')

    @classmethod
    def update_store_product_marketplace(self, server_url, token, store_product_marketplace=''):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # create 'store product marketplace' payload
        payload_store_product_marketplace = json.dumps(store_product_marketplace, ensure_ascii=False)

        # do request on POST/storeProductsMarketplace
        r = requests.put(f'{server_url}/storeProductsMarketplace/', headers=headers, data=payload_store_product_marketplace)
        print(f'Updating store product marketplace...{r.status_code} - {r.content.decode("utf-8")}')

    @classmethod
    def update_store_product(self, server_url, token, product, store_product_id, product_id):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # set hub product ID on object store product
        product.storeProduct.id = store_product_id
        product.storeProduct.productId = Utils.create_values(product_id, 'Int64')

        # create store product update payload
        payload_store_product = json.dumps(product.storeProduct.__dict__, ensure_ascii=False)

        # do request on PUT/storeProducts
        r = requests.put(f'{server_url}/storeProducts/', headers=headers, data=payload_store_product)

        # log
        print(f'Updating StoreProducts ID <{product.storeProduct.id}>... {r.status_code}:{r.content.decode("utf-8")}')

    @classmethod
    def create_store_product(self, server_url, token, product, product_id):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # create store product payload
        payload_store_product = product.storeProduct.__dict__

        # create 'store product' payload
        payload_store_product['productId'] = Utils.create_values(product_id, 'Int64')
        payload_store_product = json.dumps(payload_store_product, ensure_ascii=False)

        # do request on POST/storeProducts
        r = requests.post(f'{server_url}/storeProducts/', headers=headers, data=payload_store_product)
        print(f'Creating store product...{r.status_code} - {r.content.decode("utf-8")}')

    @classmethod
    def update_product(self, server_url, token, product):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # create product update payload
        product = product.__dict__
        product['storeProduct'] = None
        payload_product = json.dumps(product, ensure_ascii=False)
        
        # do request on PUT/storeProducts
        r = requests.put(f'{server_url}/products/', headers=headers, data=payload_product)

        # log
        print(f'Updating Products... ID <{product["id"]}>... {r.status_code}:{r.content.decode("utf-8")}')


    @classmethod
    def create_products(self, server_url='', token='', store_id='', products=[], use_ean=False, use_sku=False, update_product=False, update_store_product=False):
        # create headers
        headers = dict()
        headers['Authorization'] = f'Bearer {token}'

        # create arrays
        hub_products = []
        hub_products_not_found = []

        # loop in all integration produtcs
        for product in products:
            # create request object
            r = None

            # get product ids string
            productEan = product.productEan['String']
            productCode = product.productCode['String']
            
            # Check if use ean or sku to find product
            if use_ean:
                r = requests.get(f'{server_url}/productsByEan/?ean={productEan}', headers=headers)
            elif use_sku:
                r = requests.get(f'{server_url}/productsByProductCode/?code={productCode}&storeId={store_id}', headers=headers)

            # check if request exists
            if r:
                # find hub product id based on integration product
                hub_product = json.loads(r.content.decode('utf-8'))
                hub_product_id = hub_product['id'] 

                # check if product id exists on napp hub
                if hub_product_id != 0:
                    # log
                    print(f'Code <{productEan}>/<{productCode}> exists on Napp HUB')

                    # check update enabled
                    if update_store_product:
                        # find store product id
                        store_product = self.get_store_product_by_erpCode(
                            server_url=server_url, 
                            token=token, 
                            erpCode=productCode, 
                            store_id=store_id)
                        
                        # update if exists or create
                        if store_product: 
                            self.update_store_product(
                                server_url=server_url, 
                                token=token,
                                product=product,
                                store_product_id=store_product['id'], 
                                product_id=hub_product_id)
                        else:
                            self.create_store_product(
                                server_url=server_url,
                                token=token,
                                product=product,
                                product_id=hub_product_id)

                    # update product
                    if update_product:
                        # set hub product id on object product
                        product.id = hub_product_id

                        # call
                        self.update_product(
                            server_url=server_url,
                            token=token, 
                            product=product)
                else:
                    # create store product payload
                    payload_store_product = product.storeProduct.__dict__

                    # clear 'store products' from 'products' and create a new payload
                    product = product.__dict__
                    product['storeProduct'] = None
                    payload_product = json.dumps(product, ensure_ascii=False)

                    # do request on POST products
                    r = requests.post(f'{server_url}/products/', headers=headers, data=payload_product)
                    print(f'Creating product...{r.status_code} - {r.content.decode("utf-8")}')

                    if r.status_code == 200:
                        # get created product id
                        product_id = int(r.content.decode('utf-8'))

                        # call function
                        self.create_store_product(
                            server_url=server_url,
                            token=token,
                            product=product,
                            product_id=product_id)
    
    @classmethod
    def find_parents_childs(self, server_url='', token='', store_products=''):
        # create arrays and tmp last parent id
        parents = []
        products = []
        last_parent = 0

        # loop in all store products
        for store_product in store_products:
            # get product ID and product object
            product_id = store_product['productId']
            product = self.get_product_by_id(server_url=server_url, token=token, product_id=product_id)
            
            # append products to list and get parent ID
            products.append({'storeProduct': store_product['storeProductId'], 'product': product})
            parent_id = product['parentId']['Int64']

            # check if parent id is different from last parent id check
            if parent_id != last_parent:
                # get product parent object and append to list
                parent = self.get_product_by_id(server_url=server_url, token=token, product_id=product['parentId']['Int64'])
                parents.append({'storeProduct': store_product['storeProductId'], 'product': parent})
                
                # set latest parent id
                last_parent = parent_id
        
        return parents, products
