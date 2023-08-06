from directory_client_core.authentication import SessionSSOAuthenticator
from directory_api_client.base import AbstractAPIClient


url_exportplan_create = '/exportplan/company-export-plan/'
url_exportplan_update = '/exportplan/company-export-plan/{pk}/'
url_exportplan_detail = '/exportplan/company-export-plan/{pk}/'
url_exportplan_list = '/exportplan/company-export-plan/'

url_exportplan_objectives_create = '/exportplan/company-objectives/'
url_exportplan_objectives_update = '/exportplan/company-objectives/{pk}/'
url_exportplan_objectives_detail = '/exportplan/company-objectives/{pk}/'
url_exportplan_objectives_list = '/exportplan/company-objectives/'


url_route_to_market_create = '/exportplan/route-to-markets/'
url_route_to_market_update = '/exportplan/route-to-markets/{pk}/'
url_route_to_market_detail = '/exportplan/route-to-markets/{pk}/'
url_route_to_market_list = '/exportplan/route-to-markets/'

url_target_market_documents_create = '/exportplan/target-market-documents/'
url_target_market_documents_update = '/exportplan/target-market-documents/{pk}/'
url_target_market_documents_detail = '/exportplan/target-market-documents/{pk}/'
url_target_market_documents_list = '/exportplan/target-market-documents/'


class ExportPlanAPIClient(AbstractAPIClient):
    authenticator = SessionSSOAuthenticator

    def exportplan_update(self, sso_session_id, id, data):
        return self.patch(
            url=url_exportplan_update.format(pk=id), data=data, authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_detail(self, sso_session_id, id):
        return self.get(
            url=url_exportplan_detail.format(pk=id),
            use_fallback_cache=True,
            authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_create(self, sso_session_id, data):
        return self.post(url=url_exportplan_create, data=data, authenticator=self.authenticator(sso_session_id))

    def exportplan_list(self, sso_session_id):
        return self.get(url=url_exportplan_list, authenticator=self.authenticator(sso_session_id))

    def exportplan_objectives_update(self, sso_session_id, id, data):
        return self.patch(
            url=url_exportplan_objectives_update.format(pk=id),
            data=data,
            authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_objectives_delete(self, sso_session_id, id):
        return self.delete(
            url=url_exportplan_objectives_update.format(pk=id),
            authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_objectives_detail(self, sso_session_id, id):
        return self.get(
            url=url_exportplan_objectives_detail.format(pk=id),
            use_fallback_cache=True,
            authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_objectives_create(self, sso_session_id, data):
        return self.post(
            url=url_exportplan_objectives_create,
            data=data,
            authenticator=self.authenticator(sso_session_id)
        )

    def exportplan_objectives_list(self, sso_session_id):
        return self.get(url=url_exportplan_objectives_list, authenticator=self.authenticator(sso_session_id))

    def route_to_market_update(self, sso_session_id, id, data):
        return self.patch(
            url=url_route_to_market_update.format(pk=id),
            data=data,
            authenticator=self.authenticator(sso_session_id)
        )

    def route_to_market_delete(self, sso_session_id, id):
        return self.delete(
            url=url_route_to_market_update.format(pk=id),
            authenticator=self.authenticator(sso_session_id)
        )

    def route_to_market_detail(self, sso_session_id, id):
        return self.get(
            url=url_route_to_market_detail.format(pk=id),
            use_fallback_cache=True,
            authenticator=self.authenticator(sso_session_id)
        )

    def route_to_market_create(self, sso_session_id, data):
        return self.post(
            url=url_route_to_market_create,
            data=data,
            authenticator=self.authenticator(sso_session_id)
        )

    def route_to_market_list(self, sso_session_id):
        return self.get(url=url_route_to_market_list, authenticator=self.authenticator(sso_session_id))

    def target_market_documents_update(self, sso_session_id, id, data):
        return self.patch(
            url=url_target_market_documents_update.format(pk=id),
            data=data,
            authenticator=self.authenticator(sso_session_id)
        )

    def target_market_documents_delete(self, sso_session_id, id):
        return self.delete(
            url=url_target_market_documents_update.format(pk=id),
            authenticator=self.authenticator(sso_session_id)
        )

    def target_market_documents_detail(self, sso_session_id, id):
        return self.get(
            url=url_target_market_documents_detail.format(pk=id),
            use_fallback_cache=True,
            authenticator=self.authenticator(sso_session_id)
        )

    def target_market_documents_create(self, sso_session_id, data):
        return self.post(
            url=url_target_market_documents_create,
            data=data,
            authenticator=self.authenticator(sso_session_id)
        )

    def target_market_documents_list(self, sso_session_id):
        return self.get(url=url_target_market_documents_list, authenticator=self.authenticator(sso_session_id))
