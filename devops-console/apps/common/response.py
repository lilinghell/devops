from django.utils import six
from rest_framework import status
from rest_framework.compat import SHORT_SEPARATORS, LONG_SEPARATORS, INDENT_SEPARATORS
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json


class APIRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            'code': 'AAAAAAA',
            'msg': '成功',
            'data': {},
        }
        response = renderer_context['response']

        if data is None:
            ret = json.dumps(response_dict)
        else:
            renderer_context = renderer_context or {}
            indent = self.get_indent(accepted_media_type, renderer_context)

            if indent is None:
                separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
            else:
                separators = INDENT_SEPARATORS

            if isinstance(data, dict):
                if data.get('response_code'):
                    response_dict['code'] = data.get('response_code')
                if data.get('response_msg'):
                    response_dict['msg'] = data.get('response_msg')
                else:
                    if response.status_code == status.HTTP_400_BAD_REQUEST:
                        msg = ""
                        for i in data:
                            if i != "response_code":
                                detail = data[i]
                                if isinstance(detail, str):
                                    msg = msg + i + ":" + detail + " "
                                else:
                                    msg = msg + i + ":" + detail[0] + " "
                        response_dict['msg'] = msg
                    else:
                        response_dict['msg'] = data

            if response_dict['code'] == "AAAAAAA":
                response_dict['data'] = data
                response_dict['msg'] = "成功"

            ret = json.dumps(
                response_dict, cls=self.encoder_class,
                indent=indent, ensure_ascii=self.ensure_ascii,
                allow_nan=not self.strict, separators=separators
            )
        response.status_code = status.HTTP_200_OK
        if isinstance(ret, six.text_type):
            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
            return bytes(ret.encode('utf-8'))
        return ret
