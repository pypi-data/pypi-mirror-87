import requests, json

class ShopifyController:
    @classmethod
    def create_product(self, domain='', app_key='', app_secret='', product=''):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        url = f"https://{app_key}:{app_secret}@{domain}/admin/products.json"
        
        title = product['product']['title']
        r = requests.post(url, json=product,  headers=headers)
        if r.status_code == 201:
            print(f'Creating Product: {title}, Response: {r.status_code}')
        else:
            print(f'Creating Product: {title}, Response: {r.status_code}, Error: {r.content.decode("utf-8")}')
        return r.json()

    @classmethod
    def get_all_products(self, domain='', app_key='', app_secret=''):
        url = f"https://{app_key}:{app_secret}@{domain}/admin/products.json"
        r = requests.get(url)
        return r.json()

    @classmethod
    def get_specific_product(self, domain='', app_key='', app_secret='', productId=''):
        url = f"https://{app_key}:{app_secret}@{domain}/admin/products/{productId}.json"
        r = requests.get(url)
        return r.json()

    @classmethod
    def get_specific_variant(self, domain='', app_key='', app_secret='', skuId=''):
        url = f"https://{app_key}:{app_secret}@{domain}/admin/variants/{skuId}.json"
        r = requests.get(url)
        return r.json()

    @classmethod
    def get_specific_inventory(self, domain='', app_key='', app_secret='', inventoryId=''):
        url = f"https://{app_key}:{app_secret}@{domain}/admin/inventory_items/{inventoryId}.json"
        r = requests.get(url)
        return r.json()
    
    @classmethod
    def get_all_locations(self, domain='', app_key='', app_secret='', inventoryId=''):
        url = f"https://{app_key}:{app_secret}@{domain}/admin/locations.json"
        r = requests.get(url)
        return r.json()

    @classmethod
    def update_variant(self, domain='', app_key='', app_secret='', productId='', product=''):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        url = f"https://{app_key}:{app_secret}@{domain}/admin/variants/{productId}.json"
        title = product['variant']['sku']
        r = requests.put(url, json=product,  headers=headers)
        if r.status_code == 200:
            print(f'Updating Product: {title}, Response: {r.status_code}')
        else:
            print(f'Updating Product: {title}, Response: {r.status_code}, Error: {r.content.decode("utf-8")}')
        return r.status_code

    @classmethod
    def update_inventory(self, domain='', app_key='', app_secret='', inventory=''):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        url = f"https://{app_key}:{app_secret}@{domain}/admin/inventory_levels/set.json"

        r = requests.post(url, json=inventory,  headers=headers)
        if r.status_code == 200:
            print(f'Updating SKU inventory... Response: {r.status_code}')
        else:
            print(f'Updating SKU inventory... Response: {r.status_code}, Error: {r.content.decode("utf-8")}')
        return r.status_code

    @classmethod
    def delete_product(self, domain='', app_key='', app_secret='', productId=''):
        url = f"https://{app_key}:{app_secret}@{domain}/admin/products/{productId}.json"
        r = requests.delete(url)
        print(r.status_code)
