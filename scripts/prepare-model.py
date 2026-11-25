"""Generate the model manifest and optionally upload files to R2. Run from project root."""
import pathlib,json,subprocess,argparse
p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('--upload',action='store_true');a=p.parse_args();root=pathlib.Path(a.folder);root=root/'phonon' if (root/'phonon').is_dir() else root
files=list(root.rglob('*')); files=[f for f in files if f.is_file()];
def find(name):
 f=next((f for f in files if f.name==name),None)
 if not f: raise SystemExit('Missing '+name)
 return f
def url(f):return '/models/'+f.relative_to(root).as_posix()
weights=next((f for f in files if f.name=='model.q8.gguf'),None);quant='q8' if weights else 'f32';weights=weights or find('model.safetensors');voices={f.stem:url(f) for f in files if f.suffix=='.safetensors' and (f.parent.name in ('voices','embeddings') or f.name=='default-voice.safetensors')};
if not voices:raise SystemExit('No voice embeddings found; inspect downloaded files.')
manifest={'quant':quant,'model':{'weights':{quant:url(weights)},'tokenizer':url(find('tokenizer.json')),'config':url(find('config.json')),'voices':voices,'defaultVoice':'parisa' if 'parisa' in voices else next(iter(voices))}}
path=root/'model.json';path.write_text(json.dumps(manifest,indent=2));print(path,manifest)
if a.upload:
 for f in files+[path]:subprocess.run(['npx','wrangler','r2','object','put','cilla-reader-models/'+f.relative_to(root).as_posix(),'--file',str(f),'--remote'],check=True)
else:
 import shutil
 dest=pathlib.Path('public/models');shutil.copytree(root,dest,dirs_exist_ok=True);print('Local model files copied to public/models; remove that folder before Cloudflare build.')
