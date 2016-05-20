# -*- mode: python -*-

block_cipher = None


a = Analysis(['Pandemic-BlueDeck_Source.py'],
             pathex=['C:\\Users\\KC\\Documents\\Python Scripts\\Pandemic Decks- GUI'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries + [('icon.ico', 'C:\\Users\\KC\\Documents\\Python Scripts\\Pandemic Decks- GUI\\icon.ico', 'DATA')],
          a.zipfiles,
          a.datas,
          name='Pandemic-BlueDeck_Source',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='icon.ico')
