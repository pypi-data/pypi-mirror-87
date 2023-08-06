import base64

from flask import current_app


class ImageApi:
    @classmethod
    def build_url(cls, url_orig, w=None, h=None, download=False, extension='jpg'):
        """
        Returns a formatted URL to the Image API service
        :param url_orig: String, full URL to Dash Hudson image
            e.g. https://dashhudson-dev.s3.amazonaws.com/images/items/1532976128.41429521549.jpeg
        :param w: Int, requested width
        :param h: Int, requested height
        :param download: Bool, flag that's sent to the image API to receive a download header,
            default False
        :param extension: String, image file extension, default 'jpg'
        """
        host = current_app.config['DH_POTLUCK_IMAGE_API_URL']

        url = url_orig.encode('utf-8')
        url_bytes = base64.urlsafe_b64encode(url)
        encoded_path = str(url_bytes, 'utf-8')

        params = []
        if w is not None:
            params.append(f'w={w}')
        if h is not None:
            params.append(f'h={h}')
        if download:
            params.append('download=true')

        param_string = f'?{"&".join(params)}' if len(params) > 0 else ''

        return f'{host}/{encoded_path}.{extension}{param_string}'
