from typing import Optional, Union
import requests
import hashlib

__version__ = '1.0'

class CatCutApi:
    def __init__(self,id: Union[int,str], secret_code: str) -> None:
        """__init__

        Args:
            id (Union[int,str]): id Api приложения
            secret_code (str): Секретный код приложения
        """
        if isinstance(id,int):
            self._id = str(id)
        else:
            self._id:str  = id.replace('#G','')
        self._secret_code = secret_code
        
        
    def get_ads_balance(self) -> Union[int,float]:
        """Возвращает баланс рекламного счёта.

        Returns:
            Union[int,float]: баланс
        """
        hash_str = self._id + 'getadsbalance' + self._secret_code
        sha_1 = hashlib.sha1(hash_str.encode())
        resp = requests.post('https://catcut.net/api/get.php',data={
            'id':self._id,
            'type':'getadsbalance',
            'hash':sha_1.hexdigest()
        })
        json = resp.json()
        return json['ads_balance']
    
    def create_cc_link(self,longurl: str,**kwargs) -> str:
        """Создает CatCut ссылку

        Args:
            longurl (str): Ссылка которую нужно сократить
            advsurfing (Optional[Union[str,int]]): Добавить рекламу в ссылку
            comment (Optional[str]): Примечание к ссылке
        
        Returns:
            str: Сокращенная ссылка(символы ссылки к которой нужно конкатенировать домен)
        """
        hash_str = longurl + self._id + kwargs.get('advsurfing','') + kwargs.get('comment','') + self._secret_code
        sha_1 = hashlib.sha1(hash_str.encode())
        kwargs['longurl'] = longurl
        kwargs['id'] = self._id
        kwargs['hash'] = sha_1.hexdigest()
        resp = requests.post('https://catcut.net/api/create.php',data=kwargs)
        return resp.text
    
    def get_cc_link_stat(self,shorturl: str) -> dict:
        """Получить статистику ссылки

        Args:
            shorturl (str): Ссылка либо символы ссылки

        Returns:
            dict: Json вида:
            ```
                url – символы короткой ссылки;
                longurl – ссылка, которая была сокращена;
                comment – текст заметки;
                createtime – дата создания ссылки в формате UNIX-времени;
                countclicks – количество переходов по ссылке;
                advsurfing – статус отображения рекламы; 0 – показ рекламы для ссылки выключен, 1 – показы рекламы для ссылки включён;
                money – сумма денег, которая была заработана на этой ссылке.
            ```
        """
        symbs = shorturl.split('/')[-1]
        hash_str = self._id + 'urlstat' + symbs + self._secret_code
        sha_1 = hashlib.sha1(hash_str.encode())
        resp = requests.post('https://catcut.net/api/get.php',data={
            'id':self._id,
            'type':'urlstat',
            'url':symbs,
            'hash':sha_1.hexdigest()
        })
        return resp.json()