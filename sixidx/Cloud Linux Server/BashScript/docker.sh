#https://docs.docker.com/engine/install/ubuntu/#install-docker-engine
sudo apt-get remove docker docker-engine docker.io containerd runc

#https://askubuntu.com/questions/1030179/package-docker-ce-has-no-installation-candidate-in-18-04
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu `lsb_release -cs` test"
sudo apt update
sudo apt install docker-ce

sudo docker run hello-world

docker -v

#sudo sh docker.sh