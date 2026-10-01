from pathlib import Path
import hashlib
import threading

from PIL import Image, ImageDraw

from app.config import get_settings


_PIPELINE = None
_LOCK = threading.Lock()


def _name(text):
    return "panel_" + hashlib.sha256(text.encode()).hexdigest()[:12] + ".png"


def _mock(prompt, path, number):
    s = get_settings()

    img = Image.new(
        "RGB",
        (s.image_width, s.image_height),
        "white"
    )

    d = ImageDraw.Draw(img)

    d.rectangle(
        (12, 12, s.image_width - 12, s.image_height - 12),
        outline="black",
        width=5
    )

    d.text(
        (30, 35),
        f"COMICCRAFT - PANEL {number}",
        fill="black"
    )

    d.text(
        (30, 95),
        prompt[:220],
        fill="black"
    )

    d.text(
        (30, s.image_height - 70),
        "MOCK MODE - enable Diffusers for AI art",
        fill="black"
    )

    img.save(path)


def _pipeline():
    global _PIPELINE

    if _PIPELINE is not None:
        return _PIPELINE

    with _LOCK:
        if _PIPELINE is not None:
            return _PIPELINE

        import torch
        from diffusers import StableDiffusionPipeline

        s = get_settings()

        kwargs = {
            "torch_dtype": (
                torch.float16
                if torch.cuda.is_available()
                else torch.float32
            )
        }

        if s.hf_token:
            kwargs["token"] = s.hf_token

        pipe = StableDiffusionPipeline.from_pretrained(
            s.image_model_id,
            **kwargs
        )

        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        else:
            pipe.enable_attention_slicing()

        _PIPELINE = pipe

        return pipe


def generate_image(image_prompt, panel_number, seed=None):
    s = get_settings()

    filename = _name(
        f"{panel_number}:{image_prompt}"
    )

    path = s.panels_dir / filename

    if s.mock_mode or s.image_provider == "mock":
        _mock(
            image_prompt,
            path,
            panel_number
        )

        return f"/static/panels/{filename}"

    if s.image_provider != "diffusers":
        raise RuntimeError(
            f"Unsupported IMAGE_PROVIDER: {s.image_provider}"
        )

    import torch

    pipe = _pipeline()

    gen = None

    if seed is not None:
        gen = torch.Generator(
            device=(
                "cuda"
                if torch.cuda.is_available()
                else "cpu"
            )
        ).manual_seed(seed)

    result = pipe(
        image_prompt,
        width=s.image_width,
        height=s.image_height,
        num_inference_steps=s.image_steps,
        guidance_scale=s.image_guidance,
        generator=gen
    )

    result.images[0].save(path)

    return f"/static/panels/{filename}"