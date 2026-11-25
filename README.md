# cilla. — local-first Persian reader
Independent UI, built for Cilla Mini using phonon-tts 0.7.1. No text is sent to a server. Audio is generated on the device. Full WAV generation precedes playback in this version; the visual progress is generation progress, not streaming playback. Text normalization is limited to common Arabic/Persian letter variants (not the upstream full number normalizer).

## 1. Install
Node 22.12+ and Python 3, then `npm install`. Accept the model terms at https://huggingface.co/mehdi-hf/cilla-mini and download the authorized files with:

```sh
pip install -U huggingface_hub
hf auth login
hf download mehdi-hf/cilla-mini \
  --revision 480d6002169ee62ac7b88eed845e6624208a2ea2 \
  --include 'phonon/model/*' --local-dir model-download
```

The gated weights are not included. The helper expects config.json, tokenizer.json, model.q8.gguf or model.safetensors and voice embeddings under voices/ or embeddings/. If the upstream filenames differ, adapt scripts/prepare-model.py to the actual layout. See https://github.com/gradium-ai/xn-ptts/blob/main/ptts-wasm/js/README.md for the model spec.

## 2. Local test
```sh
python3 scripts/prepare-model.py model-download
npm run dev
```
Open the localhost URL. Paste & Listen requires a user gesture and clipboard permission; otherwise the text editor opens. Playback may require another tap in Safari. Test with a short Persian sentence first. No remote TTS fallback.

## 3. Deploy to GitHub Pages

1. After preparing the model locally, package the static files with `tar -czf cilla-mini-models.tar.gz -C public/models .`.
2. Create a GitHub Release with tag `cilla-mini-480d600` and attach `cilla-mini-models.tar.gz`.
3. In **Settings → Pages**, set **Source** to **GitHub Actions**.
4. Run **Actions → Deploy Cilla Reader to GitHub Pages → Run workflow** on `main`. The deployment job reports the site URL.

GitHub Actions downloads the release asset using its built-in GitHub token. The Pages artifact contains the app and the model under `models/`. The browser downloads weights directly from Pages. Hugging Face authentication is used only to obtain the original model when preparing the release asset. The checkpoint exceeds Git's 100 MiB per-file limit, so the source repository ignores model files.

Anyone who can open the published site can download its model assets. Check the model terms before publishing the artifact.

## Offline
Install via browser menu (iOS Safari: Add to Home Screen). The service worker caches visited shell/runtime files and phonon caches model files. After first successful online generation, reload once online to populate the shell cache, then test offline. Browser eviction can remove caches. No guarantee of persistent offline storage on iOS.

## Verification status
The production build and Persian speech with the real checkpoint were verified locally under the repository subpath. Live GitHub Pages deployment has not been verified. Model license CC BY-NC 4.0; see original model terms. The UI is independent, not an official Cilla product.
