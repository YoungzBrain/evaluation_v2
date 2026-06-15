from pathlib import Path
import pdf2image

path = Path('Documentation.pdf')
images = pdf2image.convert_from_path(str(path), first_page=12, last_page=18, dpi=200)
for idx, img in enumerate(images, start=12):
    out = Path(f'page_{idx}.png')
    img.save(out)
    print('saved', out)
