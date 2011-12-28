package "libssl-dev"
package "libncurses5-dev"
package "libreadline5-dev"


bash "install_ruby-1.9.2" do
  cwd "/tmp"
  code <<-EOH
    wget http://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.2-p290.tar.gz
    tar xzvf ruby-1.9.2-p290.tar.gz
    cd ruby-1.9.2-p290
    ./configure --prefix=/usr/local
    sudo make && sudo make install
  EOH
end

