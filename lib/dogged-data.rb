# coding: utf-8

lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)

Gem::Specification.new do |spec|
    spec.name       = "dogged-data"
    spec.version    = "0.1"
    spec.authors    = ["Erik Feller"]
    spec.summary    = %q{Ruby script to collect data from the BV humane society website.}
    spec.description= %q{This project will eventually collect data on animals at the humane society as well as notify via email when animals meeting certain critera are put up for adoption}
    spec.license    = "MIT"

    spec.files      = ['lib/*.rb']
    spec.executables= ['bin/dogged-data']
    spec.test_files = ['tests/test_dogged']
    spec.require_paths = ["lib"]
    spec.add_runtime_dependency 'nokogiri'
end
