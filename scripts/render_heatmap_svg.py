import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_svg():
    with open("data/contributions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("total", 0)

    box_size = 11
    box_gap = 3
    offset_x = 30
    offset_y = 30

    width = offset_x + (53 * (box_size + box_gap)) + 20
    height = offset_y + (7 * (box_size + box_gap)) + 40

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <style>',
        '    .bg { fill: #0d1117; rx: 6px; }',
        '    .text { font-family: monospace; font-size: 11px; fill: #8b949e; }',
        '    .cell { transform-origin: center; animation: diagSlide 0.3s ease-out forwards; opacity: 0; }',
        '    @keyframes diagSlide {',
        '      from { opacity: 0; transform: translate(-10px, -10px); }',
        '      to { opacity: 1; transform: translate(0, 0); }',
        '    }',
        '  </style>',
        '  <rect width="100%" height="100%" class="bg" />',
        '  <g>'
    ]

    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        x = offset_x + col * (box_size + box_gap)
        y = offset_y + row * (box_size + box_gap)
        
        color = PALETTE[min(day["level"], 5)]
        delay = round((col + row) * 0.015, 3)

        svg_lines.append(
            f'    <rect class="cell" x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
            f'rx="2" fill="{color}" style="animation-delay: {delay}s;" />'
        )

    footer_text = f"{total:,} contributions in the last year"
    svg_lines.append(f'  <text x="{offset_x}" y="{height - 15}" class="text">{footer_text}</text>')
    
    legend_x = width - 120
    svg_lines.append(f'  <text x="{legend_x - 30}" y="{height - 15}" class="text">Less</text>')
    for i, p_color in enumerate(PALETTE):
        lx = legend_x + i * (box_size + 2)
        ly = height - 24
        svg_lines.append(f'  <rect x="{lx}" y="{ly}" width="{box_size}" height="{box_size}" rx="2" fill="{p_color}" />')
    svg_lines.append(f'  <text x="{legend_x + len(PALETTE)*(box_size+2) + 5}" y="{height - 15}" class="text">More</text>')

    svg_lines.append('</svg>')

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print("Heatmap SVG rendered to contrib-heatmap.svg")

if __name__ == "__main__":
    render_svg()