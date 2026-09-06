#!/usr/bin/env python3
import sys
import os
import argparse
from PIL import Image, ImageDraw

def make_rounded_icon(input_path, output_path=None, radius_ratio=0.22, size=512):
    if not os.path.exists(input_path):
        print(f'Error: file not found: {input_path}')
        return False

    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = f'{base}.png'

    im = Image.open(input_path).convert('RGBA')

    w, h = im.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    im = im.crop((left, top, left + min_dim, top + min_dim))
    im = im.resize((size, size), Image.Resampling.LANCZOS)

    scale = 4
    mask_size = size * scale
    radius = int(mask_size * radius_ratio)
    mask = Image.new('L', (mask_size, mask_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, mask_size, mask_size), radius=radius, fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)

    im.putalpha(mask)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    im.save(output_path, 'PNG', optimize=True)
    print(f'Successfully created rounded icon: {output_path}')
    return True

def main():
    parser = argparse.ArgumentParser(description='Convert images to phone-style rounded app icons.')
    parser.add_argument('input', nargs='?', help='Path to input image')
    parser.add_argument('-o', '--output', help='Path to output PNG')
    parser.add_argument('-r', '--radius', type=float, default=0.22, help='Corner radius ratio (default: 0.22)')
    parser.add_argument('-s', '--size', type=int, default=512, help='Output icon dimensions (default: 512)')
    parser.add_argument('--all', action='store_true', help='Process all jpg/jpeg files in icons/ directory')

    args = parser.parse_args()

    if args.all:
        icons_dir = 'icons'
        if not os.path.exists(icons_dir):
            print(f'Directory {icons_dir} not found.')
            sys.exit(1)
        for fname in os.listdir(icons_dir):
            if fname.lower().endswith(('.jpg', '.jpeg')):
                inp = os.path.join(icons_dir, fname)
                out = os.path.splitext(inp)[0] + '.png'
                make_rounded_icon(inp, out, radius_ratio=args.radius, size=args.size)
    elif args.input:
        make_rounded_icon(args.input, args.output, radius_ratio=args.radius, size=args.size)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
