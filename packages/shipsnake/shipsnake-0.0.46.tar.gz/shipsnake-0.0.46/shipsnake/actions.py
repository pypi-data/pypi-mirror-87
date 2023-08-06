import shipsnake.build
import toml
import sys
import os

with open('shipsnake.toml') as file:
	data = toml.loads(file.read())

if sys.platform.startswith('win'):
	shipsnake.build.main(data['latest_build'],[],nointeraction=True)
	print('Hub release...')
	a = f"hub release edit -a .\dist\pyinstaller\{data['name']}.exe {data['latest_build']}"
	print(a)
	print(os.popen(a).read())
elif sys.platform.startswith('darwin') or True:
	shipsnake.build.main(data['latest_build'],[],nointeraction=True)
	print('Hub release...')
	a = f"hub release create -a ./dist/pyinstaller/{data['name']}.dmg {data['latest_build']}"
	print(a)
	print(os.popen(a).read())
else:
	print('This is not being run on Mac and Windows.')