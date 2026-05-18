# Agents

## Image generation
- Use the Hugging Face Inference API (`huggingface_hub.InferenceClient`) for image generation by default
- Default model: `black-forest-labs/FLUX.1-dev`
- Token: `hf_xxxxx` (set via env variable or replace with your own)
- Save output as `<prompt_slug>_hf.png` (e.g. `rain_hf.png` for rain, `cat_hf.png` for a cat)
