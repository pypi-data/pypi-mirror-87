import toml
import os
import sys
import glob
import shutil

# mode = sys.argv[1]
# mode="upload"
version = ""
if len(sys.argv) == 1:
	print("Provide a mode:\n\tshipsnake [wizard | build | dev | upload]")
	sys.exit(0)
mode = sys.argv[1]
if len(sys.argv) < 3 and mode in ["upload",'build']:
	print("Provide a version:\n\tshipsnake "+mode+" <version>")
	sys.exit(0)
if len(sys.argv)>2:
	version = sys.argv[2]
if mode=="dev" and version=="":
	version = "dev_build"


prefix = os.path.dirname(os.path.abspath(__file__))

if os.getenv('TEST_SNAKE')=="TRUE":
	os.chdir('tester')

questions = {
	"name":"Full name of project",
	"short_name":"Short name of project",
	"author":"Your name(s)",
	"email":"Project email",
	"short_description":"Short description of your project",
	"url":"Main project URL",
	"license":"License",
	"keywords":"Keywords seperated with a space",
	"data_files":"Data files (with *) to include in project seperated with a space",
	"file":"Main python file, leave blank for no main file",
	"modules":"Required modules, seperated with space"
}

if mode == "wizard":
	data = {}
	if os.path.isfile('./shipsnake.toml'):
		data = toml.loads(open('./shipsnake.toml').read())
	print("I'm going to ask you a few questions about your project to create a config file!\n\nPlease fill in everything to your ability. If you can't provide a value, leave it blank.\n")

	for key in questions:
		if key not in data:
			if len(glob.glob('./LICENS*'))>0 and key=="license":
				print('\033[1;34mYou seem to have a license file in your project, but what type is it?')
				for license in "AGPL-3.0/Apache-2.0/BSD-2-Clause/BSD-3-Clause/GPL-2.0/GPL-3.0/LGPL-2.1/LGPL-3.0/MIT".split('/'):
					print(f'\t- {license}')
				data[key] = input(">>>\033[0m ")
			elif len(glob.glob('./LICENSE*'))==0 and key=="license":
				data[key]=""
			elif key=="data_files" or key=="modules":
				data[key] = input("\033[1;34m"+questions[key]+":\033[0m ").split(' ')
			else:
				data[key] = input("\033[1;34m"+questions[key]+":\033[0m ")
		else:
			print("\033[1;34m"+questions[key]+":\033[0m "+data[key])
	
	if not os.path.isfile('./README.md'):
		open('README.md','w+').write(open('readme.template').read().format(**data))
	
	f = open('./shipsnake.toml','w+')
	f.write(toml.dumps(data))
	f.close()

elif mode in ["build","dev","upload"]:
	open('./.gitignore','w+').write('*'+os.sep+'__pychache__')
	if not os.path.isfile('./shipsnake.toml'):
		print('Please create a config file with `shipsnake wizard` first.')
		sys.exit(0)
	with open('./shipsnake.toml') as datafile:
		data = toml.loads(datafile.read())
	with open(prefix+'/setup.py.template') as datafile:
		template = datafile.read()
	setup = template.format(
		**data,
		version = version,
		entry_points = [data["short_name"]+"="+data["short_name"]+".__main__"] if data["file"]!="" else [""]
	)
	open('setup.py','w+').write(setup)
	source_dir = os.getcwd()
	target_dir = data["short_name"]+os.sep
	types = ('*.py',*data["data_files"])
	file_names = []
	for files in types:
		file_names.extend(glob.glob(files))
	if not os.path.isdir(target_dir):
		os.mkdir(target_dir)
	for file_name in file_names:
		if file_name in ["setup.py","shipsnake.toml"]:
			continue
		shutil.move(os.path.join(source_dir, file_name), target_dir+os.sep+file_name)
	open(target_dir+'__init__.py','w+').write('')
	if data['file']!="" and not os.path.isfile(data['short_name']+os.sep+'__main__.py'):
		try:
			os.rename(data['short_name']+os.sep+data['file'],data['short_name']+os.sep+'__main__.py')
			open(data['short_name']+os.sep+data['file'],'w+').write('# Please edit __main__.py for the main code. Thanks!\n(you can delete this file.)')
		except FileNotFoundError:
			pass
	try:
		shutil.rmtree('dist')
	except:
		pass
	try:
		os.mkdir('bin')
	except:
		pass
	open("bin"+os.sep+data['short_name'],'w+').write(f"#!/usr/bin/env bash\npython3 -m {data['short_name']} $@ || echo 'Error. Please re-install shipsnake with:\\n`pip3 install shipsnake --upgrade`'")
	if mode == "build" or mode=="upload":
		os.system('python3 ./setup.py sdist bdist_wheel')
		shutil.rmtree('build')
	elif mode == "dev":
		os.system('python3 ./setup.py develop')
	for x in glob.glob('*.egg-info'):
		shutil.rmtree(x)
else:
	print(f'Illegeal option `{mode}`')
	sys.exit(0)

if mode=="upload":
	print("Please make sure that you have a https://pypi.org/ account.")
	try:
		import twine
	except:
		input('Press enter to continue installing `twine`. Press ctrl+x to exit.')
		os.system('python3 -m pip install --user --upgrade twine || python3 -m pip install --upgrade twine')
	os.system('python3 -m twine upload dist/*')
