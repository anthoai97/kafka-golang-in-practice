package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"net/http"
	"time"

	dsr "webhook-simulator/dsr_agent"

	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
)

type server struct {
	dsr.UnimplementedDsrAgentServer
}

type MessagePackage struct {
	Agent     string      `json:"agent"`
	Data      interface{} `json:"data"`
	Timestamp string      `json:"timestamp"`
	AgentId   string      `json:"agent_id"`
	Resend    int16       `json:"resend"`
}

func main() {
	fmt.Println("Start Webhook Simulator Service....")
	httpServer()

	// grpc
	// grpcServer()
}

func grpcServer() {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", 50051))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	dsr.RegisterDsrAgentServer(s, &server{})
	log.Printf("Start Webhook Simulator gRPC Service at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

// SayHello implements helloworld.GreeterServer
func (s *server) SendMessage(ctx context.Context, in *dsr.GRPCMessagePackage) (*dsr.ServerReply, error) {
	log.Printf("Received: %v", in.GetData())
	time.Sleep(5 * time.Second)
	return &dsr.ServerReply{Message: "Hello " + in.GetAgent()}, nil
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
		var req MessagePackage
		if err := c.BindJSON(&req); err != nil {
			fmt.Println(err.Error())
		}
		time.Sleep(4 * time.Second)
		fmt.Printf("%+v\n", req)
		c.JSON(200, "OK")
	}
}
