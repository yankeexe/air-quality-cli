FROM golang:alpine AS build

ENV CGO_ENABLED=0

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build -o air

FROM alpine:latest

RUN addgroup -S cli && adduser -S cli -u 1000

USER cli

WORKDIR /home/cli

COPY --from=build --chown=cli /app/air ./

ENTRYPOINT ["./air"]
