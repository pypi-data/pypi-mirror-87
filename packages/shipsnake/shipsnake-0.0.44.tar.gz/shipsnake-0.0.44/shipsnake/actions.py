import shipsnake.build
import toml
import sys
import os

with open('shipsnake.toml') as file:
	data = toml.loads(file.read())

if sys.platform.startswith('win'):
	shipsnake.build.main(data['latest_build'],[],nointeraction=True)
	print('Hub release...')
	os.system(f"hub release edit -a .\dist\pyinstaller\{data['name']}.exe {data['latest_build']}")
elif sys.platform.startswith('darwin'):
	shipsnake.build.main(data['latest_build'],[],nointeraction=True)
	print('Hub release...')
	os.system(f"hub release create -a ./dist/pyinstaller/{data['name']}.dmg {data['latest_build']}")
else:
	print('This is not being run on Mac and Windows.')