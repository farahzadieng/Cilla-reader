# cilla. — local-first Persian reader
Independent UI, built for Cilla Mini using phonon-tts 0.4.2. No text is sent to a server. Audio is generated on the device. Full WAV generation precedes playback in this version; the visual progress is generation progress, not streaming playback. Text normalization is limited to common Arabic/Persian letter variants (not the upstream full number normalizer).

## 1. Install
Node 22.12+ and Python 3, then `npm install`. Accept the model terms at https://huggingface.co/mehdi-hf/cilla-mini and download the authorized files with:

```sh
pip install -U huggingface_hub
hf auth login
hf download mehdi-hf/cilla-mini --include 'phonon/*' --local-dir model-download
```

The gated weights are not included. The helper expects config.json, tokenizer.json, model.q8.gguf or model.safetensors and voice embeddings under voices/ or embeddings/. If the upstream filenames differ, adapt scripts/prepare-model.py to the actual layout. See https://github.com/gradium-ai/xn-ptts/blob/main/ptts-wasm/js/README.md for the model spec.

## 2. Local test
```sh
python3 scripts/prepare-model.py model-download
npm run dev
```
Open the localhost URL. Paste & Listen requires a user gesture and clipboard permission; otherwise the text editor opens. Playback may require another tap in Safari. Test with a short Persian sentence first. No remote TTS fallback.

## 3. Cloudflare
```sh
npx wrangler login
npx wrangler r2 bucket create cilla-reader-models
python3 scripts/prepare-model.py model-download --upload
rm -rf public/models
npm run deploy
```
R2 is required because large weights can exceed Workers static asset size limits. The Worker serves only model assets and the app. For Git integration set build command `npm run build`, deploy command `npx wrangler deploy`, root `/`. No HF token is deployed. Protect your personal deployment with Cloudflare Access if needed; confirm model redistribution terms before making it public. R2 billing may require activation and costs depend on use.

## Offline
Install via browser menu (iOS Safari: Add to Home Screen). The service worker caches visited shell/runtime files and phonon caches model files. After first successful online generation, reload once online to populate the shell cache, then test offline. Browser eviction can remove caches. No guarantee of persistent offline storage on iOS.

## Verification status
Source syntax checks only in the delivery environment; npm registry/model download, full build, actual speech and Safari/Cloudflare execution were not verified. Model license CC BY-NC 4.0; see original model terms. The UI is independent, not an official Cilla product.
