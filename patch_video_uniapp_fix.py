with open("iqiyi-uniappx/pages/video-detail/video-detail.uvue", "r") as f:
    content = f.read()

import re
print("Matching script additions:", re.search(r'onMounted', content))
