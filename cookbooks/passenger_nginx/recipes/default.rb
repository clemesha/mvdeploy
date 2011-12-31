bash "install_passenger_nginx" do
  code <<-EOH
    sudo apt-add-repository ppa:brightbox/passenger-nginx
    sudo apt-get update
    sudo apt-get -y install nginx-full
  EOH
end

bash "install_passenger" do
  code <<-EOH
    sudo gem install passenger
    sudo passenger-status
  EOH
end

template "/etc/nginx/conf.d/passenger.conf" do
  source "passenger.conf.erb"
  owner "root"
  group "root"
  mode "0644"
end

template "/etc/nginx/sites-enabled/default" do
  source "sites-enabled-default.erb"
  owner "root"
  group "root"
  mode "0644"
end
