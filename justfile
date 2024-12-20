build:
  docker build -t registry.paynepride.com/foo:latest .

push:
  just build
  docker push registry.paynepride.com/foo:latest
