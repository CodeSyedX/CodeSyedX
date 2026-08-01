import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@"

def image_to_ascii(image_path, width=100):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load {image_path}")
    
    aspect_ratio = img.shape[0] / img.shape[1]
    height = int(width * aspect_ratio * 0.55)
    
    resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    
    ascii_grid = []
    for row in resized:
        ascii_row = []
        for val in row:
            idx = int((val / 255.0) * (len(RAMP) - 1))
            ascii_row.append(RAMP[idx])
        ascii_grid.append("".join(ascii_row))
    return ascii_grid

def generate_svg(ascii_grid, output_svg="avi-ascii.svg"):
    rows = len(ascii_grid)
    cols = len(ascii_grid[0]) if rows > 0 else 0
    
    char_w, char_h = 7, 12
    svg_width = cols * char_w + 20
    svg_height = rows * char_h + 20
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        '  <style>',
        '    .bg { fill: #0d1117; }',
        '    .ascii-text { font-family: "Courier New", Courier, monospace; font-size: 11px; fill: #8b949e; font-weight: bold; white-space: pre; }',
        '  </style>',
        '  <defs>',
    ]
    
    duration = 0.04
    for i in range(rows):
        begin_delay = round(i * duration, 2)
        svg_lines.append(f'    <clipPath id="clip-{i}">')
        svg_lines.append(f'      <rect x="0" y="{10 + i * char_h}" width="0" height="{char_h}">')
        svg_lines.append(f'        <animate attributeName="width" from="0" to="{svg_width}" dur="{duration}s" begin="{begin_delay}s" fill="freeze" />')
        svg_lines.append('      </rect>')
        svg_lines.append('    </clipPath>')
        
    svg_lines.extend([
        '  </defs>',
        '  <rect width="100%" height="100%" class="bg" rx="6" />',
        '  <g class="ascii-text">'
    ])
    
    for i, line in enumerate(ascii_grid):
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        y_pos = 20 + i * char_h
        svg_lines.append(f'    <text x="10" y="{y_pos}" clip-path="url(#clip-{i})">{escaped_line}</text>')
        
    svg_lines.append('  </g>')
    svg_lines.append('</svg>')
    
    with open(output_svg, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg_lines))
    print(f"ASCII SVG generated at {output_svg}")

if __name__ == "__main__":
    grid = image_to_ascii("source-prepped.png")
    generate_svg(grid)