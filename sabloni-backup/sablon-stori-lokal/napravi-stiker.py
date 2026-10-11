# Pravi stiker (izrez jela + bela ivica) iz slike posta.
# Upotreba: python3 napravi-stiker.py <ulazna-slika> sticker.png
# Potrebno: pip install --break-system-packages "rembg[cpu]" pillow
import sys
from rembg import remove, new_session
from PIL import Image, ImageFilter
src, out = sys.argv[1], sys.argv[2]
im = remove(Image.open(src).convert('RGB'), session=new_session('isnet-general-use')).convert('RGBA')
a = im.split()[3].point(lambda v: 0 if v < 40 else v); im.putalpha(a); im = im.crop(a.getbbox())
pad = 40; W, H = im.size
base = Image.new('RGBA', (W + 2*pad, H + 2*pad), (0, 0, 0, 0)); base.paste(im, (pad, pad), im)
al = base.split()[3].point(lambda v: 255 if v > 100 else 0)
border = al.filter(ImageFilter.MaxFilter(29)).filter(ImageFilter.GaussianBlur(1.2))
white = Image.new('RGBA', base.size, (255, 255, 255, 255)); white.putalpha(border)
white.alpha_composite(base); white.save(out); print(out, white.size)
