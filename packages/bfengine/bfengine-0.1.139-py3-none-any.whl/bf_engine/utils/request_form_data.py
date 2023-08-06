# Generates request data payload to be sent as 'form-data'

class RequestFormData:
    REQUEST_FORM_DATA_BOUNDARY = "REQUEST_FORM_DATA_BOUNDARY"
    FORM_DATA_STARTING_PAYLOAD = '--{0}\r\nContent-Disposition: form-data; name=\\"'.format(REQUEST_FORM_DATA_BOUNDARY)
    FORM_DATA_MIDDLE_PAYLOAD = '\"\r\n\r\n'
    FORM_DATA_ENDING_PAYLOAD = '--{0}--'.format(REQUEST_FORM_DATA_BOUNDARY)
    REQUEST_CUSTOM_HEADER = {
        'content-type': "multipart/form-data; boundary={}".format(REQUEST_FORM_DATA_BOUNDARY),
        'Content-Type': "",
        'cache-control': "no-cache"
    }
    @classmethod
    def generate_form_data_payload(self,kwargs):
        payload = ''
        for key, value in kwargs.items():
            payload += '{0}{1}{2}{3}\r\n'.format(RequestFormData.FORM_DATA_STARTING_PAYLOAD, key, RequestFormData.FORM_DATA_MIDDLE_PAYLOAD, value)
        payload += RequestFormData.FORM_DATA_ENDING_PAYLOAD
        return payload