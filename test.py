from word_cloud_video import wcv,wc
import jieba
import random
from word_cloud_video.style import gen_stylecloud

# gen_fa_mask('fa-solid fa-cube')


txt = '''我国北京地区的教育资源更是让许多四五线城市表示十分羡慕，在北京地区所享受到的教学资源基本上都是来自于一线超前发达，城市结合经济发展模式，教学资源，全国政治文化发展方面，科技创新中心等各个方面学生提供德智体美劳素质文化教育体系，云集我国最顶尖的教学资源。'''

    
cloud = wc.WC(font_path=r'QianTuXiaoTuTi-2.ttf', max_font_size=30)
cloud.generate_from_text(txt)
# image = cloud.to_image()
# image.show()
svg = cloud.to_svg()
with open('img.svg', 'w', encoding='utf8') as f:
    f.write(svg)
# gen_stylecloud(txt*3, 
#                size=512,
#                icon_name='fas fa-cube',
#                background_color='black',
#                prefer_horizontal=0.5,
#                font_path=r'QianTuXiaoTuTi-2.ttf', 
#                max_font_size=50, 
#                gradient='horizontal', 
#                palette='colorbrewer.diverging.Spectral_11',)