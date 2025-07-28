import fitz  
import json
import os
from collections import Counter

def get_baseline_style(doc):
    font_counts = Counter()
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        style = (round(span["size"]), span["font"])
                        font_counts[style] += 1

    if not font_counts:
        return 12.0, "Helvetica"
    (baseline_size, baseline_font), _ = font_counts.most_common(1)[0]
    return float(baseline_size), baseline_font

def classify_span(span, baseline_size, title_size, full_text, page_width):
    """
    Improved classifier: uses font size, boldness, ALL CAPS, short length, and center position.
    """
    size = round(span["size"])
    font_name = span["font"].lower()
    is_bold = "bold" in font_name
    is_all_caps = full_text.isupper()
    is_short = len(full_text.split()) <= 8
    x0 = span["bbox"][0]
    x1 = span["bbox"][2]
    span_center = (x0 + x1) / 2
    is_centered = abs(span_center - page_width/2) < page_width * 0.15 

   
    if size == title_size:
        return "Title"

    score = 0
    if size > baseline_size * 1.8: score += 2
    elif size > baseline_size * 1.3: score += 1
    if is_bold: score += 1
    if is_all_caps: score += 1
    if is_short: score += 1
    if is_centered: score += 1

    if score >= 4:
        return "H1"
    elif score == 3:
        return "H2"
    elif score == 2:
        return "H3"
    else:
        return "P"

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title_text = ""
    title_size = 0

    if len(doc) > 0:
        first_page = doc.load_page(0)
        blocks = first_page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] > title_size:
                            title_size = round(span["size"])
                            title_text = span["text"]

    baseline_size, baseline_font = get_baseline_style(doc)
    outline = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_width = page.rect.width 
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    if line["spans"]:
                        full_text = "".join([s["text"] for s in line["spans"]]).strip()
                        if not full_text:
                            continue
                        first_span = line["spans"][0]
                        level = classify_span(first_span, baseline_size, title_size, full_text, page_width)
                        if level in ["H1", "H2", "H3"]:
                            outline.append({
                                "level": level,
                                "text": full_text,
                                "page": page_num + 1
                            })

    doc.close()
    return {"title": title_text.strip(), "outline": outline}

def main():
    input_dir = "input"
    output_dir = "output"

    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Created directory '{input_dir}'. Please place your PDF files inside and run again.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            try:
                document_structure = extract_outline(pdf_path)
                base_name = os.path.splitext(filename)[0]
                json_filename = base_name + ".json"
                json_path = os.path.join(output_dir, json_filename)

                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(document_structure, f, indent=4, ensure_ascii=False)

                print(f"Successfully processed {filename} -> {json_filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
