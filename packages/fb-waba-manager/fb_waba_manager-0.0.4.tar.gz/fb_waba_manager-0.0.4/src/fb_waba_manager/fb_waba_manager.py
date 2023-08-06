from .services.facebook.whatsapp.waba_service import WabaService


class FbWabaManager:

    def __init__(self, access_token, business_id):
        self.access_token = access_token
        self.business_id = business_id
        self.waba_service = WabaService(access_token)

    def list_business_wabas(self):
        return self.waba_service.list_wabas(self.business_id)

    def list_waba_phone_numbers(self, waba_id):
        return self.waba_service.list_phone_numbers(waba_id)

    def list_business_phone_numbers(self, wabas=None):
        return self.waba_service.list_business_phone_numbers(self.business_id, wabas)

    def list_message_templates(self, waba_id):
        return self.waba_service.list_message_templates(waba_id)
