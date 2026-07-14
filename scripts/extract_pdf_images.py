#!/usr/bin/env python3
"""
Extract component art from a rulebook PDF into per-game image assets.

Born-digital rulebooks (InDesign/Illustrator exports) store their component art as
separate embedded image objects, often with an SMask carrying the alpha channel. Those
extract cleanly and individually. Scanned or fully flattened rulebooks do not -- they
hold one big raster per page and nothing useful underneath.

So this runs in two modes. Probe first, extract only if the probe says it's worth it:

    python3 scripts/extract_pdf_images.py --probe rulebook.pdf
    python3 scripts/extract_pdf_images.py --extract rulebook.pdf --game-id tenpenny_parks

Probe reports sprite count, how many carry transparency, and the median effective DPI
(pixels per inch as actually placed on the page -- the real ceiling on display quality).
A web-optimised rulebook is typically 72 DPI, which is fine for a thumbnail or a modest
hero image and nothing larger.

Extract writes lossless WebP to files/<game_id>/images/, machine-named by PDF object id
(x1234.webp). Those names are a starting point, not the deliverable: curate the keepers,
rename them semantically (carousel.webp, worker_arborist.webp), and commit only those.
Committing all ~130 raw sprites bloats the repo permanently -- git history is forever.

Requires: PyMuPDF (pip install pymupdf), Pillow.
"""

import argparse
import io
import statistics
import sys
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent

# A sprite smaller than this is a rule, a bullet, or a compression artifact. Keep this
# low: real components hide down here. A VP token is 32x32 and a tree marker 34x47, and
# a 50x50 floor silently swallowed every one of them.
MIN_PIXELS = 900  # 30x30
# Anything this large covering the page is the page background, not a component.
PAGE_BG_MIN_WIDTH = 500
PAGE_BG_MIN_HEIGHT = 700
# Below this, the art is too soft to display at any meaningful size.
USABLE_DPI = 50


def _sprites(doc):
    """Yields (xref, smask, width, height, effective_dpi) for each candidate sprite.

    Deduped by xref -- the same logo placed on ten pages is one image object, and we
    want it once. Page backgrounds and noise are filtered out here so probe and extract
    agree on what counts as a sprite.
    """
    seen = set()
    for page in doc:
        for img in page.get_images(full=True):
            xref, smask = img[0], img[1]
            if xref in seen:
                continue

            info = doc.extract_image(xref)
            width, height = info["width"], info["height"]
            if width * height < MIN_PIXELS:
                continue
            if width >= PAGE_BG_MIN_WIDTH and height >= PAGE_BG_MIN_HEIGHT:
                continue

            # Effective DPI depends on how big the art is *drawn*, not its pixel count:
            # a 200px sprite placed in a 1-inch box is 200 DPI; stretched across 4
            # inches it's 50. The placement rect is the only way to know.
            rects = page.get_image_rects(xref)
            if not rects or not rects[0].width:
                continue
            dpi = round(width / (rects[0].width / 72))

            seen.add(xref)
            yield xref, smask, width, height, dpi


def _flattened_pages(doc):
    """Pages that are a single full-page raster -- i.e. a scan, with no separable art."""
    count = 0
    for page in doc:
        images = page.get_images(full=True)
        if len(images) != 1:
            continue
        info = doc.extract_image(images[0][0])
        if info["width"] >= PAGE_BG_MIN_WIDTH and info["height"] >= PAGE_BG_MIN_HEIGHT:
            count += 1
    return count


def probe(pdf_path):
    """Report whether this PDF's art is worth extracting. Returns True if it is."""
    doc = fitz.open(pdf_path)
    found = list(_sprites(doc))
    flattened = _flattened_pages(doc)

    print(f"{Path(pdf_path).name}: {doc.page_count} pages")

    if not found:
        print("  sprites:      0")
        print()
        print("  VERDICT: no extractable art. The rulebook is scanned, flattened, or")
        print("  draws its art as vectors. Cut the art by hand (Figma) instead.")
        return False

    with_alpha = sum(1 for s in found if s[1])
    dpis = [s[4] for s in found]
    median_dpi = statistics.median(dpis)
    too_soft = sum(1 for d in dpis if d < USABLE_DPI)

    print(f"  sprites:      {len(found)}")
    print(f"  with alpha:   {with_alpha} ({with_alpha * 100 // len(found)}%)")
    print(f"  median DPI:   {median_dpi:.0f}")
    print(f"  flat pages:   {flattened}/{doc.page_count}")
    print()

    if flattened == doc.page_count:
        print("  VERDICT: every page is a single raster -- this is a scan. Cut by hand.")
        return False

    print(f"  VERDICT: extractable. {len(found) - too_soft} sprites are usable.")
    if median_dpi <= 96:
        print(f"  Note: {median_dpi:.0f} DPI is screen resolution. Good for thumbnails and")
        print("  modest hero images; it will not survive being displayed large.")
    if with_alpha < len(found) // 2:
        print("  Note: most sprites lack an alpha mask, so they'll carry their background.")
    return True


def extract(pdf_path, out_dir):
    """Write every usable sprite to out_dir as lossless WebP. Returns the count."""
    doc = fitz.open(pdf_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for xref, smask, _, _, dpi in _sprites(doc):
        if dpi < USABLE_DPI:
            continue

        pixmap = fitz.Pixmap(doc, xref)
        if smask:
            # The colour data and its transparency are two separate objects; extracting
            # the image alone gives you the art on a black box. Re-attaching the SMask
            # is what turns it back into a cutout.
            pixmap = fitz.Pixmap(pixmap, fitz.Pixmap(doc, smask))

        image = Image.open(io.BytesIO(pixmap.tobytes("png"))).convert("RGBA")
        # Lossless: these are flat-colour game icons, and lossy WebP smears their edges.
        image.save(out_dir / f"x{xref}.webp", "WEBP", lossless=True)
        written += 1

    return written


def compose(paths, out_path, gap=10):
    """Lay several sprites side by side on one transparent canvas.

    A component is often a *set* -- 1-VP and 5-VP tokens, a handful of tile shapes,
    three tree markers. Extracting one sprite of the set and calling it "VP Tokens"
    undersells it, but a card can only show one image. So group the set into a single
    image and let that be the component's art.

    Sprites keep their natural relative sizes (a 5-VP token really is the same size as
    a 1-VP token) and are centred on a common baseline.
    """
    images = [Image.open(p).convert("RGBA") for p in paths]
    width = sum(i.width for i in images) + gap * (len(images) - 1)
    height = max(i.height for i in images)

    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = 0
    for image in images:
        canvas.alpha_composite(image, (x, (height - image.height) // 2))
        x += image.width + gap

    canvas.save(out_path, "WEBP", lossless=True)
    return canvas.size


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--probe", metavar="PDF", help="report whether a PDF's art is extractable")
    parser.add_argument("--extract", metavar="PDF", help="extract a PDF's art")
    parser.add_argument("--compose", nargs="+", metavar="SPRITE",
                        help="group several sprites into one image (see --out)")
    parser.add_argument("--game-id", help="game id; art goes to files/<game-id>/images/")
    parser.add_argument("--out", help="output directory, or output file for --compose")
    args = parser.parse_args()

    if args.probe:
        return 0 if probe(args.probe) else 1

    if args.compose:
        if not args.out:
            parser.error("--compose needs --out <file.webp>")
        size = compose(args.compose, Path(args.out))
        print(f"composed {len(args.compose)} sprites -> {args.out} {size[0]}x{size[1]}")
        return 0

    if not args.extract:
        parser.error("pass --probe, --extract or --compose")
    if not args.out and not args.game_id:
        parser.error("--extract needs --game-id (or --out)")

    out_dir = Path(args.out) if args.out else REPO_ROOT / "files" / args.game_id / "images"
    written = extract(args.extract, out_dir)
    print(f"wrote {written} sprites to {out_dir}")
    print("Now curate: keep the ones you'll reference, rename them semantically, delete the rest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
