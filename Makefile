setup_deploy:
	ansible-playbook -i ansible/hosts ansible/setup_kapellmeister.yml

setup_appserver:
	ansible-playbook -i ansible/hosts ansible/setup_appserver.yml

build:
	ansible-playbook -i ansible/hosts ansible/build_version.yml

local_build:
	ansible-playbook -i ansible/hosts ansible/build_version.yml --connection=local

install:
	ansible-playbook -i ansible/hosts ansible/install_version.yml --extra-vars "version=${version}"
