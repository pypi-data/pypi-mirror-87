import json
import asyncio
import aiohttp


class ProfitExtractAsync:
    def __init__(self, environment: str, base64token: str, base_url: str = 'rest.afas.online'):
        self.environment = environment
        self.base_url = base_url
        self.base64token = base64token
        self.got_all_results = False

    async def get_data_content(self, connector: str, parameters: dict, batch_size: int = 8, take: int = 40000) -> json:
        """
        This (asynchronous) function functions as a wrapper that can carry out multiple single get requests to be able
        to get all data from profit in an asynchronous and efficient way. Note that this function cannot be called in itself,
        but has to be called via a synchronous function.

        :param connector: Name of the connector to be extracted.
        :param fields: list of filters. each listitem is one filterblock. example: ['naam, woonplaats', 'achternaam, einddatum']
        :param values: list of filters. each listitem corresponds to one filterblock. example: ['Jan, Gouda', 'Janssen, 2019-01-01T00:00']
        :param operators: list of filters. each listitem corresponds to one filterblock. example: ['1, 1', '1, 3']
        :param orderbyfields: string of fields to order result by
        :return: data in json format
        """
        url = f'https://{self.environment}.{self.base_url}/profitrestservices/connectors/{connector}'
        authorization_header = {'Authorization': 'AfasToken {}'.format(self.base64token)}
        batch_number = 0

        total_response = []
        self.got_all_results = False
        while not self.got_all_results:
            async with aiohttp.ClientSession(headers=authorization_header) as session:
                requests = [self.simple_get_request(url=url,
                                                    params={**parameters, **{
                                                        "skip": take * (i + batch_number * batch_size),
                                                        "take": take}},
                                                    session=session,
                                                    take=take) for i in range(batch_size)]
                response = await asyncio.gather(*requests)
                total_response += response

                batch_number += 1

        return total_response

    async def simple_get_request(self, url: str, params: dict, session: aiohttp.ClientSession, take: int) -> json:
        """
        This function carries out a single get request given the inputs. It is used as input for the abovementioned wrapper,
        get_data_content. Note that this function cannot be called it itself, but has to be started via get_data_content.

        :param url: profit url to retrieve the data.
        :param params: body of the request.
        :param session: type of the request.
        :return: data in json format
        """
        async with session.get(url=url, params=params) as resp:
            if resp.status == 200:
                response = await resp.json()
            else:
                print(resp)
                print(f"request to AFAS failed with response: {resp.text()}")
            if len(response['rows']) < take:
                print(f"request with params: {params} was the last request with {len(response['rows'])} rows")
                self.got_all_results = True
            else:
                print(f"request with params: {params} has {len(response['rows'])} rows")
            return response['rows']
