import requests, json

class OpaBoxController:
    @classmethod
    def create_products(self, server_url, company, api_token='', products=[]):
        # create headers
        headers = {'Content-Type': 'Application/json'}

        # create url
        url = f'{server_url}/prod/v2/company/{company}/products?api_token={api_token}'
        
        # create product payload
        payload_product = json.dumps(products, ensure_ascii=False)

        # do request to create a product
        r = requests.put(url, headers=headers, data=payload_product)
        
        # # log
        print(f'OpaBox create products {r.status_code}:{r.content}')

    @classmethod
    def update_product(self, server_url, company, api_token='', products=[]):
        # create headers
        headers = {'Content-Type': 'Application/json'}
        
        # create url
        url = f'{server_url}/prod/v2/company/{company}/products_price_stock?api_token={api_token}'
        
        # create product payload
        payload_product = json.dumps(products, ensure_ascii=False)

        # do request to create a product
        r = requests.post(url, headers=headers, data=payload_product)
        
        # # log
        print(f'OpaBox update products {r.status_code}:{r.content}')
