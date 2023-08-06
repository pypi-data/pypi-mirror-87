import datetime

class Utils:
    @classmethod
    def create_values(self, value, tp):
        """
        Foi criado essa funcao devido a estrutura do nosso hub, em alguns casos temos que passar da seguinte forma:
        {'field': {'String': 'value', 'Valid': True}}
        Essa funcao cria o par de chaves e atribui seus tipos para ser atribuido no body de maneira correta.
        """
        pairKey = dict()  
        if tp == 'String':
            pairKey[tp] = str(value) if value != '' and value != None else ''
        elif tp == 'Int32':
            pairKey[tp] = int(value) if value != '' and value != None else ''
        elif tp == 'Int64':
            pairKey[tp] = int(value) if value != '' and value != None else ''
        elif tp == 'Float64':
            pairKey[tp] = float(value) if value != '' and value != None else ''  
        elif tp == 'Boolean':
            pairKey[tp] = bool(value) if value != '' and value != None else ''  
        pairKey['Valid'] = True if value != '' and value != None else False  
        return pairKey
    
    @classmethod
    def normalize_datetime(self, date):
        new_dt = date
        if new_dt and new_dt != '':
            if len(new_dt) > 25:
                # Eg: 2020-10-14T14:24:57.789000
                new_dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
                new_dt = new_dt.strftime('%d/%m/%Y %H:%M:%S')
            elif len(new_dt) == 25:
                # 2015-01-09T22:00:00-02:00
                new_dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
                new_dt = new_dt.strftime('%d/%m/%Y %H:%M:%S')
            elif len(new_dt) == 10:
                # 1995-01-01
                try:
                    new_dt = datetime.datetime.strptime(date, '%Y-%m-%d')
                    new_dt = new_dt.strftime('%d/%m/%Y')
                except:
                    new_dt = datetime.datetime.strptime(date, '%d-%m-%Y')
                    new_dt = new_dt.strftime('%d/%m/%Y')
        return new_dt