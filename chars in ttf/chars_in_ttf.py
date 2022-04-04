import sys
from tqdm import tqdm
from pathlib import Path
from fontTools.ttLib import TTFont

def main():
	root_dir = sys.argv[1]
	print(root_dir)
	ttffiles = sorted(Path(root_dir).rglob("*.ttf"))
	for ttffile in tqdm(ttffiles):
		ttf = TTFont(ttffile)
		if ttffile.name[-3]=="T":
			txtfile = Path(str(ttffile).replace(".TTF", ".txt"))
		if ttffile.name[-3]=="t":
			txtfile = Path(str(ttffile).replace(".ttf", ".txt"))
		chars = [chr(y) for y in ttf['cmap'].tables[0].ttFont.getBestCmap()]
		chars_final=[]
		for i in chars:
			if (i!=" " and i!="\r"):
				chars_final.append(i)
		with open(txtfile, "w", encoding='utf-8') as f:
			f.write("".join(chars_final))
if __name__ == "__main__":
    main()