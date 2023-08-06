## **NappLIB**

![version](version.svg) ![git](https://img.shields.io/github/commit-activity/m/leandrovieiraa/napplib?style=for-the-badge)

NappLib
https://pypi.org/project/napplib/

### ToDo

**Azure**
- Blob Storage
  - [x] Listar último arquivo
  - [x] Listar todos arquivos
  - [x] Listar arquivo espefico
  - [x] Upload de arquivo

**Napp HUB**
- Produtos
  - [ ] Cadastro de marca
  - [ ] Cadastro de atributo
  - [ ] Cadastro de categoria
  - [ ] Cadastro de inventário em um canal
  - [x] Cadastro de inventário
  - [x] Cadastro de produto
    - [ ] Cadastro de produto filho
  - [x] Atualizar inventário
  - [x] Atualizar produto
- Vendas
  - [ ] Cadastro de venda
  - [ ] Cadastro de nota
  - [ ] Cadastro de entrega
  - [ ] Cadastro de cliente
  - [ ] Cadastro de pagamento
  - [ ] Atualizar status da venda

**VTex**
- Produtos
  - [x] Cadastro de produto
  - [x] Cadastro de SKU
  - [x] Cadastro de preco
  - [x] Cadastro de inventário
  - [x] Atualizar produto
  - [x] Atualizar SKU
  - [x] Atualizar preco
  - [x] Atualizar inventário
- Vendas
  - [ ] ToDo...

### **Sobre**

Nós criamos essa biblioteca para auxiliar na integração dos nosso serviços e parceiros:

- Serviços Azure
- Napp HUB
- FTP e Base de dados remotas
- Conexoes com Webservices
- Plataformas de Marketplace

## **Funções**

### **Construir**

Abra o arquivo **setup.py** e altere a versão, após a mudança basta executar o arquivo abaixo:

```
./build.sh
```

### **Instalação**

```
pip install napplib
```

### **Azure Storage**

```python
from napplib.azure.blob_storage import BlobStorage
```

Função para retornar os dados do ultimo arquivo blob

```python
BlobStorage.get_latest_blob(
    account_name='AZURE_ACCOUNT_NAME',
    account_key='AZURE_ACCOUNT_KEY',
    path='AZURE_BLOB_ROOT_CONTAINER',
    project='PROJECT_NAME',
    store_name='STORE_NAME')
```

**Obs:** Vocë poderá adicionar o parametro **custom_encoding** caso seja diferente de **utf8**

Função para retornar os dados de um arquivo blob específico.

```python
BlobStorage.get_blob(
    account_name='AZURE_ACCOUNT_NAME',
    account_key='AZURE_ACCOUNT_KEY',
    path='AZURE_BLOB_ROOT_CONTAINER',
    blob_path='project/store/2020/10/23/sample.csv')
```

**Obs:** Vocë poderá adicionar o parametro **custom_encoding** caso seja diferente de **utf8**

Função que envia um arquivo local para o azure blob storage utilizando o modelo Napp, Ex: *project/store/year/month/day/file*

```python
BlobStorage.upload_blob(
    account_name='AZURE_ACCOUNT_NAME',
    account_key='AZURE_ACCOUNT_KEY',
    path='AZURE_BLOB_ROOT_CONTAINER',
    project='PROJECT_NAME',
    store_name='STORE_NAME',
    output_file='./files/sample.csv')
```

Lista todos arquivos blob de um determinado "projeto/loja"

```python
BlobStorage.list_all_blobs(
    account_name='AZURE_ACCOUNT_NAME',
    account_key='AZURE_ACCOUNT_KEY',
    path='AZURE_BLOB_ROOT_CONTAINER',
    project='PROJECT_NAME',
    store_name='STORE_NAME')
```

Para "parsear" os dados, poderá usar o seguinte modelo

```python
delimiter = '|'
lines = content.split('\n')
for line in lines:
    rows = line.split(delimiter)
    try:
        # parse here, rows[0], rows[1] ...
    except:
        # invlid line (always has one line empty)
        pass
```

**Obs**: *O split devera ocorrer por linha devido ao retorno do arquivo*

### **Napp HUB**

Importar todos modelos e controles

```python
from napplib.hub.models.product import Product
from napplib.hub.models.product import StoreProduct
from napplib.hub.controller import HubController
```

Variáveis necessárias para usar este controle

```python
hub_store_id = 0
hub_username = ''
hub_password = ''
hub_url = ''
```

Esta função cria todos objetos no Napp HUB  responsáveis para integrar um produto. Será necessário criar todos modelos abaixo

- product
- store product
- categories
- brands
- attributes

Essa função possui alguns gatilhos que podem ser utilizados

- **update_product**:  Esse gatilho atualiza o produto (product) quando verdadeiro, quando falso o controle ira somente criar o produto e não atualiza-lo caso exista.
- **update_store_product****: Esse gatilho atualiza o estoque da loja (storeProduct) quando verdadeiro, quando falso o controle ira somente criar o inventário e não atualiza-lo caso exista.

**Função**

```python
HubController.create_products(
    server_url=hub_url,
    token=hub_token,
    store_id=hub_store_id,
    products=hub_products,
    use_sku=True,
    update_product=True,
    update_store_product=True)
```

**Modelo StoreProduct**

```python

store_product = StoreProduct(
    storeId=HUB_STORE_ID,
    stockQuantity=0,
    salePrice=0,
    active=True,
    productCode='',
    productEan='',
    erpCode='',
    height=1,
    width=1,
    length=1,
    weight=1,
    measurementUnit='')

```

**Modelo Product**

```python
hub_product = Product(
    name='',
    description='',
    active=True,
    mainImageURL='',
    productCode='',
    productEan='',
    skuErp='',
    storeId=HUB_STORE_ID,
    attributes=[],
    categories=[],
    productBrandId=0,
    storeProduct=store_product)
```

### **Vtex**

Importar todos modelos e controles

```python
from napplib.vtex.models.product import VtexProduct
from napplib.vtex.models.product import VtexSku
from napplib.vtex.models.product import VtexPrice
from napplib.vtex.models.product import VtexInventory
from napplib.vtex.models.product import VtexImage
from napplib.vtex.controller import VtexController
```

Variáveis necessárias para usar este controle

```python
vtex_store = ''
vtex_url = f'https://{vtex_store}.vtexcommercestable.com.br/api'
vtex_price_url = f'https://api.vtex.com/{vtex_store}/pricing'
vtex_app_key = ''
vtex_app_token = ''
```

Função do controle que cria todos objetos de produto na Vtex, será necessário criar os respectivos modelos

- product
- sku
- price
- inventory
- image

**Função**

```python

VtexController.create_products(
    base_url=vtex_url,
    base_url_price=vtex_price_url,
    app_key=vtex_app_key,
    app_token=vtex_app_token,
    products=vtex_product)
```

**Modelo Price**

```python
vtex_price = VtexPrice(
    listPrice=0,
    costPrice=0)
```

**Modelo Inventory**

```python
vtex_inventory = VtexInventory(quantity=0)
```

**Modelo Image**

```python
vtex_image = VtexImage(
    IsMain=True,
    Label='',
    Name='',
    Url='',
    Text='')
```

**Modelo SKU**

```python
vtex_sku = VtexSku(
IsActive=True,
Name='',
RefId='',
CreationDate='',
MeasurementUnit='',
price=vtex_price,
inventory=vtex_inventory,
images=vtex_image)
```

**Modelo Product**

```python
vtex_product = VtexProduct(
Name='',
CategoryId=0,
BrandId=0,
RefId='',
IsVisible=True,
Description='',
DescriptionShort='',
ReleaseDate='',
Title='',
IsActive=True,
skus=vtex_sku)
```

## **Desenvolvedor**

```
Napp Brain 🧠
leandro@nappsolutions.com
```