
from lib.mimetypes import MimeTypes

mimetypes=MimeTypes()
# mimetypes.add_type()
relative_path="/mdeditor/fonts/editormd-logo.woff?-5y8q6h"
a=mimetypes.guess_type(relative_path)
print(a[0])