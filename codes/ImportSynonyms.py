# 安装中文近义词库，详细信息见： https://github.com/chatopera/Synonyms
# 需要购买证书

import os
# 设置你的密钥
os.environ["SYNONYMS_DL_LICENSE"] = ""
_licenseid = os.environ.get("SYNONYMS_DL_LICENSE", None)
print("SYNONYMS_DL_LICENSE=", _licenseid)

# 测试
import synonyms
synonyms.display('能量')

# 预期结果:
# '能量'近义词：
#   1. 能量:1.0
#   2. 热量:0.78949404
#   3. 热能:0.771208
#   4. 势能:0.7690508
#   5. 高能量:0.7215006
#   6. 电荷:0.69755447
#   7. 光子:0.6749917
#   8. 电磁波:0.66329706
#   9. 潜热:0.6542588
#   10. 微粒:0.6540314