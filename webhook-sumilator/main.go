package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	fmt.Println("Start Webhook Simulator Service....")

	router := gin.New()
	router.Use(gin.Recovery(), gin.Logger())

	router.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"data": "pong"})
	})

	router.POST("/hook", HookHandler())

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
