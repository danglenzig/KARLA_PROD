from dataclasses import dataclass


@dataclass
class ImageStyle:
    COMIC: str = "Toon-shaded illustration in the style of 1970s American comic books, with bold black ink outlines, flat cel shading, slightly gritty print texture, warm paper tones, halftone shading, and dramatic graphic lighting. Keep the image visually clean and readable, not photorealistic, not glossy, not 3D. No text, no logos, no symbols, no signage."
    ANIME: str = "Clean modern anime illustration with crisp linework, expressive faces, smooth cel shading, controlled highlights, and a polished visual novel look. Use soft gradients only where needed. Keep the composition uncluttered and character-focused. No text, no logos, no symbols."
    PAINTERLY: str = "Atmospheric fantasy illustration with visible brushwork, soft edge variation, rich color transitions, and cinematic light falloff. The scene should feel hand-painted and storybook-like, not photorealistic. No text, no symbols, no signage."
    NOIR: str = "High-contrast noir illustration with deep shadows, limited color palette, hard-edged lighting, and moody urban atmosphere. Use dramatic silhouette shapes and restrained detail. Keep it graphic and readable rather than photographic. No text, no logos, no signage."
    PULP: str = "Retro pulp magazine illustration with bold composition, exaggerated motion, saturated colors, simplified anatomy, and vintage printing texture. It should feel like a classic paperback cover, not a movie poster. No text, no typography, no cover titles."
    WATERCOLOR: str = "Gentle watercolor illustration with soft washes, delicate outlines, warm natural light, and subtle paper texture. The scene should feel hand-made, calm, and emotionally clear. No text, no logos, no signage."
    CLEAN: str = "Clean editorial illustration with minimal shapes, restrained palette, strong silhouette readability, and polished vector-like finish. The image should feel professional and modern, with no clutter and no visible text."
    HORROR_VHS: str = "Grainy analog horror illustration with muted colors, low-key lighting, imperfect texture, and a slightly degraded late-20th-century feel. Keep it eerie but readable. No text, no subtitles, no signs, no labels."
    SCI_FI: str = "Sleek sci-fi concept illustration with hard surface design, luminous accents, environmental depth, and crisp speculative detail. Keep the layout clear and technically believable. No text, no interface labels."
    SATURDAY_MORNING: str = "Bright, exaggerated cartoon illustration with thick outlines, simplified shapes, cheerful color blocking, and high legibility. The composition should be playful and expressive without becoming noisy. No text, no speech bubbles, no logos."
