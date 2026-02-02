from PIL import Image

def transpose_blocks(input_path, output_path, block_w, block_h):
    img = Image.open(input_path).convert("RGB")
    W, H = img.size

    n_cols = W // block_w
    n_rows = H // block_h

    img = img.crop((0, 0, n_cols * block_w, n_rows * block_h))

    blocks = []
    for y in range(n_rows):
        row = []
        for x in range(n_cols):
            box = (
                x * block_w,
                y * block_h,
                (x + 1) * block_w,
                (y + 1) * block_h
            )
            row.append(img.crop(box))
        blocks.append(row)

    blocks_T = list(map(list, zip(*blocks)))

    out_img = Image.new(
        "RGB",
        (n_rows * block_w, n_cols * block_h)
    )

    for i, row in enumerate(blocks_T):
        for j, block in enumerate(row):
            out_img.paste(block, (j * block_w, i * block_h))

    MAX_SIZE = 1200

    w, h = out_img.size
    scale = min(MAX_SIZE / w, MAX_SIZE / h, 1)

    new_w = int(w * scale)
    new_h = int(h * scale)

    out_img = out_img.resize((new_w, new_h), Image.LANCZOS)
    
    out_img.save(output_path)
