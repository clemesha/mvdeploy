
bash "install_ringsail" do
  cwd "/tmp"
  code <<-EOH
    git clone git://github.com/measuredvoice/ringsail.git
    sudo mkdir /var/www
    sudo mv ringsail /var/www/
  EOH
end

template "/var/www/ringsail/config/database.yml" do
  source "database.yml.erb"
  owner "root"
  group "root"
  mode "0644"
end

template "/var/www/ringsail/config/too_many_secrets.rb" do
  source "too_many_secrets.rb.erb"
  owner "root"
  group "root"
  mode "0644"
end

bash "rails_init" do
  cwd "/var/www/ringsail"
  code <<-EOH
    sudo gem install bundler
    sudo gem install rake
    bundle install --deployment --without development test
    bundle exec rake db:create RAILS_ENV="production"
    bundle exec rake db:schema:load RAILS_ENV="production"
    bundle exec rake db:populate RAILS_ENV="production"
    bundle exec rake assets:precompile
  EOH
end


bash "start_nginx" do
  code <<-EOH
    sudo /etc/init.d/nginx start
  EOH
end


