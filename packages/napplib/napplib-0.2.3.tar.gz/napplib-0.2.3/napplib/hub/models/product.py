import sys, datetime
sys.path.append("..") 
from ..utils import Utils

class PackageDimensions:
    def __init__(self, height='', 
                        width='', 
                        length='', 
                        weigth=''):
        self.height = height
        self.width = width
        self.length = length
        self.weight = weigth

class ProductCategorie:
    def __init__(self, id='',
                        name='', 
                        parentCategoryId='', 
                        parentCategory=''):
        self.id = id
        self.name = name
        self.parentCategoryId = parentCategoryId
        self.parentCategory = parentCategory

class Product:
    def __init__(self,  id='',
                        parentId='',
                        productBrandId='',
                        productBrandName='',
                        skuErp='',
                        name='',
                        description='',
                        NBMOrigin='',
                        cest='',
                        warrantyTime='',
                        active='',
                        codeNCM='',
                        codeISBN='',
                        variation='',
                        mainImageURL='',
                        urlImages='',
                        createdAt='',
                        updatedAt='',
                        productCode='',
                        productEan='',
                        storeId='',
                        storeProduct='',
                        attributes=[],
                        categories=[]):
        self.id = id if id else None
        self.parentId = Utils.create_values(parentId, 'Int64') if parentId else None
        self.productBrandId = Utils.create_values(productBrandId, 'Int64') if productBrandId else None
        self.productBrandName = Utils.create_values(productBrandName, 'String')
        self.skuErp = skuErp
        self.name = name
        self.description = description
        self.NBMOrigin = Utils.create_values(NBMOrigin, 'Int64') if NBMOrigin else None
        self.cest = Utils.create_values(cest, 'String') 
        self.warrantyTime = Utils.create_values(warrantyTime, 'Int64') if warrantyTime else None
        self.active = active
        self.codeNCM = Utils.create_values(codeNCM, 'String') if codeNCM else None
        self.codeISBN = Utils.create_values(codeISBN, 'String') if codeISBN else None
        self.variation = Utils.create_values(variation, 'String') if variation else None
        self.mainImageURL = Utils.create_values(mainImageURL, 'String') if mainImageURL else None
        self.urlImages = Utils.create_values(urlImages, 'String') if urlImages else None
        self.createdAt = Utils.create_values(createdAt, 'String') if createdAt else None
        self.updatedAt = Utils.create_values(updatedAt, 'String') if updatedAt else None
        self.productCode = Utils.create_values(productCode, 'String')
        self.productEan = Utils.create_values(productEan, 'String')
        self.storeId = Utils.create_values(storeId, 'Int64') if storeId else None
        self.storeProduct = storeProduct
        self.attributes = attributes
        self.categories = categories

class StoreProduct:
    def __init__(self, id='',
                        storeId='',
                        productId='',
                        productCode='',
                        productEan='',
                        erpCode='',                      
                        stockQuantity='',
                        listPrice='',
                        salePrice='',
                        active='',
                        measurementUnit='',
                        createdAt='',
                        updatedAt='',
                        height='',
                        width='',
                        length='',
                        weight='',
                        packageDimensions=''):
        self.id = id if id else None
        self.storeId = storeId
        self.productId = Utils.create_values(productId, 'Int64')
        self.productCode = Utils.create_values(productCode, 'String')
        self.productEan = Utils.create_values(productEan, 'String')
        self.erpCode = erpCode if erpCode else None
        self.stockQuantity = stockQuantity if stockQuantity else 0 
        self.listPrice = listPrice if listPrice else 0
        self.salePrice = salePrice if salePrice else 0 
        self.active = active if active else False
        self.measurementUnit = Utils.create_values(measurementUnit, 'String')
        self.createdAt = Utils.create_values(createdAt, 'String')
        self.updatedAt = Utils.create_values(updatedAt, 'String')
        self.height = Utils.create_values(height, 'Float64')
        self.width = Utils.create_values(width, 'Float64')
        self.length = Utils.create_values(length, 'Float64')
        self.weight = Utils.create_values(weight, 'Float64')
        self.packageDimensions = Utils.create_values(packageDimensions, 'String')

class StoreProductMarketplace:
    def __init__(self, id='',
                        marketplaceId='',
                        storeProductId='',
                        marketplaceForeignId='',
                        active='',
                        listPrice='',
                        salePrice='',
                        updatedAt=''):
        self.id = id if id else None
        self.marketplaceId = marketplaceId
        self.storeProductId = storeProductId
        self.marketplaceForeignId = Utils.create_values(marketplaceForeignId, 'String') if marketplaceForeignId else None
        self.active = active if active else False
        self.listPrice = Utils.create_values(listPrice, 'Float64')
        self.salePrice = Utils.create_values(salePrice, 'Float64')
        self.updatedAt = Utils.create_values(updatedAt, 'String')


        
        