from directory_api_client.base import AbstractAPIClient

url_corruption_perceptions_index = 'dataservices/corruption-perceptions-index/{country_code}/'
url_ease_of_doing_business = 'dataservices/easeofdoingbusiness/{country_code}/'
url_last_year_import_data = 'dataservices/lastyearimportdata/'
url_historical_import_data = 'dataservices/historicalimportdata/'
url_world_economic_outlook_data = 'dataservices/world-economic-outlook/{country_code}/'
url_country_data_data = 'dataservices/country-data/{country}/'
url_cia_world_factbook_data = 'dataservices/cia-factbook-data/'
url_population_data = 'dataservices/population-data/'
url_population_data_by_country = 'dataservices/population-data-by-country/'
url_last_year_import_data_from_uk = 'dataservices/lastyearimportdatafromuk/'
url_suggested_countries = '/dataservices/suggested-countries/'


class DataServicesAPIClient(AbstractAPIClient):

    def get_corruption_perceptions_index(self, country_code):
        return self.get(
            url=url_corruption_perceptions_index.format(country_code=country_code),
            use_fallback_cache=True
        )

    def get_ease_of_doing_business(self, country_code):
        return self.get(
            url=url_ease_of_doing_business.format(country_code=country_code),
            use_fallback_cache=True,
        )

    def get_last_year_import_data(self, commodity_code, country):
        return self.get(
            url=url_last_year_import_data,
            params={'commodity_code': commodity_code, 'country': country}
        )

    def get_historical_import_data(self, commodity_code, country):
        return self.get(
            url=url_historical_import_data,
            params={'commodity_code': commodity_code, 'country': country}
        )

    def get_world_economic_outlook_data(self, country_code):
        return self.get(
            url=url_world_economic_outlook_data.format(country_code=country_code),
            use_fallback_cache=True
        )

    def get_country_data(self, country):
        return self.get(
            url=url_country_data_data.format(country=country),
            use_fallback_cache=True
        )

    def get_cia_world_factbook_data(self, country, data_key):
        return self.get(
            url=url_cia_world_factbook_data,
            params={'country': country, 'data_key': data_key},
            use_fallback_cache=True
        )

    def get_population_data(self, country, target_ages):
        return self.get(
            url=url_population_data,
            params={'country': country, 'target_ages': target_ages},
            use_fallback_cache=True
        )

    def get_population_data_by_country(self, countries: list):
        return self.get(
            url=url_population_data_by_country,
            params={'countries': countries},
            use_fallback_cache=True
        )

    def get_last_year_import_data_from_uk(self, commodity_code, countries):
        return self.get(
            url=url_last_year_import_data_from_uk,
            params={'commodity_code': commodity_code, 'countries': countries}
        )

    def suggested_countries_by_hs_code(
        self, hs_code
    ):
        return self.get(
            url=url_suggested_countries, params={'hs_code': hs_code, }
        )
