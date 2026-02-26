# IMGSRV
The microservice powering [PhotoBox](https://photobox.pw), a slimmed down version of [DankMemer/imgen](https://github.com/DankMemer/imgen) with some extra features. (transparent gifs, fit/contain images, other cropping functions)

## Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- [Redis](https://redis.io/) ([quickstart](https://redis.io/topics/quickstart), [db persistence](https://redis.io/topics/persistence))

## Installation
```bash
git clone https://github.com/PhotoBoxPW/IMGSRV
cd IMGSRV
uv sync
# Optional extras
# uv sync --extra perf
# uv sync --extra dev
```
> NOTE: `perf` includes `pillow-simd`, which has platform-specific build requirements. See the [installation instructions for Pillow-SIMD](https://github.com/uploadcare/pillow-simd#installation).

## Startup
```bash
uv run python server.py
```

With pm2
```bash
pm2 start pm2.json
```

## Sources
- [Gist by egocarib: pillow transparent gif creation workaround](https://gist.github.com/egocarib/ea022799cca8a102d14c54a22c45efe0)
- [TotallyNotChase/glitch-this](https://github.com/TotallyNotChase/glitch-this)
- [noelleleigh/glitch_me](https://github.com/noelleleigh/glitch_me)
- [Ovyerus/deeppyer](https://github.com/Ovyerus/deeppyer)
- [fengsp/color-thief-py](https://github.com/fengsp/color-thief-py)
- [StackOverflow: colorsys using native numpy operations](https://stackoverflow.com/a/7274986/6467130)