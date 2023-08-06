# azure-storage-blob==2.1.0
from azure.storage.blob import BlockBlobService
import datetime

class BlobStorage:
    @classmethod
    def list_all_blobs(self, account_name='', account_key='', path='', project='', store_name=''):
        # Azure configs
        block_blob_service = BlockBlobService(
            account_name=account_name, 
            account_key=account_key
        )

        # create blob base object
        generator = block_blob_service.list_blobs(path, prefix=f'{project}/{store_name}')
        blobs = []

        for blob in generator:
            blobs.append({'name': blob.name, 'raw_object': blob})
        
        # return list of all blobs
        return blobs

    @classmethod
    def get_blob(self, account_name='', account_key='', path='', blob_path='', custom_encoding='utf8'):
         # Azure configs
        block_blob_service = BlockBlobService(
            account_name=account_name, 
            account_key=account_key
        )

        # create blob base object
        generator = block_blob_service.list_blobs(path)

        # create blob content variable
        blob_content = None

        # loop in all blobs from this path
        for blob in generator:
            # check if blob_name is equals to target blob
            if blob_path == blob.name:
                blob_content = block_blob_service.get_blob_to_bytes(path, blob_path).content.decode(custom_encoding)

        # return content
        return blob_content


    @classmethod
    def get_latest_blob(self, account_name='', account_key='', path='', project='', store_name='', custom_encoding='utf8'):
        # Azure configs
        block_blob_service = BlockBlobService(
            account_name=account_name, 
            account_key=account_key
        )

        # create blob base object
        generator = block_blob_service.list_blobs(path)
        
        # date objects
        selected_last_modified = None
        selected_file_name = None
        selected_file_content = None
        
        # loop in all blob from generator
        for blob in generator:
            # get file name and last modified date
            file_name = blob.name

            # create a match name based on blob path ex: project/store
            split_path = file_name.split('/')
            match_name = f'{split_path[0]}/{split_path[1]}'
            
            # concat project and store name
            project_store = f'{project}/{store_name}'
            
            if project_store != match_name:
                continue
                
            file_last_modified = blob.properties.last_modified

            # if selected last modified date is not None
            if selected_last_modified:
                # check if selected file  date is greater than current loop file
                if selected_last_modified > file_last_modified:
                    # log
                    print(f'This file {selected_file_name} is newest... Skip: {file_name}')
                else:
                    # set dates with this loop file
                    selected_last_modified = file_last_modified
                    selected_file_name = file_name
            else:
                # set dates with this loop file
                selected_last_modified = file_last_modified
                selected_file_name = file_name
        
        # get blob content
        if selected_file_name:
            # get file content using custom encoding, default: uf-8
            selected_file_content = block_blob_service.get_blob_to_bytes(path, selected_file_name).content.decode(custom_encoding)
            
            # print
            print(f'Selected file: {selected_file_name}, File date: {selected_last_modified}')
        
            # return blob content
            return selected_file_content
        
        # log with no match files
        print(f'No files detected for this store {store_name}...')
        return None

    @classmethod
    def upload_blob(self, account_name='', account_key='', path='', project='', store_name='', output_file=''):
        # Azure config
        block_blob_service = BlockBlobService(
            account_name=account_name, 
            account_key=account_key
        )
        
        # create date pattern based on Year/Month/Day
        dt_str = datetime.datetime.now().strftime('%Y/%m/%d')
        year = dt_str.split('/')[0]
        month = dt_str.split('/')[1]
        day = dt_str.split('/')[2]

        # extract filename from full output file path
        filename = output_file.split('/')[-1]

        # create target folder to upload on azure blob storage. Ex: project/store/2020/01/01/sample.csv
        target = f'{project}/{store_name}/{year}/{month}/{day}/{filename}'

        # use azure blob service to upload
        try:
            block_blob_service.create_blob_from_path(path, target, output_file)
            print(f'Upload file {target} finished!')
        except Exception as e:
            print(f'Failed to upload file {target} on azure blob storage: {e}')