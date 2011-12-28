
template "/home/ubuntu/.gemrc" do
  source "gemrc.erb"
  owner "ubuntu"
  group "ubuntu"
  mode "0644"
end

bash "install_rubygems-1.8.12" do
  cwd "/tmp"
  code <<-EOH
    wget http://production.cf.rubygems.org/rubygems/rubygems-1.8.12.tgz
    tar zxf rubygems-1.8.12.tgz
    cd rubygems-1.8.12
    sudo ruby setup.rb --no-format-executable
  EOH
end

