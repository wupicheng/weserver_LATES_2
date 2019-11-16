import base64
import os
import mimetypes

relative_path='/mdeditor/fonts/fontawesome-webfont.woff2?v=4.3.0'
type=mimetypes.guess_type(relative_path)[0]#根据路径的扩展名确定 content-type
print(type)