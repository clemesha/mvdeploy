bash "install_nodejs" do
  code <<-EOH
    sudo add-apt-repository ppa:chris-lea/node.js
    sudo apt-get update
    sudo apt-get -y install nodejs
  EOH
end
