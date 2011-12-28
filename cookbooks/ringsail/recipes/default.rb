
bash "install_ringsail" do
  cwd "/tmp"
  code <<-EOH
    git clone git://github.com/measuredvoice/ringsail.git
    sudo mkdir /var/www
    sudo mv ringsail /var/www/
  EOH
end


bash "rails_init" do
  cwd "/var/www/ringsail"
  code <<-EOH
    sudo gem install bundler
    sudo gem install rake
    bundle install --deployment --without development test
    cp /tmp/database.yml /var/www/ringsail/config/database.yml
    cp /tmp/too_many_secrets.rb /var/www/ringsail/config/too_many_secrets.rb

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


