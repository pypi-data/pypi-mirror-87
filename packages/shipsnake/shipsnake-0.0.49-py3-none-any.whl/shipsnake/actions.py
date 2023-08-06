import shipsnake.build
import toml
import sys
import os

from github_release import gh_release_create

with open('shipsnake.toml') as file:
	data = toml.loads(file.read())

if sys.platform.startswith('win'):

	shipsnake.build.main(data['latest_build'],[],nointeraction=True)

	with open('shipsnake.toml') as file:
		data = toml.loads(file.read())

	gh_release_create(data['build']['github']+" ", data['latest_build'], publish=True, name="Version"+data['latest_build'], asset_pattern=f"./dist/pyinstaller/{data['name']}.dmg")

elif sys.platform.startswith('darwin') or True:

	shipsnake.build.main(data['latest_build'],[],nointeraction=True)

	with open('shipsnake.toml') as file:
		data = toml.loads(file.read())

	gh_release_create(data['build']['github']+" ", data['latest_build'], publish=True, name="Version"+data['latest_build'], asset_pattern=f"./dist/pyinstaller/{data['name']}.dmg")

else:
	print('This is not being run on Mac and Windows.')