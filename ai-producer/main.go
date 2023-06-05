package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/gin-gonic/gin"
)

var (
	topic1      = "imageUpload"
	kafkaBroker = "localhost:9094"

	images = []string{"images/1.png", "images/2.png", "images/3.png", "images/4.png", "images/5.png", "images/6.png", "images/7.png", "images/8.png"}
)

func main() {

	p, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": kafkaBroker,
		"acks":              "all",
	})

	if err != nil {
		fmt.Printf("Failed to create producer: %s", err)
		os.Exit(1)
	}

	defer p.Close()

	// Go-routine to handle message delivery reports and
	// possibly other event types (errors, stats, etc)
	go func() {
		for e := range p.Events() {
			switch ev := e.(type) {
			case *kafka.Message:
				if ev.TopicPartition.Error != nil {
					fmt.Printf("Failed to deliver message: %v\n", ev.TopicPartition)
				} else {
					fmt.Printf("Produced event to topic %s: key = %-10s value = %s\n",
						*ev.TopicPartition.Topic, string(ev.Key), string(ev.Value))
				}
			}
		}
	}()

	// for n := 0; n < len(images); n++ {
	// 	time.Sleep(5 * time.Second)

	// 	p.Produce(&kafka.Message{
	// 		TopicPartition: kafka.TopicPartition{Topic: &topic1, Partition: kafka.PartitionAny},
	// 		Key:            []byte("source"),
	// 		Value:          []byte(images[n]),
	// 	}, nil)
	// }

	// Wait for all messages to be delivered
	// p.Flush(15 * 1000)

	fmt.Println("Start Storage Service....")

	router := gin.New()
	router.Use(gin.Recovery(), gin.Logger())

	router.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"data": "pong"})
	})

	router.POST("/arrange-reservation", ArrangeReservation())

	addr := fmt.Sprintf("0.0.0.0:%v", 8080)
	if err := router.Run(addr); err != nil {
		log.Fatal(err)
	}
}

func ArrangeReservation() func(*gin.Context) {
	return func(c *gin.Context) {
		// Parse JSON
		// var json struct {
		// 	Objects []*entity.RequestObjectDelete `json:"objects" binding:"required"`
		// }

		// if err := c.ShouldBind(&json); err != nil {
		// 	core.WriteErrorResponse(c, core.ErrBadRequest.WithError(err.Error()).WithDebug(err.Error()))
		// 	return
		// }

		// if len(json.Objects) < 1 {
		// 	err := errors.New("paths is emmpty")
		// 	core.WriteErrorResponse(c, core.ErrBadRequest.WithError(err.Error()).WithDebug(err.Error()))
		// 	return
		// }

		// res, err := api.business.DeleteS3Objects(c, json.Objects)
		// if err != nil {
		// 	core.WriteErrorResponse(c, core.ErrBadRequest.WithError(err.Error()).WithDebug(err.Error()))
		// 	return
		// }

		c.JSON(http.StatusOK, gin.H{"data": "pong"})
	}
}
