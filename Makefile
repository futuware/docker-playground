setup_deploy:
	ansible-playbook -i ansible/hosts ansible/setup_deploy.yml

setup_appserver:
	ansible-playbook -i ansible/hosts ansible/setup_appserver.yml
