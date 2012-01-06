bash "install_passenger_nginx" do
  code <<-EOH
    apt-add-repository ppa:brightbox/passenger-nginx
    apt-get update
    apt-get -y install nginx-full
  EOH
end

bash "install_passenger" do
  code <<-EOH
    gem install passenger
    /etc/init.d/nginx start
    passenger-status
    /etc/init.d/nginx stop
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
