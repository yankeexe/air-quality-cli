SHELL :=/bin/bash
.DEFAULT_GOAL=help
LDFLAGS := "-s -w"

test: # Run all tests
	@go test ./... -v

cover: # Launch a browser tab with coverage report
	@go test -v -coverprofile=c.out ./...
	@go tool cover -html=c.out
.PHONY: cover

clean: # Delete temp files
	@rm -f c.out || true
	@echo Temp files cleaned!

setup: # go mod tidy
	@go mod tidy
.PHONY: setup

dist: # Create distribution binaries
	mkdir -p bin
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags $(LDFLAGS) -a -installsuffix cgo -o bin/air
	CGO_ENABLED=0 GOOS=darwin go build -ldflags $(LDFLAGS) -a -installsuffix cgo -o bin/air-darwin
	CGO_ENABLED=0 GOOS=linux GOARCH=arm GOARM=6 go build -ldflags $(LDFLAGS) -a -installsuffix cgo -o bin/air-armhf
	CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -ldflags $(LDFLAGS) -a -installsuffix cgo -o bin/air-arm64
	CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -ldflags $(LDFLAGS) -a -installsuffix cgo -o bin/air.exe


help: # Show this help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
