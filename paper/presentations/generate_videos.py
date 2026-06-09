"""
Generate an mp4 loop video illustrating how the Ebbinghaus illusion parameters
(illusion_strength and difference) affect the image.

The video follows a continuous smooth sequence:
  1. Difference: 0 -> negative max -> positive max
  2. Illusion strength: 0 -> positive max -> negative max
  3. Difference -> 0
  4. Illusion strength -> 0
"""

import os
import sys

# Ensure the project root is on sys.path so pyllusion can be imported
# regardless of the working directory from which the script is invoked.
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(os.path.dirname(_HERE))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import imageio
import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

import pyllusion


# ── Video settings ─────────────────────────────────────────────────────────────
FPS = 24
WIDTH = 800
HEIGHT = 544  # divisible by 16 for codec compatibility
OUTPUT = "ebbinghaus_parameters.mp4"

# ── Layout constants ────────────────────────────────────────────────────────
LEFT_BAR = 100  # width of vertical illusion_strength slider strip
TOP_BAR  = 50   # height of title strip
BOT_BAR  = 90   # height of bottom info strip


# ── Helpers ────────────────────────────────────────────────────────────────────

def _get_font(size, bold=False):
    """Load a TrueType font, falling back to the PIL default."""
    names = ["arialbd.ttf", "C:/Windows/Fonts/arialbd.ttf"] if bold \
            else ["arial.ttf",   "C:/Windows/Fonts/arial.ttf"]
    for name in names:
        try:
            return PIL.ImageFont.truetype(name, size)
        except OSError:
            pass
    return PIL.ImageFont.load_default()


def _add_labels(img: PIL.Image.Image, strength: float, difference: float) -> PIL.Image.Image:
    """Overlay all UI chrome (title, sliders, labels) onto the canvas."""

    draw = PIL.ImageDraw.Draw(img)

    # ── "Ebbinghaus" centred bold title ─────────────────────────────────────
    font_title = _get_font(28, bold=True)
    bbox = draw.textbbox((0, 0), "Ebbinghaus", font=font_title)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((img.width - tw) // 2, (TOP_BAR - th) // 2),
              "Ebbinghaus", fill="black", font=font_title)

    # ── Shared Slider Properties ─────────────────────────────────────────────
    TRACK_W = 6                     # half-thickness (12px total thickness)
    TRACK_BG = (220, 220, 220)      # grey empty track
    ILL_TRACK_FG = (100, 150, 200)  # blue filled track (strength)
    ILL_DOT_FG = (80, 130, 220)     # blue dot color (strength)
    DIFF_TRACK_FG = (220, 80, 80)   # red filled track (difference)
    DIFF_DOT_FG = (220, 50, 50)     # red dot color (difference)
    DOT_R = 8                       # dot radius
    font_slider_title = _get_font(18, bold=True)

    # ── 1. Left Vertical Slider (Illusion Strength) ──────────────────────────
    SX    = 70
    S_TOP = TOP_BAR + 20
    S_BOT = img.height - BOT_BAR - 20
    track_h = S_BOT - S_TOP
    zero_y  = (S_TOP + S_BOT) // 2

    # track and zero-tick
    draw.rectangle([(SX - TRACK_W, S_TOP), (SX + TRACK_W, S_BOT)], fill=TRACK_BG)
    draw.line([(SX - TRACK_W - 4, zero_y), (SX + TRACK_W + 4, zero_y)], fill=(160, 160, 160), width=2)

    # calculate position and draw fill/dot
    norm_str = float(np.clip(strength / 2.0, -1.0, 1.0))
    cursor_y = int(S_BOT - (norm_str + 1.0) / 2.0 * track_h)
    
    y0, y1 = min(zero_y, cursor_y), max(zero_y, cursor_y)
    draw.rectangle([(SX - TRACK_W, y0), (SX + TRACK_W, y1)], fill=ILL_TRACK_FG)
    draw.ellipse([(SX - DOT_R, cursor_y - DOT_R), (SX + DOT_R, cursor_y + DOT_R)], fill=ILL_DOT_FG, outline="white", width=2)

    # Vertical Title (Illusion Strength)
    lb = draw.textbbox((0, 0), "Illusion Strength", font=font_slider_title)
    lw, lh = lb[2] - lb[0], lb[3] - lb[1]
    lbl_surf = PIL.Image.new("RGBA", (lw + 4, lh + 4), (255, 255, 255, 0))
    PIL.ImageDraw.Draw(lbl_surf).text((2, 2), "Illusion Strength", fill="black", font=font_slider_title)
    lbl_rot = lbl_surf.rotate(90, expand=True)
    
    # Paste centered vertically on the left
    img.paste(lbl_rot, (20, (S_TOP + S_BOT) // 2 - lbl_rot.height // 2), lbl_rot)
    draw = PIL.ImageDraw.Draw(img)  # refresh draw context after paste


    # ── 2. Bottom Horizontal Slider (Difference Size) ────────────────────────
    SY = img.height - 65
    S_LEFT = LEFT_BAR + 20
    S_RIGHT = img.width - 20
    track_w = S_RIGHT - S_LEFT
    zero_x = (S_LEFT + S_RIGHT) // 2

    # track and zero-tick
    draw.rectangle([(S_LEFT, SY - TRACK_W), (S_RIGHT, SY + TRACK_W)], fill=TRACK_BG)
    draw.line([(zero_x, SY - TRACK_W - 4), (zero_x, SY + TRACK_W + 4)], fill=(160, 160, 160), width=2)

    # calculate position and draw fill/dot (Mapping is reversed here)
    norm_diff = float(np.clip(difference, -1.0, 1.0))
    cursor_x = int(zero_x - norm_diff * (track_w / 2)) 

    x0, x1 = min(zero_x, cursor_x), max(zero_x, cursor_x)
    draw.rectangle([(x0, SY - TRACK_W), (x1, SY + TRACK_W)], fill=DIFF_TRACK_FG)
    draw.ellipse([(cursor_x - DOT_R, SY - DOT_R), (cursor_x + DOT_R, SY + DOT_R)], fill=DIFF_DOT_FG, outline="white", width=2)

    # Horizontal Title (Difference Size)
    db = draw.textbbox((0, 0), "Difference Size", font=font_slider_title)
    dw, dh = db[2] - db[0], db[3] - db[1]
    # Place it directly below the slider, centered between the left bar and the right edge
    title_x = S_LEFT + (track_w // 2) - (dw // 2)
    draw.text((title_x, img.height - 35), "Difference Size", fill="black", font=font_slider_title)

    return img


def _render_frame(strength: float, difference: float) -> np.ndarray:
    """Render one video frame as an RGB numpy array."""
    illusion_w = WIDTH - LEFT_BAR
    illusion_h = HEIGHT - TOP_BAR - BOT_BAR
    illusion = pyllusion.Ebbinghaus(illusion_strength=strength, difference=difference)
    img = illusion.to_image(width=illusion_w, height=illusion_h, background="white")

    # Build full canvas
    canvas = PIL.Image.new("RGB", (WIDTH, HEIGHT), "white")
    canvas.paste(img, (LEFT_BAR, TOP_BAR))

    canvas = _add_labels(canvas, strength, difference)
    return np.array(canvas)


# ── Sequence Generation ────────────────────────────────────────────────────────

def generate_sequence():
    """Generates the seamless parametric path across the 4 stages."""
    diff_vals = []
    ill_vals = []

    def add_move(d_start, d_end, i_start, i_end, time_units):
        frames = int(FPS * time_units)
        # Use a smoothstep cosine interpolation for smooth easing
        t = np.linspace(0, 1, frames, endpoint=False)
        weight = (1 - np.cos(t * np.pi)) / 2
        
        diff_vals.extend(d_start + (d_end - d_start) * weight)
        ill_vals.extend(i_start + (i_end - i_start) * weight)

    # 1) Difference from 0 to negative max (-1), then to positive max (+1)
    add_move(0.0, -1.0, 0.0, 0.0, 1.0)
    add_move(-1.0, 1.0, 0.0, 0.0, 2.0)

    # 2) Illusion strength from 0 to positive max (+2), then to negative max (-2)
    add_move(1.0, 1.0, 0.0, 2.0, 2.0)
    add_move(1.0, 1.0, 2.0, -2.0, 4.0)

    # 3) Difference goes back to 0
    add_move(1.0, 0.0, -2.0, -2.0, 1.0)

    # 4) Illusion strength goes back to 0
    add_move(0.0, 0.0, -2.0, 0.0, 2.0)

    return diff_vals, ill_vals


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    
    diffs, strengths = generate_sequence()
    frames = []
    total_frames = len(diffs)

    print(f"Starting render of {total_frames} frames...")
    
    for i, (d, s) in enumerate(zip(diffs, strengths)):
        print(f"  Rendering frame {i+1}/{total_frames}", end="\r")
        frames.append(_render_frame(float(s), float(d)))

    print(f"\nWriting frames → {OUTPUT}")
    imageio.mimwrite(OUTPUT, frames, fps=FPS, codec="libx264",
                     output_params=["-pix_fmt", "yuv420p", "-crf", "18"])
    print("Done.")