# -*- mode: python ; coding: utf-8 -*-
# 빌드: 저장소 루트(이 spec이 있는 폴더)에서
#   pyinstaller --noconfirm SRPG.spec
# Srpg_Project.py 4번째 줄의 "version x.y.z" 를 읽어 dist/Srpg_x.y.z/ 및 exe 이름을 정합니다.
# 실행 시 dist 폴더 전체를 비우고, 해당 버전 폴더만 다시 채웁니다.
# (build 캐시는 건드리지 않습니다. 완전 초기화는: pyinstaller --clean --noconfirm SRPG.spec)

import re
import shutil
from pathlib import Path

# SPECPATH는 PyInstaller 버전에 따라 spec 파일 경로이거나, spec이 있는 폴더 경로일 수 있음.
_sp = Path(SPECPATH).resolve()
_spec_dir = _sp.parent if _sp.suffix == '.spec' else _sp
if not (_spec_dir / 'Srpg_Project' / 'Srpg_Project.py').is_file():
    raise RuntimeError(
        f'Srpg_Project/Srpg_Project.py 을 찾을 수 없습니다. '
        f'spec이 있는 저장소 루트(파이썬)에서 pyinstaller 를 실행하세요. (기준: {_spec_dir})'
    )
_src = _spec_dir / 'Srpg_Project' / 'Srpg_Project.py'
_lines = _src.read_text(encoding='utf-8').splitlines()
if len(_lines) < 4:
    raise RuntimeError(f'{_src} 에 최소 4줄이 필요합니다. (버전은 4번째 줄)')
_ver_m = re.search(r'version\s+([\w.-]+)', _lines[3], re.I)
if not _ver_m:
    raise RuntimeError(
        f'{_src} 4번째 줄에 version 이 필요합니다. 현재: {_lines[3]!r}'
    )
APP_NAME = 'Srpg_' + _ver_m.group(1).strip()

_dist = _spec_dir / 'dist'
if _dist.exists():
    shutil.rmtree(_dist)

a = Analysis(
    [str(_spec_dir / 'Srpg_Project' / 'Srpg_Project.py')],
    pathex=[str(_spec_dir)],
    binaries=[],
    datas=[
        (str(_spec_dir / 'Srpg_Project' / 'bgm'), 'bgm'),
        (str(_spec_dir / 'Srpg_Project' / 'effect_sound'), 'effect_sound'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)
