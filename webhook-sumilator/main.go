package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"net/http"

	pb "webhook-simulator/helloworld"

	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
)

type server struct {
	pb.UnimplementedGreeterServer
}

func main() {
	fmt.Println("Start Webhook Simulator Service....")
	// httpServer()

	// grpc
	grpcServer()
}

func grpcServer() {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", 50051))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterGreeterServer(s, &server{})
	log.Printf("Start Webhook Simulator gRPC Service at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

// SayHello implements helloworld.GreeterServer
func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
	log.Printf("Received: %v", in.GetName())
	return &pb.HelloReply{Message: "Hello " + in.GetName()}, nil
}

func httpServer() {
	fmt.Println("Start Webhook Simulator Http Service....")

	router := gin.New()
	router.Use(gin.Recovery(), gin.Logger())

	router.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"data": "pong"})
	})

	router.POST("/webhook", HookHandler())

	addr := fmt.Sprintf("0.0.0.0:%v", 8080)
	if err := router.Run(addr); err != nil {
		log.Fatal(err)
	}
}

func HookHandler() func(*gin.Context) {
	return func(c *gin.Context) {
		fmt.Println(c.Request.Header)
		body, _ := ioutil.ReadAll(c.Request.Body)
		fmt.Println(string(body))

		c.JSON(http.StatusOK, gin.H{"data": string(body)})
	}
}
